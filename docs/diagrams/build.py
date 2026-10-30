"""Write the README flow diagrams as SVG sources, and fill in the hero backdrop.

Each figure is laid out by hand on a grid. render.sh turns the sources into
the committed SVGs with text converted to paths.
"""

import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

BG_TOP, BG_BOTTOM = "#0b1020", "#151b33"
NODE_FILL, NODE_STROKE = "#1b2142", "#323b6e"
TEXT, MUTED, FAINT = "#e8ecff", "#8d97c9", "#6f78a8"
SOFT = "#b6bdd9"
LINE = "#5d689e"
HEAD = "#8d97c9"
MESH_OPACITY = 0.13
CHIP_FILL = "#20284f"
ACCENTS = {
    "skill": None,
    "start": "#4fd1c5",
    "ask": "#ffc861",
    "user": "#ff6b81",
    "store": "#5ee3a1",
    "violet": "#8b7bff",
}
MONO = "JetBrains Mono"


def text_width(text, size):
    return len(text) * size * 0.6


def fit(text, size, width):
    """Largest font size up to `size` at which `text` fits in `width`."""
    return min(size, round(width / (len(text) * 0.6), 1))


def squircle(x, y, w, h, r, n=5, steps=10):
    """Path for a rectangle whose corners are superellipse quarters."""
    r = min(r, w / 2, h / 2)
    corners = [(x + w - r, y + r, 0), (x + w - r, y + h - r, 90),
               (x + r, y + h - r, 180), (x + r, y + r, 270)]
    pts = []
    for cx, cy, start in corners:
        for i in range(steps + 1):
            a = math.radians(start - 90 + 90 * i / steps)
            c, s_ = math.cos(a), math.sin(a)
            px = cx + r * math.copysign(abs(c) ** (2 / n), c)
            py = cy + r * math.copysign(abs(s_) ** (2 / n), s_)
            pts.append(f"{px:.1f} {py:.1f}")
    return "M" + " L".join(pts) + " Z"


def warped_mesh(width, height, shift):
    """Grid lines over a gently rolling surface tilted away from the viewer:
    crossing swells over a slow roll, shifted per figure."""
    span, cell, density, tilt, swell = 4.8, 0.2, 10, 0.9, 1.9
    scale = width / span
    sx, sy = shift

    def lift(x, y):
        x, y = x + sx, y + sy
        return (0.14 * math.sin(2.1 * x + 1.3 * y) + 0.1 * math.cos(2.7 * y - 1.6 * x)
                + 0.22 * math.sin(0.45 * y + 0.9 * x))

    def point(x, y):
        z = swell * lift(x, y)
        return f"{width / 2 + x * scale:.0f} {(y - z * math.sin(tilt)) * scale:.0f}"

    def steps(start, stop, step):
        count = round((stop - start) / step) + 1
        return [start + i * step for i in range(count)]

    half, length = span / 2, height / scale
    across = steps(-half - 0.4, half + 0.4, 1 / density)
    along = steps(-0.6, length + 0.6, 1 / density)
    rows = [[point(x, y) for x in across] for y in steps(-0.6, length + 0.6, cell)]
    columns = [[point(x, y) for y in along] for x in steps(-half - 0.4, half + 0.4, cell)]
    return "".join("M" + "L".join(line) for line in rows + columns)


def backdrop(w, h, shift):
    """Defs and body for the squircle card with its glow and warped mesh,
    shared by the diagrams and the hero."""
    card = squircle(0, 0, w, h, 64)
    mesh = warped_mesh(w, h, shift)
    return (f"""    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0" r="0.9">
      <stop offset="0" stop-color="#7c5cff" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#7c5cff" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="card"><path d="{card}"/></clipPath>
    <linearGradient id="sides-fade">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.22" stop-color="#fff"/>
      <stop offset="0.78" stop-color="#fff"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="bottom-fade" x2="0" y2="1">
      <stop offset="0" stop-color="#fff"/>
      <stop offset="0.55" stop-color="#fff" stop-opacity="0.7"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="sides" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
      <rect width="{w}" height="{h}" fill="url(#sides-fade)"/>
    </mask>
    <mask id="bottom" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">
      <rect width="{w}" height="{h}" fill="url(#bottom-fade)"/>
    </mask>
""",
            f"""  <path d="{card}" fill="url(#bg)"/>
  <g clip-path="url(#card)">
    <path d="{card}" fill="url(#glow)"/>
    <g mask="url(#sides)"><g mask="url(#bottom)">
      <path d="{mesh}" fill="none" stroke="{TEXT}" stroke-opacity="{MESH_OPACITY}" stroke-width="1.4"/>
    </g></g>
  </g>
""")


