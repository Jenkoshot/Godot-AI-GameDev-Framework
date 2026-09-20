# Architecture Decision Log (ADR)

This file tracks the "Why" behind major architectural decisions to prevent AI agents from losing context, undoing complex work, or hallucinating different systems in future sessions.

The Executor Agent logs a new entry here at the end of any complex task.

### Example Entry:
**Date**: 2026-08-01
**System**: Grid Movement
**Decision**: Chose `AStarGrid2D` over `NavigationRegion2D`.
**Reasoning**: The game requires strict tile-based movement and Manhattan distance calculations. `NavigationRegion2D` is too floaty and unpredictable for grid constraints.

---

## Log
