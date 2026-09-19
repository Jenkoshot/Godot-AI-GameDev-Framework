# Claude MCP Migration

Run this only when this project adopts a different Godot MCP server than the one currently
configured (see `CLAUDE.md`'s "Current MCP" section for what's active now).

## Process

1. Scan `CLAUDE.md` for every `mcp__<server>__<action>` tool reference.
2. Load the new MCP server's tool list/schema (via its own documentation or by inspecting its
   available tools directly).
3. Map each old capability to its nearest equivalent in the new server.
4. Rewrite `CLAUDE.md`'s tool references and "Current MCP" section in place — leave the
   workflow structure and principles sections untouched.
5. Flag any capability that has no equivalent in the new server, so it's a visible, explicit
   gap rather than a silently dropped capability.
