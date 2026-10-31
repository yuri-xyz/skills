---
name: readme
description: Use when writing, creating, restructuring, formatting, or reviewing a project's `README.md`, its hero, screenshots, or GIFs, or deciding what belongs in it versus other docs. Not for agent instruction files such as `AGENTS.md`, which are `/agents-md-init` and `/agents-md-compress`, or for `.spec/` documents, which are `/spec`.
---

# README

## Objective

A README is the project's front page for people. Optimize for a glance: in
a few seconds a reader should know what the project is, see it working, and
know how to try it. Keep it simple and minimal. Show the product with a hero
and animations instead of explaining it, and leave instructions, internals,
and reference material to the docs or the site.

Aim for a page that fits in two or three screens. When in doubt, cut.

## Gather first

Read what the README will claim instead of recalling or guessing it: the
manifest and flake (name, packages, binaries), the install route, the
license files, the project's site, and any existing logo, art, or
screenshots. Keep accurate text the user wrote by hand.

## Layout

Use these parts in order. Every README has the **What it is**, **Install**,
and **Usage** sections, headed exactly `### What it is`, `### Install`, and
`### Usage`; leave out any other part that does not apply.

1. **Hero.** The logo or banner on a designed background image, centered,
   with light and dark variants when the art depends on the page theme.
   It names the project, so the README needs no title heading.
2. **Tagline.** One or two centered lines: what it is and the one thing that
   sets it apart, such as "A monospace font for code and terminals, drawn
   entirely in Python". Break with `<br>` instead of letting it wrap.
3. **Links.** One centered row of the site's key pages separated by ` · `,
   when the project has a site.
4. **Showcase.** Animated GIFs of the product or its features in use, each
   followed by one centered caption line stating one fact. This carries
   the page; prefer one more GIF over one more paragraph.
5. **What it is.** At most two short paragraphs of plain, human-readable
   prose on what the project is, who it is for, and what problem it solves,
   written for someone who has never heard of it. No bullet lists, jargon,
   internals, or slogans such as "blazingly fast" or "modern".
6. **Install.** The shortest route to having it, in one small code block.
   Link the docs for anything beyond it.
7. **Usage.** The first thing a user does with it: a short command, code, or
   config example with its result, covering the main use only. Link the docs
   for options and the rest.
8. **License.** One or two sentences, the license linked to its file, plus
   any exception.

A development section is optional: at most a dev-shell command and one
pointer, such as "Run `just` for every recipe", or a link to a contributing
doc.

Leave out:

- the tech stack, dependency lists, architecture, internal modules, or
  implementation details;
- long instructions, configuration references, option tables, or FAQs;
- badges, tables of contents, "Introduction" or "About" sections beyond
  What it is,
  changelogs, and roadmaps.

Link to them when they exist elsewhere.

## Format

- Every heading is `###`. Never mix heading levels, and never use `#`,
  `##`, or `####`.
- Use raw HTML only to center the hero, tagline, links, showcase, and
  captions: `<p align="center">` around images and `<div align="center">`,
  with blank lines inside, around centered Markdown. Keep install and
  license left-aligned.
- Give every image an explicit `width` and alt text that carries its
  message, including what an animation does, so the page reads without
  images. For example: "Operators such as -> and => turning into ligatures
  and back, each character keeping its cell".
- Run every piece of prose, including the tagline, captions, and bullets,
  through `/humanize` once the draft is done, so it reads like the author
  wrote it rather than like generated copy.
- Use fenced code blocks with a language tag, prose wrapped near 80
  columns, and relative links for repo files. Use emoji sparingly, and only
  when the project already uses them.

## Assets

Every image is made for GitHub's README column, which renders about 830 to
880 CSS pixels wide.

- **Dimensions.** Render at 2× the displayed size for sharp high-DPI
  display and set the displayed size with `width`: about 1600 to 1760 px
  wide for full-width art shown at 800 to 880, and logos at 2× their shown
  size. Crop to the content; no empty margins.
- **Format.** SVG for logos and banners, with text converted to paths,
  because GitHub serves SVGs as images and loads no external fonts or
  scripts. PNG for static screenshots. GIF for animations; GitHub does not
  play videos committed to the repo inline.
- **Weight.** Keep each GIF under about 3 MB and the whole page under about
  10 MB. Trim GIFs to a short loop, lower the frame rate (12 to 20 fps is
  enough for UI), limit the palette, and cut the size before the quality.
  Optimize with `gifski` or `gifsicle -O3 --lossy`, PNGs with `oxipng`, and
  SVGs with `svgo`, run through `/nix-run`.
- **Themes.** When art depends on the background, ship `-light` and `-dark`
  variants and switch with `<picture>`:

  ```html
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/hero-dark.gif">
    <img src="docs/hero-light.gif" width="800" alt="…">
  </picture>
  ```

  Art with its own opaque background, such as a hero on a designed backdrop,
  needs only one variant.
- **Location.** Keep assets in `docs/` (logos and banners in
  `docs/brand/`) and reference them by repo-relative path. Commit the
  source that renders them, such as a recipe or script, so they can be
  regenerated.

Never invent or fake art, screenshots, or recordings. When the project has
none, use a centered text tagline and report the missing hero or GIFs as
follow-ups.

## Organizing

The root README is for people deciding whether to use the project. Usage
guides, architecture, and references belong in `docs/` or the site, linked
from it. Give a subdirectory its own README only when it is a standalone
unit with its own audience, such as a published package, crate, or flake,
and keep it to that unit's tagline, What it is, Install, Usage, and
license.

## Verify

- Confirm the README has its What it is, Install, and Usage sections, and
  that the prose has had its `/humanize` pass.
- Run or check every command shown, inside the project's dev shell.
- Check that every link and image path resolves, both theme variants exist,
  and each asset meets the size and weight limits above.
- A README is public. Check it with `/review-pii` for home paths, hostnames,
  and personal details, and with `/review-leaks` for private workflow
  material before it ships.

## Skeleton

````markdown
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/brand/hero-dark.svg">
    <img src="docs/brand/hero-light.svg" width="800" alt="The Name logo on its hero background">
  </picture>
</p>

<div align="center">

What it is, in one line,<br>and the one thing that sets it apart.

[example.dev](https://example.dev) · [docs](https://example.dev/docs)

</div>

<p align="center">
  <img src="docs/feature.gif" width="800" alt="What the animation shows happening">
</p>

<div align="center">

One fact the animation proves.

</div>

### What it is

One or two short paragraphs: what it is, who it is for, and what it solves.

### Install

```sh
install-command
```

### Usage

```sh
name do-the-main-thing   # what it does
```

### License

[License name](LICENSE).
````
