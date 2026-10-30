# Rust Async Practices

## Contents

- Core model
- Mechanism guide
- UI and request paths
- Sync/async boundaries
- Blocking and CPU-bound work
- Locks and shared state
- Channels and backpressure
- Tasks, cancellation, and shutdown
- Streams and fanout
- Public APIs and async traits
- Runtime and Cargo choices
- Testing and review checklist
- Source anchors

## Core Model

Rust async is cooperative concurrency, not automatic parallelism.

- Calling an `async fn` creates a future. It does not do the work until the future is awaited, spawned, or otherwise polled.
- `.await` is where a task can yield to the runtime. Long CPU loops or blocking calls between awaits can starve unrelated work on the same executor thread.
- `join!`, `try_join!`, `select!`, and many stream combinators run branches concurrently on the current task. They are not a CPU parallelism primitive.
- `tokio::spawn` and similar runtime spawns schedule independent async tasks. They still must avoid blocking.
- OS threads are for synchronous work that needs a blocking boundary or CPU parallelism. Async tasks are for non-blocking waits and high-concurrency orchestration.

## Mechanism Guide

| Mechanism | Use for | Avoid when |
| --- | --- | --- |
| Plain synchronous function | Quick deterministic CPU work that will not block a UI/request/executor path. | The function waits on I/O, sleeps, blocks on locks, or runs long CPU loops in async/UI paths. |
| `async fn` / future | I/O waits, timers, async protocol steps, and composable operations that should yield while waiting. | The body mostly performs CPU-heavy work or wraps blocking sync APIs without offloading. |
| `tokio::join!` / `try_join!` | A small fixed set of futures that should make progress together in one task. | You need CPU parallelism, isolation, independent cancellation, or dynamic task counts. |
| `tokio::select!` | Race shutdown, timeout, channel receive, signal, or alternate async branches. | Any branch is not cancellation-safe, or looped selection would lose buffered progress. |
| `tokio::spawn` | Independent async work on the runtime with `Send + 'static` futures on multithreaded runtimes. | Work blocks, is CPU-heavy, borrows non-static data, or can fail silently if detached. |
| `tokio::task::spawn_local` / `LocalSet` | `!Send` futures such as `Rc` or UI-affine state on a local executor. | The task may migrate threads or should be runtime-agnostic. |
| `tokio::task::JoinSet` | Dynamic sets of homogeneous Tokio tasks whose completions should be drained and whose drop should abort outstanding tasks. | Tasks have heterogeneous output types or must keep running after the owner drops. |
| `FuturesUnordered` | Dynamic sets of futures that should be polled as a stream without necessarily spawning tasks. | You need runtime task isolation, task IDs, or task abort handles. |
| `StreamExt::buffer_unordered(n)` | Bounded concurrent processing over many inputs where output order does not matter. | `n` is unbounded, result order matters, or each item needs independent task ownership. |
| Bounded `tokio::sync::mpsc` | Async producer-to-single-consumer queues with explicit backpressure. | Broadcast/pub-sub is needed, or blocking synchronous callers will use async `send`. |
| `oneshot` | A single response, completion notification, or request/reply return path. | Repeated messages or shared state updates are needed. |
| `watch` | Latest-value state where receivers only need the newest value. | Every historical event must be observed. |
| `broadcast` | Pub/sub events where every receiver should see each message, with lag handling. | Only one worker should consume each job. |
| `std::sync::mpsc` / crossbeam/flume sync channels | Communication between blocking threads. | Waiting from async code; blocking `recv` parks the executor thread. |
| `tokio::task::spawn_blocking` | Short-lived blocking operations or blocking libraries called from async code. | The work is long-lived, unbounded CPU fanout, or must be abortable after it starts. |
| `tokio::task::block_in_place` | Rare short blocking sections from within Tokio multithreaded runtime code when restructuring is impractical. | Current-thread runtimes, library code, UI paths, or work that can be moved to `spawn_blocking`. |
| Dedicated `std::thread::spawn` | Long-lived blocking loops, OS-thread-affine libraries, sync runtimes, or custom stack/name needs. | The work is async I/O that belongs on the runtime. |
| Rayon | CPU-bound data parallelism such as map/reduce, parsing batches, image operations, sorting, or compression. | Work must `.await`, hold async resources, or interact with async cancellation directly. |
| Runtime `block_on` | An explicit sync adapter at an outer boundary. Store/reuse a runtime rather than creating one per call. | Already inside async code, on UI/event-loop threads, inside libraries by surprise, or on hot paths. |

