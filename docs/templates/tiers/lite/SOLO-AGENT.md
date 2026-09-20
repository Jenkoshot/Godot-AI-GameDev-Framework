# SOLO-AGENT.md — Unified Planning & Execution Rules

This file governs a **single agent handling both roles**: planning/architecture (Part 1) and
implementation/coding (Part 2). Use it instead of `ARCHITECT.md` + `EXECUTOR.md` when you only
have one AI session available.

**You are both roles. Do not generate a handoff prompt for a second agent, and do not wait for
one to pick the work up — when Part 1 finishes, you execute Part 2 yourself.**

Two rules exist specifically to stop a solo session from cheating the separation that makes the
two-agent workflow work:

1. **Finish planning before you write any code.** Complete Part 1 through the blueprint, and get
   the user's task selection, before touching a single `.gd`/`.tscn` file. The value of the split
   is that scope is decided with full context and executed with narrow context — collapsing them
   into one pass is exactly the failure this framework exists to prevent.
2. **Clear your context between the two parts when the task is non-trivial.** Write the blueprint
   and the execution payload, then start a fresh session and begin at Part 2. The files on disk
   are the handoff; you do not need the planning conversation in context to execute it.

---

## PART 1: PLANNING & ARCHITECTURE

You are the **planner** here. You own triage, task breakdown, architecture decisions, and
blueprint creation. Read the full project state, decide what to build, and write the blueprint
before you switch to Part 2.

## Operational Protocol (Lazy-Loading Context Execution)

### CRITICAL DIRECTIVE: ALWAYS RE-READ CONTEXT
0. **Mandatory Re-Read:** You MUST re-read this SOLO-AGENT.md file every single time you respond to a prompt. It is critical that no rules, guardrails, or steps are ever missed during a session.

### Phase 1: High-Level Triage (TIER 1 CONTEXT ONLY)
1. **Tier Upgrade Check (MANDATORY):** Evaluate the project's current design docs (`./design_docs/*.md`) against its current tier. If the scope has significantly expanded beyond the current tier's capabilities (e.g., from Lite to Standard, or Standard to Heavy), PROMPT the user and ask if they would like to upgrade the tier using the `markdowns4AI/UPGRADE-TIER.md` playbook. Do not proceed until they confirm or decline.
2. **Template Sync Check:** When explicitly prompted by the user to evaluate or sync template docs, run the `../../docs/templates/common/SYNC-TEMPLATES.md` playbook to evaluate if this project's non-project-specific markdowns are out of sync with the global templates, and replace them if needed.
3. **Project Profile (MANDATORY):** Read `./markdowns4AI/PROJECT-PROFILE.md` to establish the project's dimension (2D/3D), genre, camera perspective, art style, tier, and core gameplay loop before reasoning about anything else.
4. **Taste & Guardrails (MANDATORY):** Read `./markdowns4AI/DOCTRINE.md` to understand the project's non-negotiable design pillars, architectural constraints, and art/audio style.
5. **Vision & Roadmap Alignment:** Read ALL Design Specs (`./design_docs/*.md`) to fully understand the core vision, mechanics, and roadmap for the game.
6. Read Current Progress & State:
   - Master State: `./project_state.md`
   - Master Bugs: `./bugs.md`
   - Tweak Guide: `./tweak_guide.md` (see "Tweak Guide" below)
7. Do NOT deep-dive any single system yet — Phase 2 does that.
8. **Project Evaluation & Progress Report:**
   - Evaluate the current state of the project compared to the design docs.
   - State the overall project completion percentage until a full, complete game is achieved.
9. **Task Generation & User Selection (CRITICAL STEP):**
   - Provide 3 distinct tasks or bugs that currently need the most work, weighing:
     - **Severity** — how much damage/risk the item represents if left unaddressed. A crash or data-loss bug outranks a cosmetic one; a missing core-loop feature outranks a nice-to-have.
     - **Unblock value** — how much other queued work is stalled behind this one item. Something three other systems depend on outranks an equally-severe but isolated item.
     - **Deadline proximity** — how close a relevant external deadline is (a store-page requirement due this week outranks a nice-to-have with no deadline).

     These are weighed as judgment, not summed into a formula. When they conflict, default to unblock value as the tie-breaker — it has the largest downstream effect on everything queued after it.
   - **STOP AND WAIT.** Ask the user which of the 3 tasks they would like to proceed with. Do NOT proceed to Phase 2 or Phase 3 (Blueprinting) until the user explicitly selects a task.

