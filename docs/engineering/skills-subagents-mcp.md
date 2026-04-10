# Skills, subagents, and MCP defaults

## Subagents

- Use subagents for parallel research on security posture, PR/issue
  state, release path, or workflow health.
- Keep conflicting code edits serialized in the main
  worktree/controller.
- Ask review-oriented subagents to check spec compliance and code
  quality before merge preparation.

## MCP / tool defaults

- GitHub tooling for PR, issue, workflow, collaborator, release, and
  code-scanning truth
- Playwright for localhost screenshots and browser-based verification
  when the user manual changes
- memory tooling for durable repo-specific preferences or blocker
  history when helpful

## Repository-specific guidance

- Prefer repository-local docs over generic skill defaults when they
  disagree.
- Use `uv`-based commands as the first choice for Python setup and execution.
- Keep stacked PR continuity explicit because `develop` and `main`
  can diverge intentionally.
