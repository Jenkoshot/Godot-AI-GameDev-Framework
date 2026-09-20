# -*- coding: utf-8 -*-
import os
import glob
import re

agent_paths = glob.glob(r'c:/Godot_Projects/docs/templates/tiers/*/EXECUTOR.md')

for path in agent_paths:
    if not os.path.exists(path): continue
    content = open(path, encoding='utf-8').read()
    
    # Update Tier 0 description
    pattern = re.compile(r'- \*\*Tier 0 \(always available, no MCP required\):\*\* direct text edits to \.gd script files via\n\s*normal file tools, and headless verification via the Godot binary directly \(godot --headless\n\s*--script res://tests/run_tests\.gd\)  neither needs a live editor connection\.')
    
    replacement = """- **Tier 0 (always available, no MCP required):** direct text edits to .gd script files via
  normal file tools, and command-line execution (e.g. gdlint, gdformat, and headless
  verification via the Godot binary directly using your terminal tool)  neither needs a live
  editor connection. (Note: You are expected to have and use your terminal/command execution capabilities for these tasks)."""
    
    content = pattern.sub(replacement, content)
    open(path, 'w', encoding='utf-8').write(content)
    print("Updated", path)
