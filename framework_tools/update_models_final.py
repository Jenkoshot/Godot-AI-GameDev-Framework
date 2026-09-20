import os, glob, re
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths = glob.glob(os.path.join(ROOT_DIR, 'docs/templates/tiers/*/ARCHITECT.md'))
paths.append(os.path.join(ROOT_DIR, 'ARCHITECT.md'))
new_phase4 = r'''### Phase 4: Handoff to Executor (ChatGPT Codex or Claude Code)
1. **Task Evaluation & Routing:** Evaluate the complexity of the queued task to determine the appropriate executor and model:
   - **Low Complexity** (e.g., minor fixes, isolated tweaks): Route to **ChatGPT Codex** using `GPT-5.6 Terra` or `GPT-5.6 Luna` (Low effort).
   - **Medium Complexity** (e.g., standard logic, moderate features): Route to **ChatGPT Codex** using `GPT-5.6 Sol` (Medium effort).
   - **High Complexity** (e.g., deep reworks, complex architecture, large scale refactoring): Route to **ChatGPT Codex** using `GPT-6 Astra` (High effort), or **Claude Code** (`sonnet 5.0` or `opus 5.0`).
2. **Parallel Branching (If Batched):** If handing off multiple tasks to be run in parallel, instruct the executor in the Handoff Prompt to create and checkout a specific git branch (e.g. `git checkout -b feature/ui-menu`) before making edits. Provide a separate prompt for the final session to merge the branches once verified.
3. **Handoff Prompt Generation:** Generate an easily copyable text block for the user to paste into the chosen executor (or multiple blocks if running parallel sessions). This prompt must direct the executor to the blueprint, define the exact scope of the task, and explicitly command them to handle branch creation/merging if applicable.
4. **Executor Recommendation:** Underneath the copyable prompt, explicitly tell the user which executor, model, and effort level to use (e.g., "Use **ChatGPT Codex (GPT-5.6 Sol - Medium effort)** for this task" or "Use **Claude Code (Sonnet 5.0 - Medium effort)**").
5. If the task is retiring/removing an entire system rather than building or fixing one, the executor will follow system removal guidelines (e.g., `REMOVE-SYSTEM.md` if present) and perform a dry-run diff for user approval before finalizing deletes.
6. The executor will directly edit the relevant `.gd`, `.tscn`, or `.tres` files to implement the changes.
7. The executor will update `./project-state/[target_system]/[target_system].md` with the new system state changes once execution is complete.'''

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = re.compile(r'### Phase 4: Handoff to Executor \(ChatGPT Codex or Claude Code\).*?(?=### Phase 5)', re.DOTALL)
    content = pattern.sub(new_phase4 + '\n\n', content)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated ' + p)