## UI And Request Paths

UI callbacks, render/update functions, event-loop handlers, and request handlers should return quickly. Treat them as latency-sensitive even when they are not literally async.

Bad:

```rust
fn on_click(path: PathBuf) -> Result<Summary> {
    let bytes = std::fs::read(path)?;
    parse_large_file(&bytes)
}
```

Better: move blocking work off the UI path and deliver the result by the framework's task/message mechanism.

```rust
fn start_import(path: PathBuf, tx: tokio::sync::mpsc::Sender<Message>) {
    tokio::spawn(async move {
        let result = tokio::task::spawn_blocking(move || {
            let bytes = std::fs::read(path)?;
            parse_large_file(&bytes)
        })
        .await
        .map_err(Error::from_join)
        .and_then(|inner| inner);

        let _ = tx.send(Message::ImportFinished(result)).await;
    });
}
```

For UI frameworks with native async command types, use those instead of inventing a side channel. For example, Iced exposes `Task::perform` for async work:

```rust
fn update(state: &mut State, message: Message) -> iced::Task<Message> {
    match message {
        Message::FetchWeather => {
            iced::Task::perform(fetch_weather(), Message::WeatherFetched)
        }
        Message::WeatherFetched(weather) => {
            state.weather = Some(weather);
            iced::Task::none()
        }
    }
}
```

Keep UI state mutation on the UI owner. Background work should send messages, events, or data snapshots back.

## Sync/Async Boundaries

Prefer async all the way down inside async applications. Add sync wrappers only at explicit edges such as a CLI command, C FFI boundary, test harness, or separate blocking client API.

Good sync wrapper shape:

```rust
pub struct BlockingClient {
    runtime: tokio::runtime::Runtime,
    inner: Client,
}

impl BlockingClient {
    pub fn get(&self, key: &str) -> Result<Value> {
        self.runtime.block_on(self.inner.get(key))
    }
}
```

Rules:

- Do not create a new runtime per method call.
- Do not call `block_on` from async code to wait for async work. Await it or spawn and communicate.
- Do not hide runtime creation inside a general-purpose library unless the API is explicitly a blocking adapter.
- If a sync callback must trigger async work, spawn onto an existing runtime handle and return through a channel, callback, or framework event.

## Blocking And CPU-Bound Work

Use async alternatives when they exist:

```rust
// Bad in async code.
std::thread::sleep(Duration::from_millis(50));

// Good.
tokio::time::sleep(Duration::from_millis(50)).await;
```

Use `spawn_blocking` for bounded blocking calls that eventually finish:

```rust
let digest = tokio::task::spawn_blocking(move || compute_digest(path))
    .await
    .map_err(Error::from_join)??;
```

For many CPU-heavy jobs, bound concurrency or use Rayon:

```rust
let permits = Arc::new(tokio::sync::Semaphore::new(num_cpus::get()));

for job in jobs {
    let permit = permits.clone().acquire_owned().await?;
    tokio::spawn(async move {
        let _permit = permit;
        tokio::task::spawn_blocking(move || run_cpu_job(job)).await
    });
}
```

Prefer a dedicated thread for persistent blocking loops:

```rust
let handle = std::thread::Builder::new()
    .name("device-reader".into())
    .spawn(move || read_device_loop(device, tx))?;
```

Remember:

- `spawn_blocking` tasks generally cannot be aborted after they start.
- `spawn_blocking` uses a blocking pool with a large upper limit, so CPU-heavy fanout needs its own bound.
- Blocking in a destructor dropped from async code can still block the executor path.

## Locks And Shared State

The default preference order is ownership/message passing, small synchronous lock scopes, then async locks when the protected operation must await.

Good synchronous lock scope:

```rust
async fn get_user(cache: Arc<std::sync::Mutex<HashMap<UserId, User>>>, id: UserId) -> Option<User> {
    {
        let cache = cache.lock().expect("cache mutex poisoned");
        if let Some(user) = cache.get(&id).cloned() {
            return Some(user);
        }
    }

    fetch_user(id).await.ok()
}
```

Bad:

