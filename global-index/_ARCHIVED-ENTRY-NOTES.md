# Curated Entry Notes (archived)

These are the hand-written descriptions that existed in the previous, hand-maintained
`global-index/`. That index is now generated from the actual contents of `mechanics/`,
`scenes/`, and `assets/` (see `framework_tools/build_global_index.py`), so these notes are kept
here rather than being lost.

Every mechanic below was described in the old index but is **not present in this distribution**.
Treat this as a wishlist of things worth building or harvesting, not as an inventory. When you
do add one, put the description in the entry's companion `.md` and the generator will pick it up.

| Dimension | Feature area | Entry | Description |
| :--- | :--- | :--- | :--- |
| 2D | ui components | Collapsible Section | A toggle-button-driven show/hide section — click the header to expand/collapse the content |
| 2D | ui components | Floating Text Popup | Spawns floating, fading text — the classic "+10" damage/score popup that drifts upward and fades |
| 2D | ui components | Idle Sway Animation | Applies continuous sine/cosine-driven rotation plus squash-stretch "breathing" to the parent |
| 2D | ui feedback and juice | Button Hover Juice | Attach as a child of any `BaseButton` (Button, TextureButton, etc.) to add a hover scale-bump |
| 2D | ui feedback and juice | Scale Pop Animator | A generic "pop in / pop out" show-hide animation helper for UI nodes: `pop_in` scales a node |
| 2D | ui feedback and juice | Scale Pulse Feedback | One-shot "pop" feedback: scales a target node up with a springy ease-out, then eases back down |
| 2D | ui hud | Hud | The `.tscn` structure for the player HUD. |
| 2D | ui hud | Reticle | A procedural, crosshair-drawing `Control` node script that requires no texture imports. |
| 2D | ui transitions | Iris Wipe | The progress → radius curve behind an iris-wipe transition, as pure static functions on a |
| 2D | ui transitions | Scene Transition | The `.tscn` and shader for the universal scene transition. Two nodes and twelve lines of GLSL. |
| Agnostic | camera systems | Lookahead Camera Offset | Offsets a `Camera2D` in the direction a tracked object has drifted laterally away from a |
| Agnostic | camera systems | Spring Arm Follow Camera | A third-person mouse-look camera rig: a `Node3D` pivot holding a `SpringArm3D`. Captures the |
| Agnostic | camera systems | Trauma Screen Shake | A textbook "trauma"-model screen shake (the classic GDC-talk technique): call |
| Agnostic | combat logic | Data Driven Swing Animator | Plays a named "move" from a data dictionary as a strike-then-recovery tween sequence on a target |
| Agnostic | combat logic | Debounced Impact Detector | A static scoring/impact target. The `StaticBody2D` itself gives physical bounce to anything that |
| Agnostic | combat logic | Gesture Quality Swing Controller | A mouse-driven melee swing controller with two phases: a "wind-up" stance, where the sword |
| Agnostic | combat logic | Hit Reaction Flash | A visual "juice" component for taking a hit: plays a parallel tween combo on a target node — an |
| Agnostic | combat logic | Radial Destructible Target | A multi-stage destructible target: a ring of independently-destructible segments shields a core, |
| Agnostic | combat projectiles | Projectile Preset System | A weighted-nothing (uniform) random preset system for projectiles: `ProjectilePreset` is a data |
| Agnostic | combat stats and damage | Item Stats | A data-driven item definition covering melee weapons, shields, and consumable potions in one |
| Agnostic | combat stats and damage | Kinetic Impact Damage | Physics-driven impact damage: computes a damage value from a collision's relative velocity and |
| Agnostic | combat weapons | Melee Weapon Auto Aim | A thrust-attack melee weapon with a 4-state FSM (IDLE → ATTACKING → PIERCING → RETURNING): |
| Agnostic | minigames and rules | Bouncing Cursor Timing Minigame | A classic "golf swing" / QTE timing minigame: a cursor bounces back and forth across a bar, and |
| Agnostic | minigames and rules | Cascade Sequence Resolver | Given a set of nodes where triggering one can cascade a chain of others in sequence (e.g. "hit A, |
| Agnostic | minigames and rules | Combo Rule Engine | A data-driven combo/synergy system for slot-based layouts (deckbuilders, idle games, tower |
| Agnostic | minigames and rules | Gesture Pattern Recorder | A "draw a rune" input mechanic: N dots arranged in a circle, click-drag between two dots to draw |
| Agnostic | minigames and rules | Number Abbreviator | Formats large numbers into abbreviated, readable strings for score/currency displays — e.g. |
| Agnostic | minigames and rules | Prime Math | A single static utility: `PrimeMath.is_prime(value)` evaluates whether an integer is prime using |
| Agnostic | movement flight | Hover Flight Controller | Camera-relative hover/flight movement for a `CharacterBody3D`: horizontal motion accelerates |
| Agnostic | movement general | Drag To Move | Click-and-drag component for any `Node2D`: click its hitbox to pick it up, and it follows the |
| Agnostic | movement general | Drift Slip Physics | A physics-driven "drift along a spline" system for an orb (or vehicle) racing along a `Path2D`: |
| Agnostic | movement general | Mouse Capture Toggle | Captures the mouse cursor on scene start, releases it when the player presses a release key |
| Agnostic | movement general | Movement State Machine | A highly decoupled, game-agnostic first-person movement core based on a hierarchical state machine. Designed to be completely disconnected from inputs, weapon mechanics, or specific player nodes. |
| Agnostic | movement general | Physics Object Picker | Click-and-drag for `RigidBody2D` objects: click anywhere on a body to freeze it and start |
| Agnostic | movement general | Rolling Sphere Controller | Rolls a spherical `RigidBody3D` by applying torque derived from the cross product of "up" and |
| Agnostic | movement general | Shared Cooldown Sfx | A rate-limited SFX player where the cooldowns are SHARED across every instance of this component |
| Agnostic | movement general | Throttle Coast Controller | A binary-throttle speed controller with an arcade "coast" feel: holding the throttle action |
| Agnostic | movement tethering | Tether Swing Physics | A complete grapple/whip-swing physics system — think a Just Cause grapple or a Metroid-style |
| Agnostic | procgen layouts | Grid Snapped Radius Spawner | Spawns enemies at a randomized angle/distance around a player, snapped to a world grid so |
| Agnostic | procgen layouts | Layout Position Generator Family | A strategy-pattern toolkit for "arrange N items around/along a path": `LayoutPositionGenerator` |
| Agnostic | procgen layouts | Weighted Grid Picker | Two static utilities for "scratch ticket" / slot-machine style reveal grids: `pick_weighted()` |
| Agnostic | procgen spawning | Debris Burst Spawner | Two-file system: `DebrisBurstSpawner` spawns a fan of `RigidBody2D` debris fragments radiating |
| Agnostic | procgen spawning | Pooled Particle Burst | Round-robins through a set of pre-instantiated `CPUParticles2D` children instead of instantiating |
| Agnostic | shaders | Godotshaderbible | ![][image1] |
| Agnostic | shaders | Readme | This directory acts as the central reference repository for writing and generating shaders in Godot 4.x. It contains the complete text of **The Godot Shaders Bible** (Version 0.1.2e). |
| Agnostic | vfx explosions | Impact Burst | A generic visual effect scene for hit feedback. |
| Agnostic | vfx general | Chase Knockback Enemy | A simple melee chaser: once `activated`, walks straight at the player, applies gravity, and |
| Agnostic | vfx general | Wavy Bezier Tether Line | Draws an animated quadratic-Bezier `Line2D` between three `Marker2D`s (start, control, end) with |