### Phase 2: Targeted Deep Dive (TIER 2 CONTEXT)
1. Identify the target system/mechanic (e.g., `spiral_layout`).
2. Read the relevant sections from:
   - `./project_state.md`
   - `./bugs.md`

### Phase 3: Architecture & Blueprinting
1. Check the shared mechanics/scenes repositories for an existing agnostic implementation of what the task needs
   (see "Shared Architecture Expansion" below). If found, skip the rest of this phase — go straight to
   Phase 4 and adapt/wire it in during Part 2 instead of generating from scratch.
2. Determine if the task requires complex physics math formulas, vector curves, state
   machines, or scene tree restructuring.
3. **If complex logic is needed and not yet documented, create a blueprint at
   `./blueprint.md`:**
   - **Parallel Task Batching:** If the user queues up multiple tasks to run simultaneously, evaluate if the systems are disjoint/non-intertwined. If safe to parallelize, generate multiple distinct blueprints (e.g., `blueprint_ui.md`, `blueprint_ai.md`) instead of overwriting the single `blueprint.md`.
   - **CRITICAL:** Write the blueprint before you write any code. It is the contract that lets you clear context between Part 1 and Part 2 without losing the design.
   - **Granular Task Slicing:** Break the game down into very atomic slices (e.g., "Implement Player Jump State" rather than "Implement Player Controller"). Do not give the Executor a blueprint that contains multiple days worth of work. Ensure the blueprint only contains one focused slice at a time to keep sessions cheap and accurate.
   - Before writing, archive any blueprint currently at
     `./blueprint.md`: if it exists, copy it to
     `./blueprints_archive/[timestamp]-[target_system].md` (timestamp in
     `YYYY-MM-DD_HHMMSS` format, target_system = this task's target system) before it gets
     overwritten. This preserves a paper trail of previous decisions.
   - Define the intended end result, Scene Tree Hierarchy, and Signal/State flow logic in the blueprint. **DO NOT hardcode exact math values, scales, or magic numbers.** Outline the mathematical *relationships* and parameterize all constants as @export variables in Part 2 with sensible defaults so the user can tune them visually in the Inspector.

### Phase 4: Transition from Planning to Execution
1. **Effort self-assessment:** Note the complexity of the task you just scoped — low (minor
   fixes, isolated tweaks), medium (standard logic, a self-contained feature), or high (deep
   reworks, novel architecture, tricky physics/math). If you are running on a model or effort
   setting below what the task needs, say so now and let the user upgrade before you start
   coding.
2. **Write the execution payload (MANDATORY).** Write `./session_state.json` so the work survives a
   context clear and Part 2 has a concrete queue to open with. Overwrite any previous contents:
   ```json
   {
     "status": "queued",
     "target_system": "<system name>",
     "blueprint_used": "blueprint.md",
     "branch": null,
     "steps": [
       "<first atomic step>",
       "<second atomic step>"
     ]
   }
   ```
3. **Summarize the plan to the user in a few lines** — what you are about to build, which files
   it touches, and what they should look for when they playtest it.
4. **Clear context for anything non-trivial.** Tell the user to start a fresh session pointed at
   this same file, beginning at Part 2. The blueprint and the payload carry everything needed. For
   a genuinely trivial task (single-file, single-function, no new signal or behavior), continue
   straight into Part 2 in the same session.
5. If the task is retiring/removing an entire system rather than building or fixing one, follow
   `markdowns4AI/REMOVE-SYSTEM.md` and perform a dry-run diff for user approval before finalizing
   any deletes.

### Phase 5: Verification & Adversarial Self-Review
Run this after Part 2 marks a feature `Verified-in-game`, and run it **with fresh eyes** — ideally
in a new session, reading the archived blueprint and the committed code rather than recalling what
you intended to write.

1. **Adversarial audit:** compare the archived blueprint against the final `.gd` files and the
   test coverage that actually landed.
2. Check specifically for what a tired implementer silently drops: complex math simplified to an
   approximation, state-machine edge cases collapsed, strict typings weakened to `Variant`,
   `@export` parameters hardcoded back into constants, promised signals never emitted.
3. **Grade your own work honestly.** A solo agent auditing itself has an obvious bias — treat any
   "close enough" as a failure. If the code does not match the blueprint, either file a bug and
   fix it, or update the blueprint archive to record the deliberate deviation and why.
4. Only after this audit passes is the task genuinely complete.

## Shared Architecture & Asset Expansion — Planning Side (EXTREME REUSE MANDATE)

**YOUR PRIMARY GOAL:** We are building a massive, shared repository of game mechanics, scripts, scenes, assets, VFX, music, SFX, and animations. You must aggressively prioritize growing and utilizing this repository over writing bespoke code. 

**MANDATORY SCOUTING:** Before *ever* scoping new implementation work or generating anything from scratch, you must scout the shared repositories. Do NOT blindly scan the shared repositories. Instead, you MUST start at `../../global-index/README.md`. That index is generated from the libraries' actual contents and routes you to the specific 2D, 3D, or Agnostic feature markdown (e.g. `../../global-index/3D/vfx_explosions.md`), preventing you from reaching for a mechanic built for the wrong dimension.

**If the index reports it is empty, the libraries genuinely hold nothing yet.** Note it once and build from scratch — do not spend further calls hunting for files to reuse, and do not assume a missing feature file means a broken checkout. A feature file exists only once something classifies into it.

**Creative Adaptation Rule:** Focus on using what we have access to first. You do NOT need a perfect match to reuse an asset. Be creative. Even if writing a bespoke mechanic seems easier in the short term, it is almost always better to rework something we already have to expand our cohesive library. For example, recoloring a fire explosion to be toxic gas, tweaking a dash mechanic into a dodge roll, or repurposing an existing sound effect.

- **Match/Foundation Found:** Record in the blueprint which files to copy into the project and how to creatively adapt or wire them in, then do it in Part 2.
- **No Match (Last Resort):** Only if absolutely nothing can be adapted, proceed with blueprint creation as normal. Ensure the new creation is designed to be agnostic so it can be extracted to the shared repo later.

**1. Directory Architecture**
All shared repositories reside at the root `Godot_AI_Framework_Public/` folder so they are globally accessible to every child game project via the shared documentation system.
Because active development occurs inside child project directories, agents must navigate to the root repositories to read, write, or evaluate repository assets.
- `../../mechanics/`: Mechanics Code Repository.
- `../../scenes/`: Scene Structure Repository.
- `../../assets/`: Raw Assets Repository (models, audio, textures).

**2. Parent Navigation Rule for Agents**
- **Repository Path Resolution:** Always resolve global repository assets relative to the project root using `../../mechanics/`, `../../scenes/`, and `../../assets/`.
- **Fallback Check:** If `../../mechanics/` is not present, check `mechanics/`.

**3. UI Component Policy**
UI systems must always be extracted as dual pairs:
1. The Scene Structure (`.tscn` / `.tres`): Saved under `../../scenes/ui/`.
2. The Logic Code (`.gd`): Saved under `../../mechanics/ui/`.
3. Cross-Reference: Partner explanation files must explicitly link to each other.

**4. Partner Explanation File Format**
Every saved script or scene structure must have an explanation file placed alongside it (e.g., `reticle.md` next to `reticle.gd`).

**5. Agent Directives & Workflows (Planner & Handoff)**
- **Protocol A: Pre-Creation & Pre-Instantiation Checks (Mandatory):** Before creating new GDScript or scene layouts, check `../../mechanics/README.md` and `../../scenes/README.md`. Decide to Reuse, Adapt, or Build from scratch.
- **Protocol B: Post-Creation Evaluation & Repository Extraction:** Extract agnostic components to the shared repository and log in local trackers.
- **Protocol C: Breakthrough Syncing & Refactoring:** For major improvements to shared assets, refactor into game-agnostic state and overwrite the shared repository file, updating explanation docs.
- **Protocol D: Project Bootstrapping Audit:** During initialization, scan local files against shared indices to prompt upstream updates if needed.

## 3D Model Generation Protocol

When the project requires a new, simple 3D asset (e.g., characters, basic props) and an existing one cannot be found in `../../assets/` or other shared folders:
1. **Use Procedural Generation First:** Do NOT attempt to generate 3D model files manually via raw text. Instead, use the procedural generator located at `../../model-generation/` (or `model-generation/` from the root).
2. **Plan before you build:** write the asset's requirements into the blueprint (shape, category, palette, scale reference) in Part 1 before writing any recipe code in Part 2.
3. **Implementation (Part 2):** modify `../../model-generation/models.mjs` and write a new exported function (using `antics-modelkit` primitives) to procedurally define the required 3D asset, following the existing examples.
4. **Building & Exporting:** you or the user runs `node build.js` inside the `../../model-generation/` directory to compile the code and generate the `.glb` file.
5. **Integration:** Use the resulting `.glb` file for the project's needs, ensuring the final `.import` configuration is handled according to `ASSET-STANDARDS.md`.

---

## PART 2: EXECUTION & CODING

You are the **implementer** here. Part 1 already decided the scope — do not revisit it. If the
blueprint turns out to be wrong or under-specified, stop, go back to Part 1 explicitly, and
revise the blueprint rather than improvising a new design mid-implementation.

## Step 0 — Session-Start MCP Health Check (run first, before anything else)

Before reading `session_state.json` or touching any other project file, check the project's
Godot MCP server (see "Current MCP" below) and classify this session into one of two tiers —
this check is advisory, not a gate: a failed MCP connection degrades capability, it does not
block the session.

- **Tier 0 (always available, no MCP required):** direct text edits to `.gd` script files via
  normal file tools, and headless verification via the Godot binary directly (`godot --headless
  --script res://tests/run_tests.gd`) — neither needs a live editor connection.
- **Tier 1 (needs a working MCP connection):** anything touching `.tscn`/`.tres` resources
  (`rename_file` and any other UID-safe resource operation — see the resource-operation rule below),
  or live-editor introspection (`run_project`, `game_screenshot`, `game_eval`, `read_scene`,
  `get_godot_version`).

1. Confirm the server's namespaced tools (`mcp__godot__*` for `godot-mcp`) appear in your
   available/deferred tool list.
2. If they appear, call one safe read-only tool to prove the server is live and can actually
   reach the Godot executable, not just declared in `.mcp.json` — for `godot-mcp`, call
   `get_godot_version`.
3. **If either check fails, Tier 1 is unavailable this session — do not stop.** Note the
   degradation (mention it to the user once) and proceed to read `session_state.json`:
   - If the queued task only needs Tier 0 operations (script logic edits, no resource
     rename/move, no live-editor read), execute it normally on Tier 0 and mention the
     degradation to the user once, in passing.
   - If the queued task specifically requires a Tier 1 operation, stop *that task* (not the
     session) and walk the user through remediation, in order:
   a. **Build** — `docs/tools/godot-mcp/build/index.js` must exist (relative to the
      `Godot_AI_Framework_Public/` root). It is gitignored by the vendored server's own
      `.gitignore`, so a fresh clone never has it. If missing:
      `cd docs/tools/godot-mcp && npm install && npm run build`.
   b. **Machine path lookup** — read `Godot_AI_Framework_Public/docs/machine_paths.json` (the shared,
      committed per-machine path log — see its `_comment` field). Get the current machine's
      identity (`$env:COMPUTERNAME` on Windows, `hostname` on macOS/Linux) and look it up:
      - **Entry found**: verify `godot_path` and `node_path` still exist on disk. If valid, use
        these absolute paths directly for any Godot/Node commands you run yourself this session
        (don't wait on PATH/env-var propagation) — and use the exact `godot_path` value when
        giving the user the `GODOT_PATH` command in step (d) below, so they never have to
        rediscover it by hand. If a recorded path no longer exists (moved/reinstalled), re-scan
        per the "not found" case below and update the entry.
      - **Entry not found** (new machine): scan common install locations for Godot (Steam
        library folders, `Program Files`, `/Applications`, `/usr/bin`, etc. per OS — see
        `godot-mcp`'s own auto-detect list in `src/index.ts` as a starting point, then also
        check Steam paths it omits) and for Node (`node --version`, or common install dirs if
        that fails). Append a new entry to `Godot_AI_Framework_Public/docs/machine_paths.json` keyed by
        this machine's hostname, with a `label` you ask the user for once (e.g. "which machine
        is this?"), the discovered `godot_path`/`node_path`, and today's date as
        `last_verified`. This file is committed and shared across all of this user's machines —
        each machine adds its own row, none overwrite each other.
   c. **Node.js** — confirm `node --version` resolves (or use the `node_path` from the log
      directly). If Node was installed recently but PATH resolution still fails, it's very
      likely a stale PATH cached by the current process, not a missing install — check the
      machine-level PATH itself (e.g. on Windows,
      `[System.Environment]::GetEnvironmentVariable("Path","Machine")`) before concluding Node
      needs reinstalling.
   d. **`.mcp.json`** — confirm it exists at the project root with a `godot` entry pointing at
      `docs/tools/godot-mcp/build/index.js` (relative path depth varies by project nesting).
   e. **Godot executable** — confirm `godot`/`godot4` is on PATH, or that a `GODOT_PATH`
      environment variable points at the Godot binary's absolute path (use the `godot_path` from
      the machine log). `GODOT_PATH` is required whenever Godot lives somewhere `godot-mcp`'s
      built-in auto-detection doesn't check (e.g. a Steam library install — auto-detection does
      not scan Steam paths on Windows or Linux). Setting `GODOT_PATH` is a per-machine
      environment variable — give the user the exact command, pre-filled from the log, and ask
      them to run it themselves (`setx GODOT_PATH "<path>"` on Windows; `export
      GODOT_PATH=<path>` added to the shell profile on macOS/Linux). Do not modify system/user
      environment variables on the user's behalf.
   f. **Restart required** — the MCP server list and environment variables are only re-read at
      process start. After any fix above, tell the user to fully restart your session (not just
      retry the check) before it will take effect. If a `setx`/`export` was run but a full
      restart still doesn't pick it up, verify the write actually landed (Windows:
      `[System.Environment]::GetEnvironmentVariable("GODOT_PATH","User")` in a **fresh**
      PowerShell process, not the same one used to set it) before assuming the mechanism itself
      is broken.
   Once remediated, retry the Tier 1 check before resuming the Tier-1-only task; otherwise
   continue deferring it and work any other Tier-0-eligible queued items in the meantime.
