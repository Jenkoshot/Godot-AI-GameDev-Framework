import os
import re
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

tiers = ['lite', 'standard', 'heavy']
base_dir = r"c:\Godot_AI_Framework\docs\templates\tiers"

for tier in tiers:
    file_path = os.path.join(base_dir, tier, "ARCHITECT.md")
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    in_handoff = False
    
    print(f"--- {tier} ---")
    for line in lines:
        if "Handoff to Claude Code" in line:
            in_handoff = True
        elif in_handoff and line.startswith("### Phase"):
            in_handoff = False
            
        if in_handoff:
            print(line, end="")
