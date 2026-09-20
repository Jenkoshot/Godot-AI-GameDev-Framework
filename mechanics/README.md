# Mechanic Repository

A shared, git-tracked library of reusable Godot mechanics pulled out of past projects — checked
before writing new code for a system that has plausibly already been solved once. This is not a
per-project template (see `docs/templates/` for those); it is a growing collection of working
implementations, generalised so they are agnostic to *which game* uses them.

> **This library is currently empty.** Nothing ships pre-filled. It grows from your own projects
> via the `HARVEST-REPO.md` protocol — build a mechanic in a game, prove it works, then harvest
> it here.

## How agents use it

Read side is wired into the agent workflow: the Architect checks here before scoping new
implementation work, and the Executor knows how to pull an entry in. Neither scans this folder
directly — both route through `../global-index/README.md`, which classifies every entry by
dimension (2D / 3D / Agnostic) and feature area so an agent never reaches for a `Node3D` mechanic
in a 2D game.

The index is **generated**, not hand-maintained:

```bash
python framework_tools/build_global_index.py
```

Run it after adding or removing anything here. `--check` exits non-zero if the index has drifted,
which makes it usable as a pre-commit or CI guard.

## Structure

One folder per category, created only once it has a real entry — no placeholder folders for
hypothetical future categories. The categories the index knows how to route:

```
ai/        camera/    input/      movement/      rules_engine/   ui/
audio/     combat/    minigame/   procgen/       spawning/       utility/     vfx/
```

Most mechanics are exactly two files, same base name, in their category folder:

- `<mechanic_name>.gd` — the script, generalised to drop project-specific coupling (hardcoded node
  paths, autoload names unique to the source project, magic values tuned for one game's feel) in
  favour of `@export`s and clearly-named extension points.
- `<mechanic_name>.md` — the companion doc, using the template below. This is what makes an entry
  usable without reading the code first, and it is where the index gets each entry's description.

**Multi-file exception:** some mechanics are inherently several cooperating classes, because Godot
allows one `class_name` per file — a tethering physics system split across five scripts, or a
projectile system that is a data resource plus a pool plus a consumer. These still ship exactly
one companion `.md`, named for the system as a whole rather than matching any single `.gd`. The
doc's own text lists every file it covers.

## Steering the index

Two optional HTML comments in a companion `.md` override the automatic classification:

```markdown
<!-- index: vfx_explosions -->
<!-- dimension: 3D -->
```

Without them, the feature area comes from the category folder and the dimension is inferred from
the code (`Vector2`/`Node2D`/`Sprite2D` versus `Vector3`/`Node3D`/`MeshInstance3D`; both or
neither means Agnostic). Set them when the inference would be wrong — for example a pure-maths
helper in `movement/` that belongs under `procgen_layouts`.

## Companion doc template

```markdown
# <Mechanic Name>

## What it does
One or two plain-language sentences. The first line becomes the entry's description in the
global index, so lead with what it does, not how it works.

## Dependencies
- Godot version assumptions (if narrower than 4.x generally)
- Required autoloads/singletons, or "none"
- Required project settings (input map actions, physics/collision layers, etc.), or "none"
- Other scripts/scenes it expects to exist alongside it

## How to wire it in
Step-by-step: where the file goes, what node it attaches to, what scene structure it expects,
what signals to connect, what to set via the Inspector after dropping it in.

## Source
- Extracted from: <project name>, `<original path within that project>`
- Extracted on: <YYYY-MM-DD>

## Known limitations / gotchas
Anything a future integrator should know before relying on it — edge cases it doesn't handle,
assumptions it makes, performance caveats.
```

## Adding an entry

Deliberate and on-demand, not something an agent does mid-task. When a script proves genuinely
reusable — built for one project, no game-specific coupling left after review — run
`HARVEST-REPO.md` from that project, or copy it in by hand under the right category with its
companion doc filled out. Prefer generalising a script in place over leaving several near-duplicate
variants of the same mechanic.

UI is always harvested as a **pair**: the scene into `../scenes/ui/`, the script here in `ui/`,
with each companion doc cross-linking the other.

Then regenerate the index. An index entry pointing at a file that is not there is worse than no
entry at all — it sends every future agent on a lookup that fails.
