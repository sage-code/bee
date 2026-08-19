# AI Agent Rules

- **Execution Constraints:** Absolutely no parallel or rapid-fire requests. Every write/API call MUST be followed by a 30-second pause.
- **Scope:** Do not stray from the `DECISIONS.md` log. If you find a conflict, create a new task in `/todo`.
- **Communication:** If you identify a conflict or need clarification, leave a note in `track/status.md` and create a task in `/todo`.
- **License:** All contributions are under GPLv3.
- **Workflow:** Read `track/context.md` -> Check `/todo` -> Execute -> Update `/track/status.md` -> Wait 30s.
