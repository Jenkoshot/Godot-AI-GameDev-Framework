# Remove System

An on-demand playbook for retiring an entire mechanic/system from a project — deciding "we're
done with this system, take it out," not a bug fix (which patches) or a rename/move (see
`markdowns4AI/ORGANIZE.md`). Invocable two ways: standalone, any time the user asks to remove or retire a
system; or as a queued task when Gemini/Antigravity scopes a task as a removal rather than a
build/fix (see `GEMINI.md` Phase 4).

## Process

1. **Scope identification.** Identify every file the system touches, not just its "main"
   script(s): scenes, autoload entries, project settings (input map actions, layers), its test
   file(s) under `tests/`. Also grep the rest of the codebase for
   references to the system's `class_name`(s)/autoload name(s) — a removal that leaves a
   dangling reference in an unrelated file is worse than leaving the system in place.
2. **Mandatory dry-run diff.** Before touching anything, produce a full listing of everything
   removal will change (files/scenes to delete, autoload entries to remove, doc
   sections to update, tweak_guide rows to remove, any cross-references found in step 1) and
   present it to the user for explicit approval — never proceed straight to deletion.
3. **Delete.** Once approved:
   - Delete the system's scripts/scenes via Godot MCP file operations.
   - Remove the system's sections/entries from `project_state.md`, `bugs.md`, and `tweak_guide.md`.
4. **Documentation consistency, same as any task.** Same as `CLAUDE.md` step 9: update
   the project root `README.md`, and any `design_docs/*.md` that documented the now-removed system.
