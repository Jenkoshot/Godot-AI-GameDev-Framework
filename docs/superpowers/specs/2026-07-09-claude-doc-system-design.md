# Claude Documentation System for Godot Game Projects

**Date:** 2026-07-09
**Status:** Approved design, pending implementation plan
**Test case:** Spinner (`/home/avery/Godot_Projects/Spinner`)

## Purpose

A reusable documentation system that lets Claude work effectively across many Godot game
projects without re-deriving context every session, without ingesting entire codebases to
answer simple questions, and without letting project documentation silently drift out of
sync with the actual code or the actual design intent.

The system is split into two categories:

- **Agnostic documents** — written once, reused unchanged (or nearly unchanged) across every
  game project. Define workflow, not game content.
- **Project-specific documents** — living state for one specific game. Grow and change as
  that game grows.

## Document Inventory

| Document | Category | Cardinality | Purpose |
|---|---|---|---|
| `CLAUDE.md` | Agnostic | One per project (same content) | Baseline workflow Claude follows in any game project |
| `SETUP.md` | Agnostic | One per project (same content) | Bootstraps a new or existing project into this system |
| `ORGANIZE.md` | Agnostic | One per project (same content) | On-demand file/folder reorganization utility |
| `MCP-SWITCH.md` | Agnostic | One per project (same content) | Migrates CLAUDE.md's tool references to a different Godot MCP server |
| `project-state.md` | Project-specific | One master per project | Hub: overall status, script registry, drift/sync flags |
| `project-state-[system].md` | Project-specific | One per identified system | Spoke: detailed map of one game system |
| `bugs.md` | Project-specific | One master per project | Hub: open bug counts by system, recently fixed |
| `bugs-[system].md` | Project-specific | One per identified system | Spoke: detailed bug list for one game system |

---

## CLAUDE.md — Baseline Workflow (Agnostic)

Applies to every game project. Content is stable across projects; only the MCP tool
references (see MCP-SWITCH.md) vary if a project uses a different Godot MCP server than
the current default.

### Principles

**Composition & reusability first.** Systems, scripts, and scenes should be composable and
configurable rather than tightly coupled to one game's specific content, so they can be
lifted into future projects when they fit. Prefer signal-driven communication, resource-driven
configuration (`.tres` data over hardcoded values), and generic components over game-specific
one-offs.

**Do only what the request needs.** The workflow steps below (checking project-state,
verifying against code, proposing three tasks) are not mandatory ritual for every message —
they apply when Claude judges they're necessary to properly respond to what was asked. A
one-line question about what a function does doesn't need a full context-check pass.

### Workflow (when judged necessary)

1. **Orient cheaply first.** Check `project-state.md`'s "Overall Status" and "Recently
   Updated" sections — a few lines, not a deep read.
