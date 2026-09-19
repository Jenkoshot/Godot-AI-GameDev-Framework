# Godot 4 Snippets Bible

This document is a foundational explanation of Godot 4 API changes and a living record of corrected syntax.

## Core API Changes (Godot 3.x -> 4.x)
- `move_and_slide()`: In Godot 4, `move_and_slide()` no longer takes arguments (like velocity or up direction). You set `velocity`, `up_direction`, etc., directly on the `CharacterBody2D/3D` and then simply call `move_and_slide()`.
- **Tweens:** The Godot 3.x `Tween` node has been largely replaced by the `SceneTreeTween` created via `create_tween()`. E.g., `var tween = create_tween(); tween.tween_property(self, "position", Vector2(100, 100), 1.0)`.
- **Navigation:** Navigation has moved from `Navigation` nodes to `NavigationServer2D` and `NavigationServer3D`. Use the server directly or the newer `NavigationAgent2D/3D` properties for pathfinding.

## Log of Corrected Syntax
*(Agents: Whenever the user corrects a syntax hallucination, append the correct Godot 4 syntax below, formatting it clearly with examples.)*

