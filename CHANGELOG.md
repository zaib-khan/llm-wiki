# Changelog

All notable changes to the LLM Wiki prompt (`zaib-khan-llm-wiki.md`) are documented here.
A wiki applies these changes with the `update wiki` command (`/update_wiki` in Claude Code).
Only tagged versions (`vX.Y.Z`) are proposed as updates.

Versions follow `MAJOR.MINOR.PATCH`:
- **PATCH**: clarifications, no impact on the wiki.
- **MINOR**: new rules, templates, or commands; simple migration.
- **MAJOR**: structural changes; pages or folders may move.

## [Unreleased]

## [0.9.0] - 2026-10-15

### Added
- First versioned release of the prompt (`Version: 0.9.0`).
- `update wiki` command and `/update_wiki` Claude Code skill (section 9.6): checks the latest tagged version, shows the changes, detects user customizations, secures the wiki (git commit or `../<wiki-name>_backup/`), and applies the update after validation.
- `prompt_version` and `prompt_source` in `settings.md`; copy of the applied prompt in `.llm-wiki/prompt-<version>.md`.
- Lint check: a newer version of the prompt is published.
- Log event type `update`.

### Migration from an unversioned wiki
- No `prompt_version`: the update compares the whole wiki with this version and lists every difference for validation.