2. **Session-start drift check** (only if `HEAD` has moved since the commit hash recorded in
   `project-state.md`'s last-verified marker; otherwise skip entirely):
   - Diff actual script/scene filenames on disk against the Script Registry — flag anything
     unlisted (orphan) and anything listed-but-deleted (dangling entry) in
     `project-state-orphans.md`.
   - Diff each system doc's recorded design-doc source markers against the current commit
     hashes of those files under `design_docs/` — flag any system whose design docs changed
     since last sync in `project-state.md`'s "Design Sync Status" section.
3. **For the specific system being worked on:** read `project-state-[system].md` and
   `bugs-[system].md`. If what they describe doesn't match the actual code, update the doc
   first, then proceed with the task.
4. **Inspect the running game** (screenshot, run, test input) when necessary to confirm actual
   behavior — code existing is not the same as a feature working.
5. **Propose three focused tasks** with trade-offs and a recommendation, when the request
   calls for planning next steps rather than a specific fix.
6. **After the user's request is fully satisfied** (not after every individual edit): update
   the relevant `project-state-[system].md` and `bugs-[system].md`, then update the master
   `project-state.md` and `bugs.md` to reflect it. Advance the last-verified commit hash
   marker.
7. **Create new system docs on demand** — when work touches a system with no existing
   `project-state-[system].md`/`bugs-[system].md`, create both at that point (not
   preemptively), and register it in the master docs.

### Implementation status is tri-state, not binary

Every feature/system tracked in a `project-state-[system].md` gets one of three statuses,
never a flat "implemented/not implemented":

- **Coded** — the script/logic exists.
- **Wired-in** — it's actually called/connected from the systems that should invoke it.
- **Verified-in-game** — observed working correctly in a running instance of the game.

This distinction exists because Spinner's own history has already produced the failure mode
it prevents: SynergyEngine, JuicedPathTraveler, and CascadeRouter were all fully coded but
never wired into gameplay, and a plain "implemented" status would have reported them as done.

### Industry practices to default to (Godot-specific)

- Signal-driven communication between systems, not direct cross-references
- Composition over inheritance
- Autoload managers for cross-system state, not scattered singletons
- Resource-driven configuration (`.tres`) over hardcoded values
- Scene composition via reusable subscenes over monolithic scenes
- Use the engine's own class reference (`godot --headless --doctool <dir>`) or live
  `ClassDB` reflection via the MCP when unsure of an API — don't guess from training data,
  which may not match the installed engine version

---

## SETUP.md — Bootstrap (Agnostic)

Run once per project. Idempotent: if `CLAUDE.md`, `project-state.md`, and `bugs.md` all
already exist, it does nothing.

### Step 1 — Existence check

If all three files exist, stop. Setup is already complete.

### Step 2 — Scope detection

Scan the project for existing game code beyond boilerplate. Auto-detect **new project** vs.
**existing codebase**, state the assumption to the user, and let them correct it before
proceeding.

### Step 3a — New project path

- Write `CLAUDE.md` from the canonical template above.
- Write empty `project-state.md` and `bugs.md` masters (empty Script Registry, empty
  sections).
- If a `design_docs/`-equivalent folder exists despite no code yet, seed "Missing/Gap
  Systems" from it.

### Step 3b — Existing codebase path (tiered audit)

**Tier 1 (always, cheap):** Structural scan — enumerate script/scene files, grep for
`signal`/`func`/`class_name`/`extends`. Build the complete Script Registry. Group scripts
into system boundaries using judgment — informed by `design_docs/` categories, folder
structure, or autoload managers, whichever fits this particular project. No fixed rule.

**Tier 2 (selective, deep):** For systems judged architecturally significant (autoloads,
anything with a matching detailed design doc, anything central to the core loop), do a full
read and produce a real `project-state-[system].md` with signal flow and integration detail.
Everything else gets a stub (registry entry + "not yet audited in depth").

For Spinner specifically: seed Tier 2 content for already-audited systems (Kinematic Engine,
Synergy System, Grid Manager, Traveling Text, Cascade Router, Tether Network, Upgrade
persistence) from the existing Aug 2026 codebase audit already in memory, rather than
re-reading those systems from scratch.

Prompt the user once: "Would you like a project organization review too?" If yes, invoke
`ORGANIZE.md`. If no, log the decline in `project-state.md`'s Organization Notes section so
it is never auto-suggested again (the user can still request it manually anytime).

### Step 4 — Write remaining templates

Write `project-state-[system].md` / `bugs-[system].md` shells only for systems identified in
Step 3 — not preemptively for hypothetical future systems.

### Step 5 — Hand off

Report what was created or found. All future sessions defer to CLAUDE.md's normal workflow.

---

## ORGANIZE.md — Reorganization Utility (Agnostic)

Invocable two ways: standalone/on-demand at any time, or offered once during SETUP.md's
initial run.

- **Survey:** current file/folder naming and structure against Godot and general project
  conventions.
- **Propose:** specific renames/moves as a numbered list with reasoning. Never executed
  unprompted.
- **Approval gate:** wait for explicit approval, per-item or as a batch.
- **Execution:** all moves/renames go through Godot MCP file operations (e.g.,
  `mcp__godot__rename_file`), never raw shell `mv`/`rm` — raw filesystem operations can break
  UID-based or path-based resource references that the engine tracks.
- **Decline handling:** any declined proposal is logged in `project-state.md`'s Organization
  Notes section (what was proposed, when declined) so it is never auto-resurfaced. The user
  can still request a fresh pass manually.

---

## MCP-SWITCH.md — MCP Migration Utility (Agnostic)

Invoked only when a project adopts a different Godot MCP server than the current default.

1. Scan `CLAUDE.md` for all `mcp__<server>__<action>` tool references.
2. Load the new MCP server's tool list/schema.
3. Map each old capability to its nearest equivalent in the new server.
4. Rewrite `CLAUDE.md`'s tool references in place — workflow structure and principles are
   untouched.
5. Flag any capability with no equivalent in the new server, so it's a visible gap rather
   than a silent loss.

---

## project-state.md — Master Hub (Project-Specific)

### Sections

- **Overall Status** — one-sentence project health summary.
- **Implemented Systems** — table: system name, tri-state rollup, link to detail doc.
- **Missing/Gap Systems** — table: what's planned but not started, linked to design docs if
  available.
- **Critical Blockers** — anything blocking forward progress.
- **Recently Updated** — last 3-5 systems touched, with dates.
- **Script Registry** — every script/scene file: path, primary owning system doc, optional
  secondary system(s) for shared/utility scripts.
- **Design Sync Status** — per system, last-synced design doc commit marker; flagged if the
  current `design_docs/` commit hash has moved since.
- **Organization Notes** — log of `ORGANIZE.md` proposals and their outcomes (approved /
  declined, with date), so declines are never re-asked automatically.
- **Last Verified Commit** — the git hash at which the session-start drift checks were last
  run; gates whether those checks run again.

---

## project-state-[system].md — System Spoke (Project-Specific, Created On-Demand)

### Sections

- **Current Implementation**
  - What's built and how it works, in plain terms.
  - Signal flow: which scripts emit which signals, which listen, what data flows.
  - Script locations and responsibilities.
  - Integration points with other systems.
  - Per-feature status: Coded / Wired-in / Verified-in-game.
- **Gaps vs. Design Docs**
  - What's designed but not implemented, or implemented differently than designed.
- **Known Issues & Workarounds**
  - Technical debt or temporary hacks specific to this system.
- **Related Systems**
  - Links to other system docs this one depends on or communicates with.
- **Design Doc Sources**
  - Paths under `design_docs/` this doc was built from, and the commit hash at last sync
    (feeds the master's Design Sync Status check).

---

## bugs.md — Master Hub (Project-Specific)

### Sections

- **Open Bugs by System** — table: system, open bug count, link to system bugs doc.
- **Recently Fixed** — last 5-10 fixed bugs, with date and system.
- **Critical/Showstopper Bugs** — anything blocking progress.

---

## bugs-[system].md — System Spoke (Project-Specific, Created On-Demand)

### Sections

- **Open Bugs** — description, repro steps if applicable, related script, priority.
- **Fixed Bugs** — historical log: description, how it was fixed, date fixed. Bugs move here
  from Open Bugs rather than being deleted.

---

## project-state-orphans.md — Drift Holding Pen (Project-Specific, Created On-Demand)

Filename-only listing of files found on disk but not present in any system's Script
Registry entry, from the session-start drift check. No deep analysis performed at detection
time. When a task actually touches an orphaned file, it gets properly analyzed and promoted
into the appropriate `project-state-[system].md` (creating that system doc if it doesn't
exist yet), and removed from this file.

---

## Open Items Deferred to Implementation Planning

- Exact grep/heuristics for Tier 1 structural scan (what counts as a "significant" system for
  Tier 2 promotion).
- Whether `CLAUDE.md`/`SETUP.md`/`ORGANIZE.md`/`MCP-SWITCH.md` templates themselves live in
  this shared `Godot_Projects/docs/` repo for copying into each new game project, or are
  generated fresh by Claude each time from this spec.
- Concrete file format/table syntax for the Script Registry and status tables (this spec
  defines required content, not exact Markdown table shape).
