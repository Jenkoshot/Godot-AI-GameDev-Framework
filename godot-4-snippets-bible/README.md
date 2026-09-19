# AI Directory Guide: godot-4-snippets-bible

This directory acts as the central source of truth for Godot 4.x syntax and API nuances, preventing AI agents (Claude, Gemini) from hallucinating deprecated Godot 3.x syntax.

## Contents
- `godot_4_snippets.md`: A foundational reference of Godot 4 API changes and the project's living record of corrected syntax errors.

## Agent Directives
1. **Always Check Here First:** When writing complex Godot 4 logic, physics math, tweening, or navigation code, you MUST consult `godot_4_snippets.md` before generating code.
2. **Log Corrections:** If the user corrects a syntax hallucination or informs you of a Godot 4 specific change, you MUST log the correct syntax in `godot_4_snippets.md`. This ensures you never make the same mistake twice.
