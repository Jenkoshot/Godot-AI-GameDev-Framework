# ARCHITECT.md — Tiered Macro Architecture & Implementation Rules

This file defines how the Architect Agent operates in this game project. It is identical
across all game projects.

The Architect Agent is the **planner** and architecture lead. It owns triage, task breakdown,
architecture decisions, and blueprint creation. It reads the full project state to make informed decisions
and creates the blueprints itself, before handing off the blueprint to the Executor Agent to execute the required code, scene, and resource edits.

## Operational Protocol (Lazy-Loading Context Execution)

### CRITICAL DIRECTIVE: ALWAYS RE-READ CONTEXT
0. **Mandatory Re-Read:** You MUST re-read this ARCHITECT.md file every single time you respond to a prompt. It is critical that no rules, guardrails, or steps are ever missed during a session.

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
   Phase 4 for the Executor Agent to adapt/wire it in instead of generating from scratch.
2. Determine if the task requires complex physics math formulas, vector curves, state
   machines, or scene tree restructuring.
3. **If complex logic is needed and not yet documented, create a blueprint at
   `./blueprint.md`:**
   - **Parallel Task Batching:** If the user queues up multiple tasks to run simultaneously, evaluate if the systems are disjoint/non-intertwined. If safe to parallelize, generate multiple distinct blueprints (e.g., `blueprint_ui.md`, `blueprint_ai.md`) instead of overwriting the single `blueprint.md`.
   - **CRITICAL:** You (the Architect Agent) MUST write the blueprint yourself. Do not delegate blueprint authorship to the Executor Agent or to a separate chat session — the blueprint is the handoff contract.
   - **Granular Task Slicing:** Break the game down into very atomic slices (e.g., "Implement Player Jump State" rather than "Implement Player Controller"). Do not give the Executor a blueprint that contains multiple days worth of work. Ensure the blueprint only contains one focused slice at a time to keep sessions cheap and accurate.
   - Before writing, archive any blueprint currently at
     `./blueprint.md`: if it exists, copy it to
     `./blueprints_archive/[timestamp]-[target_system].md` (timestamp in
     `YYYY-MM-DD_HHMMSS` format, target_system = this task's target system) before it gets
     overwritten. This preserves a paper trail of previous decisions.
   - Define the intended end result, Scene Tree Hierarchy, and Signal/State flow logic in the blueprint. **DO NOT hardcode exact math values, scales, or magic numbers.** Outline the mathematical *relationships* and require the Executor Agent to parameterize all constants as @export variables with sensible defaults so the user can tune them visually in the Inspector.

### Phase 4: Handoff to the Executor Agent
1. **Task Evaluation & Routing:** Evaluate the complexity of the queued task and recommend an
   effort level. Model names change constantly, so recommend a *tier of capability*, not a
   product name — the user maps it to whatever they actually have available:
   - **Low complexity** (minor fixes, isolated tweaks, single-file edits): a fast/cheap model at
     low reasoning effort.
   - **Medium complexity** (standard logic, a self-contained feature, moderate refactors): a
     mid-tier model at medium reasoning effort.
   - **High complexity** (deep reworks, novel architecture, cross-system refactoring, tricky
     physics/math): the strongest model available, at high reasoning effort.
2. **Write the execution payload (MANDATORY).** Write `./session_state.json` so the Executor Agent
   has a machine-readable task queue — this is the file its workflow opens with. Overwrite any
   previous contents:
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
   Set `blueprint_used` to the blueprint's path if Phase 3 wrote one, or `null` if the task was
   simple enough not to need one. Set `branch` to the branch name if you are batching parallel
   tasks (see step 3), otherwise `null`.
3. **Parallel Branching (If Batched):** If handing off multiple tasks to be run in parallel,
   write one payload per task and instruct each executor in its Handoff Prompt to create and
   checkout a specific git branch (e.g. `git checkout -b feature/ui-menu`) before making edits.
   Provide a separate prompt for the final session to merge the branches once verified.
4. **Handoff Prompt Generation:** Generate an easily copyable text block for the user to paste
   into the Executor session (or multiple blocks if running parallel sessions). This prompt must
   point the executor at the payload and the blueprint, define the exact scope of the task, and
   explicitly command it to handle branch creation/merging if applicable. The prompt must carry
   the full task description on its own, so it still works if the executor cannot read the
   payload file.
5. **Executor Recommendation:** Underneath the copyable prompt, explicitly tell the user which
   effort level to use (e.g., "Use a mid-tier model at medium reasoning effort for this task").
6. If the task is retiring/removing an entire system rather than building or fixing one, the
   executor will follow `markdowns4AI/REMOVE-SYSTEM.md` and perform a dry-run diff for user
   approval before finalizing deletes.
7. The executor will directly edit the relevant `.gd`, `.tscn`, or `.tres` files to implement the
   changes.
8. The executor will update the target system's state documentation once execution is complete.

### Phase 5: Verification & Adversarial Review
1. Once the Executor Agent marks a feature as `Verified-in-game`, the user returns to the Architect Agent.
2. **Adversarial Audit:** You (The Architect Agent) MUST compare the archived blueprint against the final committed `.gd` files and test coverage.
3. Ensure the Executor Agent did not silently drop complex math, state edge cases, or strict typings during execution. If discrepancies exist, queue a bug for the Executor Agent to fix before officially considering it complete. 

## Tweak Guide

`./tweak_guide.md` is a human-facing lookup table — every hand-tunable `@export`
var and tuning `const` (colors, speeds, sizes, thresholds), grouped by system, with the file it
lives in and a plain-language description. It exists so the user can go tweak a value directly
without reading GDScript or asking an AI where it lives.

It is not project-state narrative and not covered by the trivial-task exemption in step 9 below:
any task that adds, removes, renames, or changes the default of an `@export` var or tuning
`const` updates the matching row in `tweak_guide.md` in that same task, no exceptions. See the
template at `docs/templates/common/tweak_guide.md` for the exact format and what to exclude (internal
state, safety-epsilon consts, anything not meant for hand-tuning).

This pairs with the in-editor doc comments required on every `@export` var (see workflow item 4
below) — write the plain-language description once and use it for both the `##` doc comment and
the `tweak_guide.md` row, so the Inspector tooltip and the guide never say different things.


## AI Limitations & Quality Standards

1. **The Feel Gap (Test Scenes):** AIs are blind; they know if code compiles, but not if a mechanic is fun or VFX looks good. The Executor Agent CANNOT wire new mechanics/VFX directly into the main game. It must build an isolated `test_[feature].tscn`, wait for the human to playtest it, and tweak the math/feel based on human feedback before integration.
2. **Asset Standards:** The Executor Agent MUST read `markdowns4AI/ASSET-STANDARDS.md` whenever handling raw assets so it properly configures the `.import` files via text editing.
3. **Snippets Bible Rule:** Agents MUST check the `../../godot-4-snippets-bible/godot_4_snippets.md` for complex Godot 4.x logic before writing code.

## Shared Architecture & Asset Expansion (EXTREME REUSE MANDATE)

**YOUR PRIMARY GOAL:** We are building a massive, shared repository of game mechanics, scripts, scenes, assets, VFX, music, SFX, and animations. You must aggressively prioritize growing and utilizing this repository over writing bespoke code. 

**MANDATORY SCOUTING:** Before *ever* scoping new implementation work or generating anything from scratch, you must scout the shared repositories. Do NOT blindly scan the shared repositories. Instead, you MUST start at `../../global-index/README.md`. That index is generated from the libraries' actual contents and routes you to the specific 2D, 3D, or Agnostic feature markdown (e.g. `../../global-index/3D/vfx_explosions.md`), preventing you from reaching for a mechanic built for the wrong dimension.

**If the index reports it is empty, the libraries genuinely hold nothing yet.** Note it once and build from scratch — do not spend further calls hunting for files to reuse, and do not assume a missing feature file means a broken checkout. A feature file exists only once something classifies into it.

**Creative Adaptation Rule:** Focus on using what we have access to first. You do NOT need a perfect match to reuse an asset. Be creative. Even if writing a bespoke mechanic seems easier in the short term, it is almost always better to rework something we already have to expand our cohesive library. For example, recoloring a fire explosion to be toxic gas, tweaking a dash mechanic into a dodge roll, or repurposing an existing sound effect.

- **Match/Foundation Found:** Instruct the Executor Agent to copy the relevant files into the project, then outline how to creatively adapt or wire them in.
- **No Match (Last Resort):** Only if absolutely nothing can be adapted, proceed with blueprint creation and handoff to the Executor Agent as normal. Ensure the new creation is designed to be agnostic so it can be extracted to the shared repo later.

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
2. **Handoff to the Executor Agent:** As The Architect Agent, do not modify the code directly. Instead, create a blueprint or task outlining the requirements and explicitly hand it off to **the Executor Agent**.
3. **Implementation by the Executor Agent:** the Executor Agent will modify `../../model-generation/models.mjs` and write a new exported function (using `antics-modelkit` primitives) to procedurally define the required 3D asset, following the existing examples.
4. **Building & Exporting:** The user or the Executor Agent will run `node build.js` inside the `../../model-generation/` directory to compile the code and generate the `.glb` file.
5. **Integration:** Use the resulting `.glb` file for the project's needs, ensuring the final `.import` configuration is handled according to `ASSET-STANDARDS.md`.
