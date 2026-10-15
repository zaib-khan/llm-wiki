# Changelog

All notable changes to the LLM Wiki prompt (`zaib-khan-llm-wiki.md`) are documented here.
A wiki applies these changes with the `update wiki` command (`/update_wiki` in Claude Code).
Only tagged versions (`vX.Y.Z`) are proposed as updates.

Versions follow `MAJOR.MINOR.PATCH`:
- **PATCH**: clarifications, no impact on the wiki.
- **MINOR**: new rules, templates, or commands; simple migration.
- **MAJOR**: structural changes; pages or folders may move.

## [Unreleased]

### Changed
- People and companies: `contacts/` and `companies/` folders at the domain level, each with a list page (`<domain>-contacts.md`, `<domain>-companies.md`). Types `contact`, `contact-list`, `company`, `company-list`. A contact needs a name and a way to reach them, except family members.
- Type subfolders (`sources/`, `entities/`, `concepts/`, `syntheses/`, `contacts/`, `companies/`) are now named in the wiki's language, fixed once in `settings.md`.
- `contact` and `company` pages: every section is optional; only sections with content are shown. Other page types keep all their sections.
- Update procedure (section 9.6): rule for migrating pages to a new template — section mapping validated once per template, no empty sections added, frontmatter filled only when deducible, content and links always kept.
- Update from an unknown version (section 9.6, step 2): every difference is now presented as a possible conflict, one at a time, and the user says whether it is a personal choice (keep) or an old rule (replace). If the user does not know, the new version is applied.

### Migration from 0.9.0
- Move `<domain>/entities/personne/*` to `<domain>/contacts/` and `<domain>/entities/companies/*` to `<domain>/companies/`.
- Rename `personne-<domain>.md` to `<domain>-contacts.md` (type `contact-list`); create `<domain>-companies.md`.
- Change `type: person` to `contact`, `type: people` to `contact-list`; rename templates accordingly.
- Contacts without a way to reach them and not marked as family: ask the user (keep with a contact detail, mark as family, or turn into plain text).
- Choose the type subfolder names in the wiki's language, record them in `settings.md`, then rename the existing type subfolders and list pages in every domain (wikilinks resolve by file name, so links keep working).

## [0.9.0] - 2026-10-15

### Added
- First versioned release of the prompt (`Version: 0.9.0`).
- `update wiki` command and `/update_wiki` Claude Code skill (section 9.6): checks the latest tagged version, shows the changes, detects user customizations, secures the wiki (git commit or `../<wiki-name>_backup/`), and applies the update after validation.
- `prompt_version` and `prompt_source` in `settings.md`; copy of the applied prompt in `.llm-wiki/prompt-<version>.md`.
- Lint check: a newer version of the prompt is published.
- Log event type `update`.

### Migration from an unversioned wiki
- No `prompt_version`: the update compares the whole wiki with this version and lists every difference for validation.
