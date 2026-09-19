# Mechanic Repository

A shared, git-tracked library of engine-agnostic-to-*which game* Godot mechanics pulled out of
past projects — checked before writing new code for a system that's plausibly already been
solved once. This is not a per-project template (see `docs/templates/` for those); it's a
growing collection of working, reusable implementations.

Read side is wired into the dual-agent workflow: Gemini checks here before scoping new
implementation work (see `GEMINI.md`'s "Mechanic Repository" section) and Claude Code knows how
to pull an entry in (see `CLAUDE.md`'s "Mechanic Repository" section). Populating this repository
itself is a separate, manual curation step — nothing here gets added or edited automatically.

## Structure

One folder per category, created only once it has a real entry (no placeholder folders for
hypothetical future categories). Current categories:

```
mechanic-repository/
  ai/            combat/        input/         procgen/       spawning/      utility/
  audio/         minigame/      movement/      rules_engine/  ui/            vfx/
  camera/
```

Most mechanics are exactly two files, same base name, in their category folder:

- `<mechanic_name>.gd` — the script itself, generalized to drop project-specific coupling
  (hardcoded node paths, autoload names unique to the source project, magic values tuned for
  one game's feel) in favor of `@export`s and clearly-named extension points.
- `<mechanic_name>.md` — the companion doc, using the template below. This is what makes an
  entry usable without re-reading the code first.

**Multi-file exception:** some mechanics are inherently several cooperating classes (Godot
requires one `class_name` per file) — e.g. `movement/tether_*.gd` (5 files, one physics system)
or `combat/projectile_preset*.gd` + `preset_driven_projectile.gd` (a data resource + pool +
consumer). These still ship as exactly one companion `.md`, but its filename won't match any
single `.gd`'s base name — it's named for the system as a whole (e.g.
`movement/tether_swing_physics.md`). The doc's own text lists every file it covers.

## Companion doc template

```markdown
# <Mechanic Name>

## What it does
One or two plain-language sentences.

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

Manual, on-demand — not something either agent does mid-task. When a script proves genuinely
reusable (built for one project, no game-specific coupling left after review), copy it in under
the right category with its companion doc filled out per the template above. Prefer generalizing
a script in place over leaving multiple near-duplicate variants of the same mechanic.

## Master Index

*The following is a high-level overview of the available mechanics so agents can decide whether to reuse, adapt, or build from scratch.*

### Movement (`movement/`)
- **`movement_state_machine.gd`**: A highly decoupled, game-agnostic first-person movement core based on a hierarchical state machine (Grounded, Airborne, Sliding).
- **`bounce_pad_trigger.gd`**: A generic trigger that launches CharacterBody3Ds upward upon overlap. (Partner scene in `scene-repository/movement/bounce_pad.tscn`)

### Minigame (`minigame/`)
- **`physics_crafter.gd`**: A crafting node that dynamically shrinks physics bodies when they collect inside an area and pops out a configured result object.

### UI (`ui/`)
- **`hud.gd`**: A decoupled Heads-Up Display logic script that binds to a generic `ammo_changed` signal. (Partner scene in `scene-repository/ui/hud.tscn`)
- **`reticle.gd`**: A procedural crosshair `Control` node that draws itself without relying on textures.
- **`scene_transition.gd`**: A scene autoload owning an entire scene change — iris wipe closed, `change_scene_to_file()`, wipe open — with duck-typed `on_transition_out()` / `on_transition_in()` hooks so scenes opt into flourishes and a scene that implements neither still transitions. Requires `iris_wipe.gd`. (Partner scene in `scene-repository/ui/scene_transition.tscn`)
- **`iris_wipe.gd`**: The iris wipe's progress→radius maths as pure static functions, mirroring the shader so corner coverage is unit-testable without a viewport. (Companion of `scene_transition.gd`)
- **`scale_pulse_component.gd`**: A reusable component to punch the scale of a `CanvasItem` on a beat or event, settling securely back to its resting scale without compounding scale errors. (Partner scene in `scene-repository/ui/scale_pulse_component.tscn`)
- **`interactive_button_component.gd`**: A generic component to standardize button interaction feedback, adding hover scale tweens and optional audio hooks. (Partner scene in `scene-repository/ui/interactive_button_component.tscn`)

### Audio (`audio/`)
- **`throttled_audio_component.gd`**: A generic audio rate-limiter that spaces out rapidly-fired overlapping sound effects using global lockouts. (Partner scene in `scene-repository/audio/throttled_audio_component.tscn`)

### VFX (`vfx/`)
- **`impact_burst.gd`**: A generic hit feedback visual effect script that self-cleans on emission completion. (Partner scene in `scene-repository/vfx/impact_burst.tscn`)
