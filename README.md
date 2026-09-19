# Godot Projects Global Repository

This is the shared, cross-project parent repository for all Godot game projects. It centralizes our **Standardized Dual-Agent Workflow**, making it easy for multiple games to share assets, maintain documentation, and follow the same AI-assisted development processes.

## What's Inside

- **`Projects/`**: The directory where all individual game projects live. Each game has its own independent git repo.
- **Global Shared Repositories**:
  - `asset-repository/`: Raw 3D models and textures.
  - `mechanic-repository/`: Reusable, project-agnostic GDScript logic.
  - `scene-repository/`: Reusable `.tscn` and `.tres` structures.
  - `effect-blocks/` & `poly-blocks/`: Visual effects and environment nature blocks.
  - `godot-shader-bible/` & `godot-4-snippets-bible/`: References for complex rendering and logic.
  - `model-generation/`: Workspace for procedural or AI-generated 3D models.
- **`docs/templates/`**: The canonical markdown playbooks (e.g., `SETUP.md`, `CLAUDE.md`, `GEMINI.md`) that govern the AI agents and orchestrate project setup.
- **`global-index/`**: The master routing directory for finding shared assets.

## The Dual-Agent Workflow

Our workflow relies on two AIs working in tandem via local markdown state files:
1. **Antigravity (Gemini)** - *The Planner*: Reads project state, checks shared global repos, and generates technical blueprints in `project-state/blueprints/latest_blueprint.md`.
2. **Claude Code** - *The Executor*: Takes the blueprint and writes the actual `.gd`, `.tscn`, and `.tres` files using Godot MCP tools, then creates isolated test scenes for human playtesting.

---

## AI Prompt Guide (Copy & Paste)

Use these exact prompts with **Antigravity** (run `agy` in your project folder) to trigger specific playbook workflows without having to guess. 

### 1. Setting Up a New Game
Drop your initial design documents into the `new_project_design_docs/` folder, open a terminal in the `Godot_Projects` root directory, and run `agy`. Then use this prompt:
> "I want to create a new project. Look at the design docs in `new_project_design_docs/`, determine the game name, create a new folder under `Projects/` with that name, make a new Godot project in it, run the setup based on the docs, and move the design docs into the game's `design_docs/` folder."

### 2. Planning a New Feature
Run this to have Antigravity analyze the current state, check the global repositories for reusable code/assets, and write a blueprint for Claude.
> "I want to build [Feature]. Read our overview docs, check the global index for reusable assets, and generate a detailed blueprint for this."

### 3. Upgrading Project Tier
If your project is getting too complex for its current tier (e.g., Lite, Standard), you can upgrade its documentation and tracking structure.
> "Run the upgrade playbook at `../docs/templates/UPGRADE-TIER.md` to upgrade this project's scale tier."

### 4. Cleaning Up / Restructuring
Run these maintenance tasks when the project gets messy or outdated.

**To fix documentation drift:**
> "Review the codebase against our docs using `DESIGN-DRIFT.md` to find and fix any mismatches."

**To restructure folders:**
> "Propose and execute safe file and folder restructuring following the `ORGANIZE.md` playbook."

**To delete an old system:**
> "We are retiring the [System Name] system. Please follow the `REMOVE-SYSTEM.md` playbook to safely archive it."

### 5. Harvesting Reusable Assets
If you built a cool agnostic system or asset in your game, push it up to the global repositories for future games to use.
> "Sweep this project for generic assets and extract them to the global repository per the `HARVEST-REPO.md` playbook."

---

## Prerequisites
To fully utilize this repository and workflow, you need:
- **Godot 4.4+** (Required for the `godot-mcp` server)
- **Node.js 18+** (Required for the MCP server and `model-generation` scripts like `antics-modelkit`)
- **Python 3 + pip** (Install `gdtoolkit` for formatting/linting)
- **Gemini CLI (Antigravity)** and **Claude Code**
- **Git**

### Model Generation Setup
For 3D model generation, you also need to initialize the workspace inside `model-generation/`:
1. Navigate to the `model-generation/` directory.
2. Ensure you run `npm install` to install `antics-modelkit`, `three`, and `@gltf-transform/cli`.
3. Read `model-generation/GEMINI.md` for specific rules on generating procedural assets.
