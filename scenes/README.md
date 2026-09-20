# Scene Repository

A shared, git-tracked library of game-agnostic Godot scene structures (`.tscn` / `.tres`) pulled
out of past projects.

> **This library is currently empty.** Nothing ships pre-filled. It grows from your own projects
> via the `HARVEST-REPO.md` protocol.

## How agents use it

Agents do not scan this folder directly. They route through `../global-index/README.md`, which is
generated from the actual contents of this repository:

```bash
python framework_tools/build_global_index.py
```

Run it after adding or removing anything here.

## Structure

One folder per category, created only once it has a real entry. Each scene ships with a companion
`.md` of the same base name explaining what it is, what it expects, and how to wire it in — the
first line of its `## What it does` section becomes the entry's description in the index.

```
audio/    camera/    movement/    ui/    vfx/
```

## The UI pairing rule

UI systems are always extracted as a **pair**, never as a lone scene or a lone script:

1. The scene structure (`.tscn` / `.tres`) goes here, under `ui/`.
2. The logic (`.gd`) goes in `../mechanics/ui/`.
3. Each companion doc explicitly links the other, so finding either half leads to the other.

A scene harvested without its script, or a script without its scene, is not reusable — it is a
fragment that the next integrator has to reverse-engineer.

## Adding an entry

Run `HARVEST-REPO.md` from the project the scene came from, or copy it in by hand with its
companion doc. Strip project-specific coupling first: hardcoded `res://` paths to game-specific
resources, references to autoloads that only exist in the source project, and node names that only
make sense in one game.

Then regenerate the index.
