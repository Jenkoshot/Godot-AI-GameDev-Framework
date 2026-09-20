# Tweak Guide — Quick Variable Reference

A single lookup table for every hand-tunable value in this project — speeds, colors, sizes,
thresholds — so you can go straight to the file and variable without reading (or asking an AI to
re-explain) the surrounding script.

**How this file works**
- Only lists values meant to be hand-tuned: `@export` vars and top-level `const`s used for
  tuning/feel. Internal state (`var`), implementation-detail consts (epsilons, clamps, magic
  numbers that exist for numerical safety rather than design), and anything not meant to be
  edited are left out on purpose — this file is for knobs, not internals.
- Grouped by system, matching the system names already used in `project-state/_overview.md` and
  `project-state/[system].md`.
- Kept current by the Executor Agent as part of every task's documentation-consistency check
  (see `EXECUTOR.md`'s task-completion step) — if a task adds, removes, renames, or changes the default of a tunable,
  this file is updated in the same task, regardless of whether the task is otherwise "trivial."
  An entry that no longer matches the code is a bug, same as any other stale doc.
- Not a substitute for the Godot Inspector — for `@export` vars, the Inspector is still the
  fastest place to *try* a value live. This file is for finding *which script* owns a value and
  understanding what it does before you go there, and for `const`s that aren't Inspector-visible
  at all.

**Columns**
- **Variable** — exact name in code.
- **File** — where it lives (`res://...` path).
- **Kind** — `@export` (Inspector-editable) or `const` (edit in script directly).
- **Default** — value as of the last update to this file.
- **What it does** — one line, plain language, no jargon.
- **Safe range / notes** — known-good bounds, what breaks if pushed too far, or how it interacts
  with other values in the same table.

---

## [System Name]

| Variable | File | Kind | Default | What it does | Safe range / notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| _(none yet)_ | | | | | |

---

*(Add one `## [System Name]` section per system as tunables are introduced — match the system
names already in use elsewhere in `project-state/`. Delete the placeholder row in a section once
it has real entries. Delete an entire section if a system is removed.)*