```rust
let mut cache = cache.lock().expect("cache mutex poisoned");
let user = fetch_user(id).await?;
cache.insert(id, user);
```

Use `tokio::sync::Mutex` when the lock must guard an async resource across `.await`, such as a single database connection or protocol stream. Even then, keep the lock around the smallest resource operation, not unrelated computation.

Often better: actor-style ownership of the resource.

```rust
enum DbCommand {
    Get {
        key: String,
        reply: tokio::sync::oneshot::Sender<Result<Option<Value>>>,
    },
}

let (tx, mut rx) = tokio::sync::mpsc::channel::<DbCommand>(64);

tokio::spawn(async move {
    while let Some(command) = rx.recv().await {
        match command {
            DbCommand::Get { key, reply } => {
                let _ = reply.send(client.get(&key).await);
            }
        }
    }
});
```

## Channels And Backpressure

Pick channel semantics deliberately:

- `mpsc`: job queue, command queue, actor mailbox, one consumer.
- `oneshot`: return one result from a worker.
- `watch`: publish latest state, no event history.
- `broadcast`: every subscriber sees every event, with lag handling.
- `std::sync::mpsc` or crossbeam/flume: blocking thread communication, not async wait paths.

Prefer bounded channels. Capacity is a product decision: too small can cause unnecessary head-of-line blocking, too large can hide overload and memory growth.

Bad unbounded fanout:

```rust
for item in items {
    tokio::spawn(process(item));
}
```

Better bounded stream:

```rust
use futures::{stream, StreamExt, TryStreamExt};

let results = stream::iter(items)
    .map(|item| async move { process(item).await })
    .buffer_unordered(16)
    .try_collect::<Vec<_>>()
    .await?;
```

## Tasks, Cancellation, And Shutdown

Tasks are owned work. Decide who observes completion, errors, and cancellation.

- Await `JoinHandle`s for important work, or store them in a supervisor.
- Dropping a Tokio `JoinHandle` detaches the task; it does not mean the task completed successfully.
- Use `JoinSet` for dynamic task groups that should be drained and aborted when the set is dropped.
- Use `CancellationToken`, channel closure, or explicit shutdown messages for graceful task shutdown.
- Use `abort` for forceful cancellation, and then await the handle if you need to observe completion.

Timeout around a spawned task must explicitly abort the task if expiration should stop it:

```rust
let mut handle = tokio::spawn(do_work());

let value = match tokio::time::timeout(Duration::from_secs(5), &mut handle).await {
    Ok(joined) => joined.map_err(Error::from_join)?,
    Err(_) => {
        handle.abort();
        let _ = handle.await;
        return Err(Error::TimedOut);
    }
};
```

With `select!`, losing branches are cancelled. In a loop, only select over operations that are cancellation-safe or restructure the state machine.

```rust
loop {
    tokio::select! {
        biased;

        _ = shutdown.cancelled() => break,
        maybe_msg = rx.recv() => {
            let Some(msg) = maybe_msg else { break };
            handle_message(msg).await?;
        }
    }
}
```

Be cautious with `read_exact`, `write_all`, lock acquisition, semaphore acquisition, and custom futures inside repeated `select!` loops unless the relevant docs say they are cancellation-safe for your usage.

## Streams And Fanout

Use the smallest abstraction:

- Fixed small set: `join!` or `try_join!`.
- Race or shutdown: `select!`.
- Many inputs with bounded concurrency: `buffer_unordered(n)` or `buffered(n)`.
- Dynamic spawned task set: `JoinSet`.
- Dynamic non-spawned futures: `FuturesUnordered`.

Do not add spawning just to get concurrency if a stream combinator can keep ownership, error handling, and concurrency bounds simpler.

## Public APIs And Async Traits

Native `async fn` in traits is usable, especially for private traits. Public traits need care because callers may need bounds such as `Send` on the returned future, and async trait methods are not dyn-compatible by default.

For a public trait that must work on multithreaded executors, prefer an explicit returned future bound or a generated variant:

```rust
pub trait Fetcher: Send + Sync {
    fn fetch(&self, url: Url) -> impl Future<Output = Result<Bytes>> + Send;
}
```

Use `async-trait` or another boxing approach only when dynamic dispatch is actually needed or the project supports older Rust versions. Make the allocation and dynamic dispatch tradeoff explicit.

