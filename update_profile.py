import os
import re

tiers = ['lite', 'standard', 'heavy']
base_dir = r"c:\Godot_Projects\docs\templates\tiers"

for tier in tiers:
    file_path = os.path.join(base_dir, tier, "GEMINI.md")
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    out_lines = []
    in_phase_1 = False
    added_profile = False
    
    for line in lines:
        if "### Phase 1: High-Level Triage" in line:
            in_phase_1 = True
            out_lines.append(line)
            continue
            
        if "### Phase 2:" in line:
            in_phase_1 = False
            
        if in_phase_1:
            match = re.match(r"^(\d+)\.\s+(.*)", line)
            if match:
                num = int(match.group(1))
                rest = match.group(2)
                
                if num == 3 and not added_profile:
                    out_lines.append("3. **Project Profile (MANDATORY):** Read `./PROJECT-PROFILE.md` to instantly understand the project's dimension (2D/3D), genre, tier, and core loop.\n")
                    added_profile = True
                    out_lines.append(f"4. {rest}\n")
                else:
                    new_num = num + 1 if added_profile else num
                    out_lines.append(f"{new_num}. {rest}\n")
            else:
                out_lines.append(line)
        else:
            out_lines.append(line)
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
    print(f"Updated {tier} GEMINI.md")
