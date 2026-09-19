import os
import re

tiers = ['lite', 'standard', 'heavy']
base_dir = r"c:\Godot_Projects\docs\templates\tiers"

for tier in tiers:
    file_path = os.path.join(base_dir, tier, "GEMINI.md")
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find the Handoff section
    handoff_regex = r"(### Phase \d+: Handoff to Claude Code \(Task Execution\)).*?(?=### Phase \d+:)"
    match = re.search(handoff_regex, content, re.DOTALL)
    
    if match:
        old_handoff = match.group(0)
        phase_title = match.group(1)
        
        # Extract the state file text from the old bullet 4
        bullet4_match = re.search(r"4\. Claude Code will update (.*?) with the new system state changes", old_handoff)
        state_files = bullet4_match.group(1) if bullet4_match else "the relevant state tracking files"
        
        new_handoff = f"""{phase_title}
1. **Task Evaluation:** Evaluate the complexity of the queued task to determine the appropriate Claude Code model and effort level.
   - **Model Options:** `sonnet 5.0` (for standard logic/fixes) or `opus 5.0` (for deep reworks or complex architecture).
   - **Effort Options:** `low`, `medium`, `high`. (Use `max` ONLY with `opus 5.0` for really complex and deep reworks).
2. **Handoff Prompt Generation:** Generate an easily copyable text block for the user to paste into Claude Code. This prompt must direct Claude to the blueprint and define the exact scope of the task.
3. **Model & Effort Recommendation:** Underneath the copyable prompt, explicitly tell the user which Claude Code model and effort level to use (e.g., "Use **Sonnet 5.0** with **Medium** effort").
4. If the task is retiring/removing an entire system rather than building or fixing one, Claude Code will follow system removal guidelines (e.g., `REMOVE-SYSTEM.md` if present) and perform a dry-run diff for user approval before finalizing deletes.
5. Claude Code will directly edit the relevant `.gd`, `.tscn`, or `.tres` files to implement the changes.
6. Claude Code will update {state_files} with the new system state changes once execution is complete.

"""
        
        new_content = content[:match.start()] + new_handoff + content[match.end():]
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {tier}")
    else:
        print(f"Could not find Handoff section in {tier}")
