# Remove System

An on-demand playbook for retiring an entire mechanic/system from a project — deciding "we're
done with this system, take it out," not a bug fix (which patches) or a rename/move (see
`markdowns4AI/ORGANIZE.md`). Invocable two ways: standalone, any time the user asks to remove or retire a
system; or as a queued task when the Architect Agent scopes a task as a removal rather than a
build/fix (see `ARCHITECT.md` Phase 4).

## Process

1. **Scope identification.** Identify every file the system touches, not just its "main"
   script(s): scenes, autoload entries, project settings (input map actions, layers), its test
   file(s) under `tests/`, its `project-state/[system]/[system].md` and
   `bugs/[system]/[system].md`, its rows in `project-state/tweak_guide.md`, and its entry in
   `project-state/_overview.md`'s Script Registry. Also grep the rest of the codebase for
   references to the system's `class_name`(s)/autoload name(s) — a removal that leaves a
   dangling reference in an unrelated file is worse than leaving the system in place.
2. **Mandatory dry-run diff.** Before touching anything, produce a full listing of everything
   removal will change (files/scenes to delete-and-archive, autoload entries to remove, doc
   sections to update, tweak_guide rows to remove, any cross-references found in step 1) and
   present it to the user for explicit approval — never proceed straight to deletion. This
   mirrors `markdowns4AI/ORGANIZE.md`'s approval gate, scaled up for a harder-to-reverse action.
3. **Archive, never destroy.** Once approved:
   - Move the system's scripts/scenes to `project-state/archived_systems/[system]/[timestamp]/`
     (timestamp in `YYYY-MM-DD_HHMMSS` format) via Godot MCP file operations (`rename_file` to relocate within the project; `read_file` + `write_file` + `delete_file` if a true move is needed) — never raw shell
     `mv`/`rm`, per `EXECUTOR.md`'s resource-operation rule. Git history already preserves everything, but a
     local archive folder makes "what did this used to look like" discoverable without digging
     through `git log`.
   - Move `project-state/[system]/[system].md`, `bugs/[system]/[system].md`, and the system's
     test file(s) into the same archive folder rather than deleting them.
   - Remove the system's rows from `project-state/tweak_guide.md` and its entry from
     `project-state/_overview.md`'s Script Registry, and log the removal — what was removed,
     when, and where it's archived — in `_overview.md`'s "Organization Notes" section (the same
     section `markdowns4AI/ORGANIZE.md` uses for declined proposals).
4. **Reinstatement path.** Because everything is archived rather than deleted, restoring a
   removed system is: copy the archived files back via Godot MCP, re-add the Script
   Registry/tweak_guide rows, and treat it as a normal existing-codebase re-audit (Tier 2 per
   `SETUP.md` Step 3b) rather than starting from scratch. This is best-effort, not a guarantee —
   if other systems evolved significantly since removal, the reinstated system may need real
   rework to integrate cleanly again, not just a copy-back.
5. **Documentation consistency, same as any task.** Same as `EXECUTOR.md`'s task-completion step: update
   `_overview.md`, `bugs/_overview.md`, the project root `README.md`, and any `design_docs/*.md`
   that documented the now-removed system.
