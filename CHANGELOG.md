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
- Split prompt authoring into seven thematic files in `prompt/`. A dependency-free Python script assembles the same complete prompt, preserving its text and section order; `--check` detects an outdated generated file.
- Ingest checks for partially processed sources, completes each source before moving it, and resumes interrupted work without duplicating pages or facts. Sources needing a filing decision stay pending while independent sources continue.
- Projects attached to a domain or subdomain now live inside it (`wiki/<domain>/projects/<project>/<project>.md`, `projects/` being a reserved name); the domain page and template list its projects. `wiki/projects/` is kept only for cross-domain projects without a main domain.
- Per-domain filing rules: when it is unclear where content belongs among a domain's subdomains or projects, the agent proposes a short filing rule; once validated, it is recorded in `settings.md` ("Filing rule (<domain>)") and applied at every ingest and capture without asking again.

### Migration
- The source split requires no wiki migration: installation, tagged updates and the saved prompt copy still use `zaib-khan-llm-wiki.md`.
- No file migration. Existing wikis adopt this ingest procedure when they update the schema.
- Projects attached to a domain: projects currently in `wiki/projects/` that clearly belong to one domain are proposed to the user one by one and, after validation, moved to `wiki/<domain>/projects/<project>/` (their raw sources move to `raw/processed/<domain>/projects/<project>/`), and the domain page links them. Wikilinks resolve by file name, so links keep working. Cross-domain projects stay in `wiki/projects/`.
- Filing rules: none needed. Existing wikis adopt them when they update; rules are added to `settings.md` as filing questions arise.

## [0.11.0] - 2026-10-15

### Added
- New page type `howto` (template `template-howto.md`, type subfolder `how-to/`, e.g. `comment-faire/` in a French wiki): step-by-step procedures. Only "Goal" is required. `status` (`writing`, `draft`, `tested`, `outdated`) with a synced `howto/<status>` tag, and `last_used`. The user may write `writing` how-tos by hand.

### Changed
- Page type `concept` renamed to `knowledge` (template `template-knowledge.md`, type subfolder `knowledge/`, e.g. `connaissances/` in a French wiki).

### Migration from 0.10.0
- Rename every `concepts/` type subfolder to the `knowledge` folder name of the wiki's language (recorded in `settings.md`), change `type: concept` to `type: knowledge`, rename `template-concept.md` to `template-knowledge.md` and its "Related concepts" section to "Related knowledge". Wikilinks resolve by file name, so links keep working.
- The agent lists the `knowledge` pages that are actually step-by-step procedures (e.g. "procedure-…", "runbook-…"), and after validation moves them to the how-to folder and adapts them to `template-howto.md` (section 9.6 migration rule). Their status is asked to the user.

## [0.10.0] - 2026-10-15

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
