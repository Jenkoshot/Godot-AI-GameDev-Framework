# Claude Project Organization Review

An on-demand utility for reviewing and improving file/folder naming and structure. Invocable
two ways: standalone, any time the user asks for a cleanup pass; or offered once during
`SETUP.md`'s initial bootstrap run.

## Process

1. **Survey & Re-evaluate** current file/folder naming and structure against Godot conventions (consistent casing, folder-per-responsibility) and the game's evolving `design_docs/`. Also gather any stray AI markdowns (like `DOCTRINE.md`, `ASSET-STANDARDS.md`) at the root and cleanly move them into a `markdowns4AI/` folder. Actively evaluate if the project has outgrown its current structure and if new root folders or nested subdirectories need to be created to better compartmentalize new features or systems.
2. **Propose** specific new folder creations, file moves, and renames as a numbered list, each with a one-line reason. Never execute anything unprompted. If proposing to move markdowns to `markdowns4AI/`, explicitly state that you will also update `GEMINI.md` and `CLAUDE.md` so their internal path references point to the new folder.
3. **Approval gate.** Wait for explicit user approval — per item or as a batch.
4. **Execution.** Route every move/rename of a Godot-tracked resource (`.gd`, `.tscn`,
   `.tres`) through Godot MCP file operations (e.g., `mcp__godot__rename_file`) — never raw
   shell `mv`/`rm`. Raw filesystem operations can silently break UID-based or path-based
   resource references the engine tracks internally.
5. **Decline handling.** Any declined proposal is logged into `project-state/_overview.md`'s
   "Organization Notes" section — what was proposed, when, and that it was declined — so it
   is never auto-resurfaced. The user can still request a fresh review manually at any time.