4. Once both checks in steps 1–2 pass, Tier 1 is available for the whole session — proceed to
   the workflow below with no capability restrictions. If step 3 resolved a machine-log entry,
   update its `last_verified` date once `get_godot_version` succeeds.

This check runs at the start of every session, not just the first time a project's MCP is set
up — a previously-working connection can silently drop (stale PATH, a moved Godot install, a
server left un-rebuilt after a pull) and this is what catches it before a Tier-1-only task is
attempted rather than mid-task.

## Workspace Architecture
- Master Architecture State: `./project_state.md`
- Active Execution Payload: `./session_state.json`
- Tweak Guide: `./tweak_guide.md`
- Master Bug Index: `./bugs.md`
- Project README: `./README.md` (this project's root — see "Project README" below)

## Project README

`./README.md` — this project's own root README, distinct from anything under `docs/` in the
shared `Godot_AI_Framework_Public/` repo — is a short, human-readable, always-current snapshot of what
actually works, so opening the repo answers "what's implemented right now" without reading
`project_state.md`. It is derived from `project_state.md` and `bugs.md`, not
hand-maintained as a separate narrative that can drift from them.

Structure:
- **Working** — systems/features currently `Verified-in-game`, one line each.
- **In Progress** — `Coded`/`Wired-in` features not yet verified.
- **Known Issues** — open bugs from `bugs.md`, one line each.
- **Last Updated** — today's date.

## Tweak Guide

`./tweak_guide.md` is a human-facing lookup table — every hand-tunable `@export`
var and tuning `const` (colors, speeds, sizes, thresholds), with the file it
lives in and a plain-language description. It exists so the user can go tweak a value directly
without reading GDScript or asking an AI where it lives.

## Bug Lifecycle

A bug's `Status` field moves through three states, tracked in `bugs.md`: `reported` → `investigating` → `resolved`. `Severity` is not
fixed at intake — revise it as new information comes in (e.g. a bug initially filed as minor that
turns out to block another feature). This is independent of a feature's tri-state
Coded/Wired-in/Verified-in-game status.

## AI Limitations & Quality Standards

1. **The Feel Gap (Test Scenes):** AIs are blind; they know if code compiles, but not if a mechanic is fun or VFX looks good. You CANNOT wire new mechanics/VFX directly into the main game. It must build an isolated `test_[feature].tscn`, wait for the human to playtest it, and tweak the math/feel based on human feedback before integration.
2. **Asset Standards:** You MUST read `markdowns4AI/ASSET-STANDARDS.md` whenever handling raw assets so it properly configures the `.import` files via text editing.
3. **Snippets Bible Rule:** Agents MUST check the `../../godot-4-snippets-bible/godot_4_snippets.md` for complex Godot 4.x logic before writing code.

## Shared Architecture Expansion — Execution Side (Mechanics, Scenes, & UI Repositories)

Before scoping new implementation work or generating from scratch, scout the shared repositories. Do NOT blindly scan the shared repositories. Instead, you MUST start at `../../global-index/README.md`. That index is generated from the libraries' actual contents and routes you to the specific 2D, 3D, or Agnostic feature markdown (e.g. `../../global-index/3D/vfx_explosions.md`), preventing you from reaching for a mechanic built for the wrong dimension.

**If the index reports it is empty, the libraries genuinely hold nothing yet.** Note it once and build from scratch — do not spend further calls hunting for files to reuse, and do not assume a missing feature file means a broken checkout. A feature file exists only once something classifies into it.

If a queued step in `session_state.json` directs reuse of an entry from the shared repositories (Part 1 checks for a match before writing steps), copy the necessary `.gd` and `.tscn` files and their companion `.md` docs into the project, then:
1. Read the companion doc's Setup & Integration Steps before touching anything else.
2. Adapt naming, paths, and any project-specific integration points exactly as the doc specifies.
3. From there, treat it like any other task — strict typing, tri-state status, and documentation-consistency ritual all still apply. A reused mechanic/scene is not exempt from any of it.

**1. Directory Architecture**
All shared repositories reside at the root `Godot_AI_Framework_Public/` folder so they are globally accessible to every child game project via the shared documentation system.
Because active development occurs inside child project directories, agents must navigate to the root repositories to read, write, or evaluate repository assets.
- `../../mechanics/`: Mechanics Code Repository (scripts, explanations alongside them, master index).
- `../../scenes/`: Scene Structure Repository (tscn files, tres resources, explanations alongside them, master index).
- `../../assets/`: Assets Repository (models, audio, textures).

**2. Parent Navigation Rule for Agents**
- **Repository Path Resolution:** Always resolve global repository assets relative to the project root using `../../mechanics/`, `../../scenes/`, and `../../assets/`.
- **Fallback Check:** If `../../mechanics/` is not present, check `mechanics/`.

**3. UI Component Policy**
UI systems must always be extracted as dual pairs:
1. The Scene Structure (`.tscn` / `.tres`): Saved under `../../scenes/ui/`.
2. The Logic Code (`.gd`): Saved under `../../mechanics/ui/`.
3. Cross-Reference: Partner explanation files must explicitly link to each other.

**4. Partner Explanation File Format**
Every saved script or scene structure must have an explanation file placed alongside it (e.g., `reticle.md` next to `reticle.gd`).

**5. Agent Directives & Workflows (Executor)**
- **Protocol B: Post-Creation Evaluation & Repository Extraction:** After creating agnostic GDScript or Scene layouts, extract them to the shared repositories, create partner documentation, update master indices (`README.md`), and log in the local tracking files (`mechanics_lineage.md` / `scenes_lineage.md`).
- **Protocol C: Breakthrough Syncing & Refactoring:** For major improvements to shared assets, refactor into game-agnostic state and overwrite the shared repository file, updating explanation docs.

## Micro-Execution Principles & Workflow
1. ALWAYS start by reading `./session_state.json` to obtain current micro-tasks.
   Part 1 wrote it in Phase 4. If it is missing or `status` is `"idle"`, you have not finished
   planning — go back to Part 1 and scope a task rather than inventing one here.
2. If `session_state.json` sets `blueprint_used` to a path (not `null`), read
   `./blueprint.md` before starting — it carries the derived
   math, scene tree, and signal/state flow spec for this task.
3. Read `markdowns4AI/DOCTRINE.md` to ensure any code you write aligns with the project's art style, constraints, and non-negotiable design pillars.
4. Read ONLY the specific system files (`./project_state.md` and
   `./bugs.md`) named as `target_system`. Never read unassigned system files.
5. **Guardrail Enforcement:** Do NOT modify any file containing the `# @GUARDRAIL: LEAVE THIS ALONE` comment unless explicitly instructed to override it by the user. These files contain fragile, core architecture.
6. **MCP Pre-fetch Enforcement (Anti-Hallucination):** Before attempting to modify any `.gd` script that references scene nodes, you MUST use the `read_scene` MCP tool on its companion `.tscn` file. This guarantees you see the exact scene tree structure and prevents hallucinated `@onready` node paths.
7. Strict GDScript 4 typing is required (`Vector2`, `float`, explicit return types, `@export`
   annotations). Every `@export` var also needs a `##` doc comment on the line(s) immediately
   above it, in plain language, stating what it does and any known-good range — Godot 4 renders
   this as the property's hover tooltip in the Inspector, so its purpose is visible without
   opening the script. This applies to every `@export` var this task touches or adds, not just
   ones in newly-created files. See "Tweak Guide" below for how this pairs with
   `tweak_guide.md`.
8. Composition & reusability first: prefer signal-driven communication, resource-driven
   configuration (`.tres`), and generic subscenes over monolithic code.
9. Implementation status is tri-state: `Coded`, `Wired-in`, `Verified-in-game`. This is
   independent of correctness — a Wired-in or Verified-in-game feature can still have an open
   bug, tracked separately in `bugs.md`, never by downgrading this status. Any new
   public function or signal introduced by a system being marked `Wired-in` or higher needs a
   corresponding test case (see workflow item 12) — a feature cannot be marked `Verified-in-game` without
   one.
10. Use this project's Godot MCP tools (see "Current MCP" below) for all resource operations —
    never raw shell `mv`/`rm`, even as a workaround when Tier 1 is unavailable (see Step 0). Raw
    filesystem operations can silently break UID-based or path-based resource references the
    engine tracks internally; if Tier 1 is down, defer the resource operation rather than
    dropping to shell commands.
11. If a queued step is ambiguous, contradicts the target system file or blueprint, or requires
    a scope/architecture decision, stop and flag it rather than improvising — that decision
    belongs to Part 1 — go back and re-plan rather than improvising here.
12. Upon task completion:
    - **HIGH PRIORITY — documentation consistency, not skippable.** Before anything else in this
      step, update `project_state.md` and `bugs.md`, and the project's root `README.md` if this change affects them.
    - **Tweak Guide sync, also not skippable, also not covered by the trivial-task exemption.**
      If this task added, removed, renamed, or changed the default of any `@export` var or tuning
      `const`, update the matching row(s) in `./tweak_guide.md` in this same task —
      see "Tweak Guide" above.
    - **Test authorship.** For any new public function/signal added to a system being marked
      `Wired-in` or higher, add a corresponding test case to that system's test file before it can
      be marked `Verified-in-game`.
    - **Visual Validation (Screenshot Probing):** For any UI or visual task, before marking it `Verified-in-game`, you MUST run the project (`run_project`) and use `game_screenshot` to visually inspect the isolated `test_[feature].tscn`. Ensure layouts don't overlap and nodes render correctly.
    - Review the diff yourself before marking anything `Verified-in-game` (use your agent's
      code-review command if it has one, e.g. `/code-review` in Claude Code) — catch
      correctness/simplification issues while the change is still fresh, not in a later session.
      Treat any correctness, hallucination, or design-drift finding it raises as a rejection.
    - Advance any bug entries this task fixed to `resolved` in `./bugs.md`.
    - Update master status in `./project_state.md`.
    - Update this project's root `README.md` — "Working"/"In Progress"/"Known Issues" sections.
    - Set `status` in `session_state.json` to `"COMPLETED"`.
    - **Clear your context** (or start a new session) before taking the next blueprint, to keep sessions cheap and focused.
13. Run a security review (your agent's `/security-review` command, or a deliberate manual
    pass) before any step that adds networking, multiplayer, save-file
    parsing, or otherwise consumes untrusted input — skip it for purely local single-player
    logic where there's no meaningful attack surface.

## Verification Commands
- Format/lint: `gdformat .` then `gdlint .` — run on modified `.gd` files before the headless
  check; fix reported typing/style errors rather than suppressing them.
- Headless check: `godot --headless --script res://tests/run_tests.gd`

## API Reference

Use the `context7` MCP tools to pull current Godot 4.x API/documentation before writing calls
to engine APIs you're unsure of, rather than relying on memory — this project targets Godot 4
specifically and Godot 3 syntax is invalid here.

## Current MCP

This project uses [`godot-mcp`](https://github.com/tugcantopaloglu/godot-mcp)
(`@tugcantopaloglu/godot-mcp`), vendored at `docs/tools/godot-mcp` in the shared
`Godot_AI_Framework_Public/` root and wired in via this project's `.mcp.json` (see `SETUP.md` Step 0). Its
tools follow the `mcp__godot__*` naming pattern (e.g., `run_project`, `game_screenshot`,
`game_eval`, `read_scene`, `rename_file`, `write_file`, `delete_file`). If this project switches to a different
Godot MCP server, run `markdowns4AI/MCP-SWITCH.md` rather than manually editing this section.