Avoid exposing runtime-specific types in library APIs unless the library is intentionally runtime-specific. Plain `async fn` does not itself require Tokio, but using Tokio timers, channels, task spawning, or I/O types does.

## Runtime And Cargo Choices

Use the runtime the project already uses unless there is a clear reason to change it.

- Tokio: default choice for many network services and ecosystem integrations.
- async-std: std-like async APIs when the project is already built around it.
- smol/async-executor: small embeddable runtimes or libraries that already use that stack.
- futures crate: runtime-agnostic traits and combinators.
- Rayon/std threads: synchronous CPU or thread-bound work, not an async runtime.

Cargo guidance:

- In applications, `tokio = { version = "1", features = ["rt-multi-thread", "macros", "time", "sync"] }` is often better than `full` unless the app genuinely uses everything.
- In libraries, avoid enabling broad runtime features by default. Use optional features for runtime integrations.
- Use `cargo tree -e features` when an async crate unexpectedly pulls in runtime, TLS, OS, or full feature dependencies.
- Be careful with `default-features = false`: every dependency path must avoid defaults for the default set to stay disabled.

## Testing And Review Checklist

Before finishing async changes, verify:

- Blocking calls are not on UI, request, or async executor paths.
- Long CPU work is bounded and offloaded to `spawn_blocking`, Rayon, or dedicated threads.
- Every queue, fanout, and task group has a bound or explicit lifecycle reason.
- Lock guards do not cross `.await`, except intentional async locks around async resources.
- Important `JoinHandle`s are awaited, supervised, or intentionally detached with a comment or owner.
- Timeouts and `select!` branches have the intended cancellation semantics.
- Shutdown paths notify tasks and wait for cleanup when needed.
- Public async traits have the needed `Send`/dyn story.
- Runtime-specific APIs match the project's runtime.
- Tests cover at least one overload, cancellation, timeout, or shutdown path when the change affects those behaviors.

Use project-local validation first: `cargo fmt`, focused tests, then `cargo clippy` or broader tests when shared async behavior changed.

## Source Anchors

- Rust Book: async/await, futures, streams, and runtime execution: https://doc.rust-lang.org/book/ch17-00-async-await.html
- Rust Book: futures, tasks, and threads are complementary: https://doc.rust-lang.org/book/ch17-06-futures-tasks-threads.html
- Tokio task docs: tasks should not block executor threads; use `spawn_blocking`/`block_in_place` for blocking sections: https://docs.rs/tokio/latest/tokio/task/
- Tokio `spawn_blocking`: blocking work, CPU-bound bounds, non-abortability, dedicated thread guidance: https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html
- Tokio shared state: synchronous mutex is fine only for low contention and no lock held across `.await`: https://tokio.rs/tokio/tutorial/shared-state
- Tokio channels: channel choices, bounded capacity, and backpressure: https://tokio.rs/tokio/tutorial/channels
- Tokio `select!`: cancellation safety and non-cancellation-safe operations: https://docs.rs/tokio/latest/tokio/macro.select.html
- Tokio sync bridging: sync wrappers around async clients with stored runtimes: https://tokio.rs/tokio/topics/bridging
- Tokio `JoinSet`: dynamic spawned task groups and drop-aborts behavior: https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html
- Tokio-util `CancellationToken`: cooperative shutdown token: https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html
- futures `StreamExt::buffer_unordered`: bounded concurrent stream processing: https://docs.rs/futures-util/latest/futures_util/stream/trait.StreamExt.html#method.buffer_unordered
- Rayon: data parallelism for CPU-bound work: https://docs.rs/rayon/
- Rust std `thread::spawn`: dedicated OS thread behavior and join/detach semantics: https://doc.rust-lang.org/std/thread/fn.spawn.html
- Rust std `mpsc`: blocking sync channels and bounded/unbounded variants: https://doc.rust-lang.org/std/sync/mpsc/index.html
- Rust async traits announcement: public async traits, Send bounds, and dyn dispatch gaps: https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/
- Rust Reference: dyn compatibility excludes async fn and opaque return types: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
- Cargo Book: dependency features, defaults, and feature unification caveats: https://doc.rust-lang.org/cargo/reference/features.html
- Iced docs: UI update functions can return `Task` for async work: https://docs.rs/iced/latest/iced/
