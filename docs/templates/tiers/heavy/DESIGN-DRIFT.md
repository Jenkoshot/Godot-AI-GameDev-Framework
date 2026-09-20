# Design Drift Detector

An on-demand, read-only utility that compares `design_docs/*.md` and
`project-state/[system]/[system].md` descriptions against the actual code, flagging concrete
mismatches for the user to resolve — in either direction. Invocable two ways: standalone, any
time the user asks for a drift check; or offered once during `SETUP.md`'s initial bootstrap run
on an existing codebase.

Distinct from a bug: see `EXECUTOR.md`'s "Bugs vs. Design Drift" section. This utility only
surfaces drift, never bugs — a mismatch caused by code failing to do what was intended belongs
in `bugs/[system]/[system].md` instead, not in this report.

## Process

1. **Manual trigger only.** Never runs automatically as part of a normal task — the
   task-completion step of `EXECUTOR.md` already catches drift caused by the current task; this is a separate, explicit
   sweep for drift that accumulated outside any single task.
2. **Scope.** For each system named in `project-state/_overview.md`'s Script Registry (or a
   single system if the user names one), compare its `project-state/[system]/[system].md`
   description and any `design_docs/*.md` that documents it against the actual current code —
   signals, public functions, and tri-state status.
3. **Report concrete mismatches only** — a signal documented but absent from code, a function
   renamed or removed, a status marked `Verified-in-game` with no corresponding test, a
   `design_docs/*.md` describing behavior the shipped code no longer has. Do not report
   subjective or style opinions; this is a factual diff, not a code review.
4. **Never auto-resolve.** Present each mismatch as a numbered item: what the doc says vs. what
   the code does. Let the user decide the fix direction — patch the code to match the doc, or
   update the doc to match the code.
5. **Approval gate.** Wait for the user's fix-direction decision per item (or a batch decision)
   before touching anything.
6. **Execution.** Route any resulting doc edit through `EXECUTOR.md`'s normal
   documentation-consistency handling; route any resulting code edit through the normal
   `EXECUTOR.md` workflow (typing, test authorship, tri-state rules) — a drift-detector-triggered
   code change is not exempt from any of that.
