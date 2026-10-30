# Rust Patterns

Small examples of the patterns in the skill, written for the 2024 edition.
Adapt names to the project, and use its existing error and newtype helpers
when it has them.

## Contents

- Enums instead of option bags
- Exhaustive matching without wildcards
- Let-else, let chains, and if-let guards
- Newtypes with validating constructors
- Typestate
- Typed errors
- Checked conversions and arithmetic
- Lint configuration
- Compile-time contract tests

## Enums Instead Of Option Bags

```rust
// Describes combinations that cannot happen: `data` and `error` both set,
// or `loading` with data.
struct Loose<T> {
    loading: bool,
    data: Option<T>,
    error: Option<String>,
}

// Exactly the real states.
enum Remote<T, E> {
    Loading,
    Loaded(T),
    Failed(E),
}
```

## Exhaustive Matching Without Wildcards

```rust
#[derive(Clone, Copy)]
enum Status {
    Draft,
    Review,
    Published,
    Archived,
}

fn is_visible(status: Status) -> bool {
    match status {
        Status::Published => true,
        // Listed, not `_`: a new variant is a compile error here.
        Status::Draft | Status::Review | Status::Archived => false,
    }
}
```

## Let-Else, Let Chains, And If-Let Guards

```rust
use std::collections::HashMap;

fn port(config: &HashMap<String, String>) -> Result<u16, ConfigError> {
    // let-else: bind or leave.
    let Some(raw) = config.get("port") else {
        return Err(ConfigError::Missing("port"));
    };
    raw.parse().map_err(|_| ConfigError::Invalid("port"))
}

fn admin_name(user: Option<&User>) -> Option<&str> {
    // Let chains (2024 edition): no nested `if let` pyramid.
    if let Some(user) = user
        && user.is_admin
        && let Some(name) = user.display_name.as_deref()
    {
        return Some(name);
    }
    None
}

fn describe(event: &Event) -> String {
    match event {
        // if-let guard (Rust 1.95): match and destructure in one arm.
        Event::Message(body) if let Ok(n) = body.trim().parse::<u32>() => {
            format!("number {n}")
        }
        Event::Message(body) => format!("text {body}"),
        Event::Closed => "closed".to_owned(),
    }
}
```

## Newtypes With Validating Constructors

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Email(String); // Private field: only `TryFrom` can build one.

impl TryFrom<String> for Email {
    type Error = EmailError;

    fn try_from(raw: String) -> Result<Self, Self::Error> {
        match raw.split_once('@') {
            Some((local, domain)) if !local.is_empty() && domain.contains('.') => Ok(Self(raw)),
            Some(_) | None => Err(EmailError { raw }),
        }
    }
}

impl Email {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// IDs that cannot be swapped by accident.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(u64);
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct OrderId(u64);
```

Expose `as_str` or similar accessors rather than `Deref`, so the newtype does
not inherit the inner type's whole API.

## Typestate

```rust
use std::marker::PhantomData;

pub struct Draft;
pub struct Signed;

pub struct Request<State> {
    body: Vec<u8>,
    signature: Option<[u8; 32]>,
    state: PhantomData<State>,
}

impl Request<Draft> {
    pub fn new(body: Vec<u8>) -> Self {
        Self { body, signature: None, state: PhantomData }
    }

    // Consumes the draft: an unsigned request cannot be sent.
    pub fn sign(self, key: &Key) -> Request<Signed> {
        let signature = key.sign(&self.body);
        Request { body: self.body, signature: Some(signature), state: PhantomData }
    }
}

impl Request<Signed> {
    pub fn send(&self) -> Result<(), SendError> {
        transmit(&self.body, self.signature)
    }
}
```

## Typed Errors

```rust
use std::{error::Error, fmt, io, path::PathBuf};

#[derive(Debug)]
pub enum LoadError {
    Read { path: PathBuf, source: io::Error },
    Parse { path: PathBuf, line: usize, message: String },
}

impl fmt::Display for LoadError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Read { path, .. } => write!(f, "cannot read {}", path.display()),
            Self::Parse { path, line, message } => {
                write!(f, "{}:{line}: {message}", path.display())
            }
        }
    }
}

impl Error for LoadError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Read { source, .. } => Some(source),
            Self::Parse { .. } => None,
        }
    }
}

pub fn load(path: PathBuf) -> Result<String, LoadError> {
    std::fs::read_to_string(&path).map_err(|source| LoadError::Read { path, source })
}
```

A derive-based error crate can generate the `Display` and `Error` impls when
the project already uses one; the shape of the enum is what matters.

## Checked Conversions And Arithmetic

```rust
fn to_index(value: i64) -> Result<usize, std::num::TryFromIntError> {
    usize::try_from(value) // Instead of `value as usize`, which wraps negatives.
}

fn total(price: u32, quantity: u32) -> Option<u32> {
    price.checked_mul(quantity) // Instead of `price * quantity`.
}

fn last(items: &[u8]) -> Option<u8> {
    items.last().copied() // Instead of `items[items.len() - 1]`.
}
```

## Lint Configuration

```toml
[lints.rust]
unsafe_code = "forbid"
missing_debug_implementations = "warn"

[lints.clippy]
pedantic = { level = "warn", priority = -1 }
unwrap_used = "warn"
expect_used = "warn"
panic = "warn"
indexing_slicing = "warn"
as_conversions = "warn"
wildcard_enum_match_arm = "warn"
allow_attributes = "warn"
allow_attributes_without_reason = "warn"
undocumented_unsafe_blocks = "warn"
```

Exceptions then read as:

```rust
#[expect(clippy::indexing_slicing, reason = "callers pass `chunks_exact(64)` chunks")]
fn header(chunk: &[u8]) -> &[u8] {
    &chunk[..8]
}
```

## Compile-Time Contract Tests

````rust
/// An unsigned request cannot be sent:
///
/// ```compile_fail
/// let request = my_crate::Request::new(Vec::new());
/// request.send();
/// ```
pub struct Request<State> { /* ... */ }
````

The doctest fails the build if the misuse ever starts compiling. Use
`assert_matches!` (import it from `std`, Rust 1.96) for runtime pattern
assertions, since it prints the value on failure.
