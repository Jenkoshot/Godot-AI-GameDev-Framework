# SETUP-FRAMEWORK Playbook

**Trigger:** When the user has just cloned the repository and asks to "set up the framework", "install requirements", or "run the setup markdown".

**Description:** This playbook automates the initialization of the entire Godot AI GameDev Framework, installing necessary Node and Python dependencies, and mapping the Godot executable for the MCP server.

## Execution Steps

1. **Verify Prerequisites:** 
   Ask the user to confirm they have installed:
   - Node.js (v18+)
   - Python 3+
   - Godot 4.4+
2. **Setup Godot MCP:**
   - Navigate into `docs/tools/godot-mcp/`.
   - Run `npm install` and `npm run build`.
3. **Setup Model Generation (antics.gg):**
   - Navigate into `model-generation/`.
   - Run `npm install`.
4. **Configure Godot Path:**
   - Ask the user for the absolute file path to their Godot 4.4 executable (e.g., their Steam path or standalone `.exe`).
   - Read `docs/machine_paths.json`.
   - Replace the generic template with their computer's hostname and the executable path they provided.
5. **Python Dependencies:**
   - Run `pip install gdtoolkit` (required for Godot script formatting/linting).
6. **Completion Report:**
   - Inform the user that the framework is ready.
   - Tell them they can now provide a Game Design Document (GDD) or ask you to brainstorm a new game!