class Figure:
    def __init__(self, name, width, height, label, shift=(0.0, 0.0)):
        self.name, self.width, self.height = name, width, height
        self.shift = shift
        self.parts = []
        self.edges = []
        self.labels = []
        self.nodes = {}
        self.label = label
        self.kinds = set()

    def node(self, key, x, y, w, title, sub=(), kind="skill", h=None, shape="box"):
        """Add a node centered on (x, y); `sub` lines render below the title."""
        sub = [sub] if isinstance(sub, str) else list(sub)
        h = h or (64 if not sub else 66 + 26 * len(sub))
        self.nodes[key] = (x, y, w, h)
        self.kinds.add(kind)
        accent = ACCENTS[kind]
        left, top = x - w / 2, y - h / 2
        out = []
        if shape == "pill":
            r = h / 2
            fill = accent + "1f"
            out.append(f'<rect x="{left}" y="{top}" width="{w}" height="{h}" rx="{r}" '
                       f'fill="{fill}" stroke="{accent}" stroke-width="2"/>')
        else:
            stroke = accent or NODE_STROKE
            box = squircle(left, top, w, h, 26)
            out.append(f'<path d="{box}" fill="{NODE_FILL}" stroke="{stroke}" stroke-width="2" filter="url(#lift)"/>')
            if accent:
                out.append(f'<path d="{box}" fill="{accent}" fill-opacity="0.07"/>')
        lines = len(sub)
        title_y = y + 9 - 13 * lines
        color = accent if (accent and shape == "pill") else TEXT
        weight = 600 if shape == "pill" else 500
        room = w - 48
        out.append(f'<text x="{x}" y="{title_y}" text-anchor="middle" font-family="{MONO}" '
                   f'font-size="{fit(title, 25, room)}" font-weight="{weight}" fill="{color}">{escape(title)}</text>')
        sub_size = min(fit(line, 18, room) for line in sub) if sub else 18
        for i, line in enumerate(sub):
            out.append(f'<text x="{x}" y="{title_y + 32 + 26 * i}" text-anchor="middle" '
                       f'font-family="{MONO}" font-size="{sub_size}" fill="{MUTED}">{escape(line)}</text>')
        self.parts.append("\n".join(out))

    def port(self, key, side, offset=0):
        x, y, w, h = self.nodes[key]
        return {
            "n": (x + offset, y - h / 2),
            "s": (x + offset, y + h / 2),
            "w": (x - w / 2, y + offset),
            "e": (x + w / 2, y + offset),
        }[side]

    def edge(self, points, label=None, at=None, dashed=False, color=LINE, arrow=True):
        """Draw an orthogonal path through `points` with rounded corners."""
        self.edges.append(rounded_path(points, color, dashed, arrow))
        if label:
            lx, ly = at or midpoint(points)
            self.chip(lx, ly, label)

    def chip(self, x, y, label, color=MUTED):
        w = text_width(label, 17) + 36
        self.labels.append(
            f'<rect x="{x - w / 2}" y="{y - 16}" width="{w}" height="32" rx="16" fill="{CHIP_FILL}" '
            f'stroke="#2c3463"/>'
            f'<text x="{x}" y="{y + 6}" text-anchor="middle" font-family="{MONO}" font-size="17" '
            f'font-weight="500" fill="{color}">{escape(label)}</text>')

    def legend(self):
        names = {"start": "start or end", "ask": "check", "user": "needs you",
                 "store": "saved file", "violet": "on request"}
        used = [k for k in names if k in self.kinds]
        out, x = [], self.width - 48
        for kind in reversed(used):
            label = names[kind]
            x -= text_width(label, 19)
            out.append(f'<text x="{x}" y="58" font-family="{MONO}" font-size="19" font-weight="500" '
                       f'fill="{SOFT}">{label}</text>')
            out.append(f'<circle cx="{x - 18}" cy="51" r="7" fill="{ACCENTS[kind]}"/>')
            x -= 50
        return "\n".join(out)

    def svg(self):
        w, h = self.width, self.height
        legend = self.legend()
        backdrop_defs, backdrop_body = backdrop(w, h, self.shift)
        tag = (f'<text x="48" y="58" font-family="{MONO}" font-size="18" font-weight="600" '
               f'letter-spacing="3" fill="{FAINT}">{escape(self.label.upper())}</text>')
        return f"""<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
{backdrop_defs}    <filter id="lift" x="-20%" y="-30%" width="140%" height="190%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000" flood-opacity="0.35"/>
    </filter>
    <marker id="head" viewBox="0 0 24 24" refX="20" refY="12" markerWidth="24" markerHeight="24" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M2 3 L22 12 L2 21 L7 12 Z" fill="{HEAD}"/>
    </marker>
  </defs>
{backdrop_body}  {tag}
{legend}
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
{chr(10).join(self.edges)}
  </g>
{chr(10).join(self.parts)}
{chr(10).join(self.labels)}
</svg>
"""


