# -*- coding: utf-8 -*-
import os, glob, re
paths = glob.glob('c:/Godot_Projects/docs/templates/tiers/*/AGENTS.md')
for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(r'- \*\*Tier 0 \(always available, no MCP required\):\*\* direct text edits to \.gd script files via\n\s*normal file tools, and command-line execution \(e\.g\. gdlint, gdformat, and headless\n\s*verification via the Godot binary directly using your terminal tool\) — neither needs a live\n\s*editor connection\. \(Note: You are expected to have and use your terminal/command execution capabilities for these tasks\)\.')
    
    repl = r'''- **Tier 0 (always available, no MCP required):** direct text edits to `.gd` script files via
  normal file tools, and command-line execution (e.g. `gdlint`, `gdformat`, and headless
  verification via the Godot binary directly using your terminal tool) — neither needs a live
  editor connection. (Note: You are expected to have and use your terminal/command execution capabilities for these tasks).'''
    
    content = pattern.sub(repl, content)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated ' + p)
