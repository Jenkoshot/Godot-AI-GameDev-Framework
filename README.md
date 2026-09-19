# Godot AI Monorepo & Dual-Agent Workflow

Welcome to the **Godot AI Monorepo Framework**. This repository is a scalable, tiered architecture designed to solve the biggest bottlenecks in AI-assisted game development: context window bloat, Godot scene corruption, and code duplication. 

Instead of treating every game as an isolated folder, this monorepo acts as a centralized brain. It utilizes a **Dual-Agent Workflow** (using Gemini/Antigravity and Claude Code) combined with a **Godot MCP Server** to build games safely, efficiently, and at scale.

---

## 🌟 Why This Architecture Exists

If you've tried building games with AI, you know the pain points:
1. **The Context Trap:** You feed your whole project into an AI, the context window fills up, and the AI starts forgetting rules or hallucinating old code.
2. **Scene File Corruption:** Godot's `.tscn` files are fragile. When an LLM tries to guess text-based scene edits, it often corrupts the file.
3. **The Blank Canvas Problem:** AIs prefer writing from scratch. They will write a bespoke `player_controller.gd` 10 different times for 10 different games instead of reusing one.

**The Solution:**
- **The Planner (Antigravity/Gemini):** Reads your high-level docs, tracks project completion percentage, calculates bug triage, checks shared repositories for reusable code, and writes a strict "blueprint".
- **The Executors (Claude Code & ChatGPT Codex):** Reads *only* the blueprint. Gemini dynamically routes tasks based on complexity—sending low/medium effort tasks to ChatGPT Codex, and complex architectural tasks to Claude Code (which uses the Godot MCP server for native `.tscn` edits).
- **The Global Repositories:** Forces the AI to harvest and reuse agnostic code (`mechanic-repository/`) across all your games.

---

## 🚀 Key Features

### 1. Automated Triage & Progress Tracking
You never have to guess what to work on next. When you start a session, Gemini reads your `project-state/_overview.md` and `bugs/master_bugs.md`. It automatically calculates the game's overall completion percentage and selects the single highest-priority task to execute based on three weighted metrics:
- **Severity** (e.g., Crash > Cosmetic)
- **Unblock Value** (Does this task unblock 3 other queued features?)
- **Deadline Proximity**

### 2. Smart Executor Routing (Claude vs. Codex)
Not every task requires an expensive, heavy-duty AI. Gemini evaluates the complexity of the blueprint it just created and recommends the best Executor:
- **Low/Medium Complexity:** Gemini generates a copy-paste handoff prompt instructing you to use **ChatGPT Codex** (GPT-5.6).
- **High Complexity / Deep Refactors:** Gemini hands the blueprint off to **Claude Code** (Sonnet/Opus 5.0) utilizing the Godot MCP server.

### 3. Godot MCP Integration
Godot's `.tscn` files are fragile. When an LLM tries to guess text-based scene edits, it corrupts the file. Our custom Node.js Godot MCP server allows Claude to interface natively with the Godot engine, dramatically reducing scene corruption.

---

## 🛠️ Prerequisites

To run this framework, you need:
1. **Godot 4.4+** (Required for the `godot-mcp` server)
2. **Node.js 18+** (Required for the MCP server and procedural model generation)
3. **Python 3 + pip** (For running the sync scripts and formatting)
4. **Claude Code** & **ChatGPT Codex** (The Executors)
5. **Gemini CLI (Antigravity)** (The Planner)

---

## 🧠 The Three Workspaces (How to run the AI)

You do not run the AI from just one place. You open your CLI (Antigravity or Claude) in specific folders depending on what you want the AI to do.

### 1. The Root Workspace (`/Godot_Projects/`)
**Run Antigravity here when you want to:**
- Create a brand new game project (using `docs/templates/SETUP.md`).
- Run python scripts to sync rules across all games (`python sync_templates.py`).
- Ask high-level questions about your entire portfolio of games.

### 2. The Project Workspace (`/Projects/[Your_Game]/`)
**Run Antigravity & Claude Code here to actually build the game.**
* **Step 1:** Open Antigravity in this folder. Ask it to design a feature. It will read `GEMINI.md`, check the global repos, and output a blueprint to `project-state/blueprints/latest_blueprint.md`.
* **Step 2:** Open Claude Code in the same folder. Tell it: *"Execute the latest blueprint."* It will read `CLAUDE.md`, use the Godot MCP to write the code/scenes, and make an isolated test scene.
* **Step 3:** You playtest the test scene. Once it feels good, Claude integrates it into the main game.

### 3. The Model Generation Workspace (`/model-generation/`)
**Run an AI here when you need 3D assets.**
Instead of opening Blender, open an AI here. It uses a procedural Node.js library (`antics-modelkit`) to generate 3D models via code.
- Run `npm install`.
- Ask the AI to write a script to generate a specific model (e.g. "a low poly spaceship").
- Run `node build.js` to spit out a perfect `.glb` file you can drag into the asset repository.

---

## 📖 The Playbooks (How to command the AI)

The `docs/templates/` folder contains Markdown "Playbooks". These are highly specific workflows you can command the AI to execute. 

**How to call them:** Open Antigravity in your specific game's folder (`Projects/[Game]`) and simply say: *"Run the [PLAYBOOK_NAME] playbook."*

- **`HARVEST-REPO.md`**: Run this when you've built a really cool, generic system (like a dialogue manager) in your specific game. The AI will extract it, make it project-agnostic, and move it to the global `mechanic-repository/` so your future games can use it.
- **`REMOVE-SYSTEM.md`**: Run this when a game system is bloated or broken. The AI will safely untangle it, remove the dependencies, and archive it without breaking the rest of your game.
- **`DESIGN-DRIFT.md`**: Run this when your game code has drifted away from your original design docs. The AI will audit the codebase and highlight where the code no longer matches the design.
- **`UPGRADE-TIER.md`**: Our projects have "Tiers" (Lite, Standard, Heavy). If your simple mobile game (Lite) suddenly becomes a massive RPG, run this playbook to upgrade its documentation tier to Heavy, giving the AI stricter architectural rules.

---

## 🔌 Setting up the Godot MCP Server

The Godot MCP Server (`docs/tools/godot-mcp`) is what allows Claude Code to natively understand Godot. 

1. Navigate to `docs/tools/godot-mcp/`.
2. Run `npm install` and `npm run build`.
3. In Claude Code, or your preferred MCP client, configure the server by pointing it to the compiled build directory. 
4. The template configuration is located at `docs/templates/common/mcp_config.json`. The Python sync scripts (`sync_templates.py`) will automatically drop this config into your game projects so Claude knows how to use it.

---

## 🤝 Contributing & Customizing

This monorepo is designed to be customized. If you find that the AI keeps making a specific mistake, **do not correct it in the chat**. 
Instead, edit `docs/templates/tiers/standard/CLAUDE.md` and add a new rule. Then, go to the root directory and run `python sync_templates.py`. Your new rule will instantly be pushed to every single game project you own.