def midpoint(points):
    lengths = [abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(points, points[1:])]
    half = sum(lengths) / 2
    for (a, b), length in zip(zip(points, points[1:]), lengths):
        if half <= length:
            t = half / length
            return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        half -= length
    return points[-1]


def rounded_path(points, color, dashed, arrow, radius=18):
    d = [f"M{points[0][0]} {points[0][1]}"]
    for prev, cur, nxt in zip(points, points[1:], points[2:]):
        r = min(radius, seg(prev, cur) / 2, seg(cur, nxt) / 2)
        a = toward(cur, prev, r)
        b = toward(cur, nxt, r)
        d.append(f"L{a[0]} {a[1]} Q{cur[0]} {cur[1]} {b[0]} {b[1]}")
    end = points[-1]
    if arrow:
        end = toward(end, points[-2], 2)
    d.append(f"L{end[0]} {end[1]}")
    dash = ' stroke-dasharray="2 9"' if dashed else ""
    head = ' marker-end="url(#head)"' if arrow else ""
    return f'    <path d="{" ".join(d)}" stroke="{color}" stroke-width="2.5"{dash}{head}/>'


def seg(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def toward(p, q, dist):
    length = seg(p, q) or 1
    return p[0] + (q[0] - p[0]) * dist / length, p[1] + (q[1] - p[1]) * dist / length




def agenda():
    f = Figure("agenda", 1720, 780, "Agenda", shift=(0.5, 2.0))
    a, b, c, d = 230, 640, 1060, 1480
    top, mid, low = 200, 410, 600
    f.node("idea", a, 150, 330, "Idea, bug, or follow-up", kind="start", shape="pill")
    f.node("size", a, (top + mid) / 2 + 50, 240, "Needs a plan?", kind="ask", shape="pill", h=56)
    f.node("task", b, top, 330, "/agenda-task-create", "tasks/ · todo")
    f.node("plan", b, mid, 330, "/agenda-plan-create", "plans/ · planned")
    f.node("refine", b, low, 330, "/agenda-plan-refine", "concrete, evidence-backed")
    f.node("ready", c, mid - 105, 330, "/agenda-readiness", "settled and unblocked?", kind="ask")
    f.node("unblock", c, low - 10, 330, "/unblock", ["agent: technical calls", "you: the rest"], kind="user")
    f.node("pending", d, top, 330, "/pending", "what can start now")
    f.node("impl", d, mid, 330, "/agenda-implement", "in progress → done")
    f.node("gaps", d, low, 330, "/gaps", "work left undone")

    f.edge([f.port("idea", "s"), f.port("size", "n")])
    sx, sy = f.port("size", "e")
    fork = 430
    f.edge([(sx, sy), (fork, sy), (fork, top), f.port("task", "w")], "small", at=(fork, (sy + top) / 2))
    f.edge([(sx, sy), (fork, sy), (fork, mid), f.port("plan", "w")], "large", at=(fork, (sy + mid) / 2 + 4))
    f.edge([f.port("plan", "s"), f.port("refine", "n")])
    bus = 850
    ry = f.port("ready", "w")[1]
    f.edge([f.port("task", "e"), (bus, top), (bus, ry), f.port("ready", "w")])
    f.edge([f.port("refine", "e"), (bus, low), (bus, ry), f.port("ready", "w")])
    f.edge([f.port("ready", "s", -80), f.port("unblock", "n", -80)], "open decisions", at=(c - 80, 433))
    f.edge([f.port("unblock", "n", 90), f.port("ready", "s", 90)], "settled", at=(c + 90, 433))
    f.edge([f.port("ready", "e"), (1270, ry), (1270, top), f.port("pending", "w")], "ready", at=(1270, (ry + top) / 2))
    f.edge([f.port("pending", "s"), f.port("impl", "n")], "by hand or /autopilot", at=(d, (top + mid) / 2))
    f.edge([f.port("impl", "s"), f.port("gaps", "n")])
    gx, gy = f.port("gaps", "s")
    ix, iy = f.port("idea", "w")
    f.edge([(gx, gy), (gx, 715), (48, 715), (48, iy), (ix, iy)],
           "leftovers return as new tasks", at=(860, 715), dashed=True)
    return f


def finishing():
    f = Figure("finishing", 1720, 560, "Finishing work", shift=(2.2, 2.4))
    y = 290
    f.node("work", 200, 190, 280, "Finished work", kind="start", shape="pill")
    f.node("checks", 200, 400, 280, "/checks", "what passes, what fails")
    f.node("gaps", 620, y, 300, "/gaps", "tag each leftover", kind="ask")
    f.node("autofix", 620, 470, 300, "/autofix", "settle every tag", kind="violet", h=None)
    f.node("decide", 1090, y, 240, "/decide", "agent picks")
    f.node("un", 1480, 160, 320, "/unattended", "fix it now")
    f.node("rec", 1480, 420, 320, "/gaps-record", "save as an agenda task", kind="store")

    f.edge([f.port("work", "s"), f.port("checks", "n")])
    wx, wy = f.port("work", "e")
    f.edge([(wx, wy), (400, wy), (400, y), f.port("gaps", "w")])
    f.edge([f.port("autofix", "n"), f.port("gaps", "s")], dashed=True)
    fork = 840
    gx, gy = f.port("gaps", "e")
    uy, ry = 160, 420
    f.edge([(gx, gy), (fork, gy), (fork, uy - 18), (f.port("un", "w")[0], uy - 18)], "unattended", at=(1060, uy - 18))
    f.edge([(gx, gy), f.port("decide", "w")], "decision", at=(885, gy))
    f.edge([(gx, gy), (fork, gy), (fork, ry + 18), (f.port("rec", "w")[0], ry + 18)], "deferred", at=(1060, ry + 18))
    join = 1270
    dx, dy = f.port("decide", "e")
    f.edge([(dx, dy), (join, dy), (join, uy + 18), (f.port("un", "w")[0], uy + 18)], "small", at=(join, 240))
    f.edge([(dx, dy), (join, dy), (join, ry - 18), (f.port("rec", "w")[0], ry - 18)], "large or human", at=(join, 362))
    return f


def decisions():
    f = Figure("decisions", 1720, 580, "Decide", shift=(4.0, 2.0))
    y, gap, left = 300, 275, 175
    f.node("q", left, 150, 190, "A decision", kind="start", shape="pill")
    f.node("kind", left, y, 190, "Technical?", kind="ask", shape="pill", h=56)
    f.node("task", left, 465, 220, "/gaps-record", "a task for you", kind="user")
    xs = [485 + gap * i for i in range(4)]
    f.node("research", xs[0], y, 230, "/research", ["code, history,", "docs, prior art"])
    f.node("options", xs[1], y, 230, "/options", ["up to three", "candidates"])
    f.node("criteria", xs[2], y, 230, "/criteria", ["/hacky, /layering", "cause or patch?"])
    f.node("approach", xs[3], y, 230, "/approach", ["durable and", "proportionate?"], kind="ask")
    f.node("rec", 1575, y, 190, "Proposal", kind="start", shape="pill")
    f.edge([f.port("q", "s"), f.port("kind", "n")])
    f.edge([f.port("kind", "e"), f.port("research", "w")], "yes")
    f.edge([f.port("kind", "s"), f.port("task", "n")], "human or large", at=(left, 372))
    order = ["research", "options", "criteria", "approach", "rec"]
    for one, two in zip(order, order[1:]):
        f.edge([f.port(one, "e"), f.port(two, "w")])
    ax, ay = f.port("approach", "s")
    ox, oy = f.port("options", "s")
    f.edge([(ax, ay), (ax, 460), (ox, 460), (ox, oy)], "falls short: revise or try the next", at=((ax + ox) / 2, 460), dashed=True)
    return f


def spec():
    f = Figure("spec", 1720, 540, "Spec", shift=(1.3, 1.8))
    f.node("init", 220, 190, 280, "/spec-init", "only when asked", kind="user")
    f.node("standard", 220, 400, 280, "/spec", "the standard", kind="violet")
    f.node("spec", 760, 295, 360, ".spec/", ["overview · glossary · invariants", "features · decisions · api"], kind="store")
    f.node("code", 1400, 170, 320, "Code and tests", kind="start", shape="pill")
    f.node("sync", 1400, 420, 320, "/spec-sync", "in the same session", h=None)
    ix, iy = f.port("init", "e")
    f.edge([(ix, iy), (470, iy), (470, 270), f.port("spec", "w", -25)])
    sx, sy = f.port("standard", "e")
    f.edge([(sx, sy), (470, sy), (470, 320), f.port("spec", "w", 25)], dashed=True)
    px, py = f.port("spec", "e", -30)
    f.edge([(px, py), (1060, py), (1060, 170), f.port("code", "w")], "cites § IDs", at=(1060, (py + 170) / 2))
    f.edge([f.port("code", "s"), f.port("sync", "n")], "contract changes", at=(1400, 290))
    qx, qy = f.port("sync", "w")
    f.edge([(qx, qy), (1060, qy), (1060, 325), f.port("spec", "e", 30)], "updates entries", at=(1060, (qy + 325) / 2))
    return f


def debugging():
    f = Figure("debugging", 1720, 580, "Debug", shift=(1.0, 1.9))
    y = 240
    f.node("bug", 190, y, 270, "Bug or odd behavior", kind="start", shape="pill")
    f.node("debug", 560, y, 290, "/debug", "targeted logs to a file")
    f.node("cause", 960, y, 240, "Root cause?", kind="ask", shape="pill", h=56)
    f.node("fix", 1400, y + 18, 300, "/root-cause", "fix where it starts")
    f.node("cleanup", 1400, 450, 300, "/debug-cleanup", "drop probes, keep fix", kind="start")
    f.node("trace", 560, 450, 290, "/debug-trace", ".debug/traces/", kind="store")
    f.node("try", 960, 450, 260, "/temp", "trial fix, you confirm", kind="user")
    f.edge([f.port("bug", "e"), f.port("debug", "w")])
    f.edge([f.port("debug", "e"), f.port("cause", "w")])
    f.edge([f.port("cause", "e"), (f.port("fix", "w")[0], y)], "found", at=(1140, y))
    cx, cy = f.port("cause", "n")
    dx, dy = f.port("debug", "n")
    f.edge([(cx, cy), (cx, 125), (dx, 125), (dx, dy)], "not yet: ask one more question", at=((cx + dx) / 2, 125))
    f.edge([f.port("cause", "s"), f.port("try", "n")], "unsure of the fix", at=(960, 340))
    tx, ty = f.port("try", "e")
    fx = f.port("fix", "w")[0]
    f.edge([(tx, ty), (1200, ty), (1200, y + 36), (fx, y + 36)], "confirmed", at=(1200, (ty + y + 36) / 2))
    f.edge([f.port("fix", "s"), f.port("cleanup", "n")])
    f.edge([f.port("debug", "s"), f.port("trace", "n")], "spans sessions", at=(560, 345), dashed=True)
    return f


def chain(name, label, steps, shift, loop=None):
    """Lay out a workflow as one row of steps joined by arrows. `steps` are
    (title, sub, kind) tuples; `loop` is (from, to, label) indices for a dashed
    edge back along the bottom."""
    margin, gap, y = 48, 96, 176
    height = 360 if loop else 290
    f = Figure(name, 1720, height, label, shift=shift)
    w = (1720 - 2 * margin - gap * (len(steps) - 1)) / len(steps)
    for i, (title, sub, kind) in enumerate(steps):
        x = margin + w / 2 + i * (w + gap)
        pill = kind == "start"
        f.node(i, x, y, w, title, sub, kind=kind, h=92 if pill else 118, shape="pill" if pill else "box")
    for i in range(len(steps) - 1):
        f.edge([f.port(i, "e"), f.port(i + 1, "w")])
    if loop:
        a, b, text = loop
        ax, ay = f.port(a, "s")
        bx, by = f.port(b, "s")
        f.edge([(ax, ay), (ax, 300), (bx, 300), (bx, by)], text, at=((ax + bx) / 2, 300), dashed=True)
    return f


WORKFLOWS = [
    ("flow-commit", "Check, fix, and commit", (2.6, 1.4), [
        ("/checks", "run every check", "skill"),
        ("/fix-lints", "fix at the cause", "skill"),
        ("/git-commit", "once all pass", "store"),
    ], (1, 0, "check again")),
    ("flow-backlog", "Work through the backlog", (0.7, 2.6), [
        ("/goal", "until none left", "start"),
        ("/autopilot", "pick ready work", "skill"),
        ("/git-worktree", "one per plan", "skill"),
        ("Implement", "commit each unit", "store"),
    ], (3, 1, "next ready unit")),
    ("flow-unblock", "Clear the blockers", (3.4, 1.1), [
        ("/unblock", "open decisions", "skill"),
        ("/decide", "+ /recommended", "skill"),
        ("You", "the human calls", "user"),
        ("/pending", "ready to start", "start"),
    ], None),
    ("flow-roadmap", "Roadmap to running app", (1.8, 2.9), [
        ("/agenda-roadmap", "features you pick", "store"),
        ("/goal", "every plan", "start"),
        ("/agenda-implement", "with /fast-mode", "skill"),
        ("/run-app", "try it yourself", "user"),
    ], None),
    ("flow-wizard", "Start a new project", (2.9, 0.6), [
        ("/wizard", "your rough idea", "skill"),
        ("/research-web", "prior art", "skill"),
        ("You", "intent and taste", "user"),
        ("A plan", "ready to build", "store"),
    ], None),
    ("flow-criteria", "Decide with criteria", (0.4, 1.7), [
        ("/options", "lay out candidates", "skill"),
        ("/criteria", "weigh each one", "ask"),
        ("/recommended", "agent picks", "skill"),
        ("Decision", "work goes on", "start"),
    ], None),
    ("flow-plan", "Implement a plan", (3.8, 2.3), [
        ("/goal", "until the plan is done", "start"),
        ("/git-worktree", "own branch", "skill"),
        ("/agenda-implement", "item by item", "skill"),
        ("/git-worktree-finish", "merge back", "store"),
    ], None),
    ("flow-bug", "Chase a bug", (1.5, 0.9), [
        ("/debug", "targeted logs", "skill"),
        ("/root-cause", "fix where it starts", "skill"),
        ("/debug-cleanup", "drop the probes", "skill"),
        ("/git-commit", "just the fix", "store"),
    ], (1, 0, "not clear yet")),
    ("flow-review", "Review before publishing", (2.2, 2.0), [
        ("/review-bugs", "and /review-security", "skill"),
        ("Fix", "what is clear", "skill"),
        ("/review-leaks", "and /review-pii", "ask"),
        ("You push", "nothing private", "user"),
    ], None),
]


def workflows():
    return [chain(name, label, steps, shift, loop) for name, label, shift, steps, loop in WORKFLOWS]


def hero(out):
    """Fill the backdrop markers in the hero source, so the hero shares the
    diagrams' card and mesh."""
    src = (Path(__file__).parent.parent / "brand" / "hero.src.svg").read_text()
    defs, body = backdrop(1720, 602, (3.1, 2.2))
    for marker, part in (("<!-- backdrop defs -->", defs), ("<!-- backdrop -->", body)):
        if marker not in src:
            sys.exit(f"hero.src.svg: missing {marker}")
        src = src.replace(marker, part.rstrip())
    (out / "hero.src.svg").write_text(src)


def main(args):
    if args[0] == "--hero":
        hero(Path(args[1]))
        return
    out = Path(args[0])
    for figure in (agenda(), finishing(), decisions(), spec(), debugging(), *workflows()):
        (out / f"{figure.name}.src.svg").write_text(figure.svg())


if __name__ == "__main__":
    main(sys.argv[1:])
