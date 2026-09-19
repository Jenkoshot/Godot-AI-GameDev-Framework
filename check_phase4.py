import os

tiers = ['lite', 'standard', 'heavy']
base_dir = r"c:\Godot_Projects\docs\templates\tiers"

for tier in tiers:
    file_path = os.path.join(base_dir, tier, "GEMINI.md")
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_idx = content.find("### Phase 4:")
    end_idx = content.find("### Phase 5:")
    print(f"--- {tier} ---")
    if start_idx != -1 and end_idx != -1:
        print(content[start_idx:end_idx])
