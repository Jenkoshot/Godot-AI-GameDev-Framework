# Scene Repository

A shared, git-tracked library of game-agnostic Godot scene structures (`.tscn` / `.tres`) pulled out of past projects.

## Master Index

*The following is a high-level overview of the available scenes so agents can decide whether to reuse, adapt, or build from scratch.*

### UI (`ui/`)
- **`hud.tscn`**: A decoupled Heads-Up Display scene featuring a reticle and ammo label. (Partner script in `mechanic-repository/ui/hud.gd`)
- **`scene_transition.tscn`**: A high-layer CanvasLayer + full-rect ColorRect overlay for use as a scene autoload, carrying `iris_wipe.gdshader` / `IrisWipeShader.tres` — a full-screen iris wipe whose disc reaches the screen corner at any aspect ratio. (Partner script in `mechanic-repository/ui/scene_transition.gd`)
- **`scale_pulse_component.tscn`**: A scene node carrying the `scale_pulse_component.gd` for visual punch feedback.
- **`interactive_button_component.tscn`**: A component node carrying the `interactive_button_component.gd` for generic button feedback.

### Movement (`movement/`)
- **`bounce_pad.tscn`**: A generic trigger area with a cylinder shape for launching characters. (Partner script in `mechanic-repository/movement/bounce_pad_trigger.gd`)

### Audio (`audio/`)
- **`throttled_audio_component.tscn`**: A scene structure containing standard audio players for rate-limited sound effects.

### VFX (`vfx/`)
- **`impact_burst.tscn`**: A generic hit feedback visual effect scene. (Partner script in `mechanic-repository/vfx/impact_burst.gd`)
