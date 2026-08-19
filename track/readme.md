# AI Context Management

This directory serves as the source of truth for AI agents working on the Bee project. To ensure consistency across multiple agents, all agents must read and update these files before and after any major changes.

## File Structure

- `context.md`: High-level overview of the project, current priorities, and global constraints.
- `status.md`: Real-time tracking of open tasks, active branches, and project health.
- `rules.md`: Shared guidelines and behaviors for AI agents working in this repository.

## Agent Protocol

1. **Before Starting:** Read `context.md` and `status.md` to understand the current state.
2. **During Tasks:** If a task changes the architectural direction or adds a new dependency, update `context.md`.
3. **After Tasks:** Update `status.md` to reflect completed work and identify next steps.
4. **Coordination:** If another agent is currently working (check the timestamp/status), coordinate via `status.md` to avoid conflicts.
