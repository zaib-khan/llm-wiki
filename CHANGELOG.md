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
- Untitled files (section 9.4): the lint flags files created by mistake with a default name ("Untitled", "Untitled 1", or the localized equivalent such as "Sans titre"), whatever their extension (`.md`, `.base`, `.canvas`…), anywhere in the wiki. The agent shows their content (often empty) and asks the user before deleting them. Migration: none.
- Valid YAML frontmatter (section 9.4): the lint checks that every page's frontmatter is valid YAML (unclosed quotes, broken lists…), since Obsidian, Bases and queries cannot read a broken one. Fixing the syntax without changing any value is a mechanical fix, done automatically. Migration: none; broken frontmatter is fixed at the next lint.
- Personal integrations (section 5.9): when the user wants the agent to use a personal tool on its own (task manager, calendar, e-mail tool), the agent, after validation, creates the skill in two identical copies (`.claude/skills/<name>/`, `.agents/skills/<name>/`), adds a trigger rule (the user's phrasings, even without naming the skill) referenced from both `CLAUDE.md` and `AGENTS.md`, adds a row to `settings.md` and the command to `command.md`, and logs `schema`. Credentials and tokens never go into the wiki. The word used to ask the agent for work (e.g. "task") alone does not trigger an integration. Migration: none.
- Agent folders explained (section 5.8): `.claude/` holds Claude Code's `skills/` (identical copies in `.agents/skills/` for Codex and other agents), `rules/` (Claude Code only; a rule for every agent is referenced from both `CLAUDE.md` and `AGENTS.md`) and `hooks/` (inactive until activated in Claude Code's settings, only after validation). Scripts stay in `scripts/`. No agent subfolder is created in advance: each is created with its first file, plus a short README in the wiki's language; the lint flags empty agent folders. Migration: none; empty agent folders created in advance may be removed during the lint, after validation.
- Skills for Claude Code and Codex: every skill of the wiki (starting with `update_wiki`) exists as two real files with identical content, `.claude/skills/<name>/SKILL.md` (Claude Code) and `.agents/skills/<name>/SKILL.md` (Codex and other agents), created at first launch whatever the agent used. No symbolic link; whenever one copy changes, the other changes the same way. The lint checks that both copies are identical. Migration: at update, the agent creates `.agents/skills/update_wiki/SKILL.md` as an identical copy of the Claude Code one.
- Split prompt authoring into seven thematic files in `prompt/`. A dependency-free Python script assembles the same complete prompt, preserving its text and section order; `--check` detects an outdated generated file.
- Ingest checks for partially processed sources, completes each source before moving it, and resumes interrupted work without duplicating pages or facts. Sources needing a filing decision stay pending while independent sources continue.
- Projects attached to a domain or subdomain now live inside it (`wiki/<domain>/projects/<project>/<project>.md`, `projects/` being a reserved name); the domain page and template list its projects. `wiki/projects/` is kept only for cross-domain projects without a main domain.
- Per-domain filing rules: when it is unclear where content belongs among a domain's subdomains or projects, the agent proposes a short filing rule; once validated, it is recorded in `settings.md` ("Filing rule (<domain>)") and applied at every ingest and capture without asking again.
- Domain-specific frontmatter fields: a domain may have its own extra fields (e.g. `amount`, `due_date`, `status` for bills). The agent proposes them; once validated, they are recorded per domain in `settings.md`, filled on new and updated pages when known, and checked by the lint. When tags mirror a field, the field is the reference.
- Outdated pages: a page that is no longer useful but worth keeping gets the tag `archived` after the user's validation (the agent may propose it). It stays in place with its links and index entry (marked as archived), is no longer used to answer except for history, and is ignored by the lint's staleness check. Distinct from `wiki/archive/` (finished projects).
- Optional "to try" / "tried" domain pattern: when the user collects many things to try, the agent may suggest a "to try" domain feeding a "tried" domain; tried items are kept (moved) or dropped (left with the reason). A suggestion, not a rule; domains still need validation.
- Web page extraction: ingest (and saving web-search results to `raw/`) uses Defuddle first (`npx -y defuddle parse <url> --md`, `--json` for title, author, and date), with a plain fetch as fallback. Video transcripts and other content are unchanged.
- Sub-agents for a large ingest (optional, section 9.2): when the agent can launch sub-agents, independent sources may be processed in parallel, one sub-agent per source. Sub-agents write only their source's own pages and report back; only the main agent writes shared files (index, log, domain and list pages, `user.md`, open questions), asks the user's questions at the end, and commits. Sources touching the same existing page are handled sequentially; each source is still completed as a unit.
- Question style setting: at first launch, the welcome interview asks whether the user prefers questions one at a time or all together in a list (recorded in `settings.md`, "Question style": `one by one` or `list`; default `one by one`). It applies wherever the agent asks several questions (end of ingest, lint, update, open questions review). In both styles, each question keeps the context needed to answer it. The user can change it for good or just for the current batch.
- Commit mode and push frequency: at first launch, when git is used, the welcome interview asks (after the remote) whether the agent should propose each commit or commit on its own ("Commit mode": `propose`, default, or `automatic`, recorded in `settings.md`), and how many commits between pushes ("Push frequency": N, default 5; 1 = after every commit). `propose`: commits and pushes are proposed for validation; `automatic`: the agent commits at the end of each operation and reports the hash, and pushes are done and reported. Pending commits are also pushed at the end of a work session. No remote: commits only. Both settings can be changed at any time.
- "I don't know" answers: an open question answered "I don't know" is closed. The related page records the information as unknown with the date (e.g. "Current medication: unknown (2026-11-08)"), the question leaves the open questions files and is not asked again, unless a new source brings the information. Skipping ("not now") still keeps the question open.
- Update safety and review: with git, after the user's pending changes are committed, the update creates a local tag `pre-update-<version>` on that commit and tells the user that `git reset --hard pre-update-<version>` undoes the whole update. After applying, the agent creates a temporary review checklist at the wiki root (`changes-<version>.md`, named in the wiki's language), listing every applied change with a checkbox plus the safety commit and tag; the user ticks or comments, the agent undoes or adjusts refused points, then deletes the file. The lint flags a forgotten review file.
- Obsidian Bases dashboard: at first launch the agent creates `wiki/dashboard.base` (core Bases plugin, enabled in `core-plugins.json`) with five generic views: recently updated, how-tos by status, dormant pages (over 60 days, contacts and companies excluded), orphans (`user` excluded), contacts as cards. View and column names are in the wiki's language. When a domain gets its own fields, the agent may propose a dedicated view (e.g. bills by due date with a total). Bases is the recommended tool for dynamic tables; Dataview stays optional. The lint never flags the dashboard as an orphan or empty note.
- Obsidian skills: at first launch, the agent proposes to install kepano's Obsidian skills (`npx skills add https://github.com/kepano/obsidian-skills`), only after validation and only if it supports skills. Once installed, it uses `obsidian-markdown`, `obsidian-bases`, `json-canvas` and `defuddle` when writing pages, bases, or canvases. If installation fails or is declined, nothing changes.
- Obsidian configuration: `app.json` gets `"alwaysUpdateLinks": true` (links are updated automatically, without asking, when a page is renamed or moved). When git is used, `.gitignore` also ignores `.obsidian/cache` and `.trash/` (Obsidian's cache and trash).

### Migration
- The source split requires no wiki migration: installation, tagged updates and the saved prompt copy still use `zaib-khan-llm-wiki.md`.
- No file migration. Existing wikis adopt this ingest procedure when they update the schema.
- Update safety tag and review checklist: none. If old `changes-*.md` review files from earlier updates are still in the wiki, the agent asks the user and deletes them.
- Projects attached to a domain: projects currently in `wiki/projects/` that clearly belong to one domain are proposed to the user one by one and, after validation, moved to `wiki/<domain>/projects/<project>/` (their raw sources move to `raw/processed/<domain>/projects/<project>/`), and the domain page links them. Wikilinks resolve by file name, so links keep working. Cross-domain projects stay in `wiki/projects/`.
- Filing rules: none needed. Existing wikis adopt them when they update; rules are added to `settings.md` as filing questions arise.
- Domain-specific fields: none needed.
- Archived tag: none needed.
- To-try / tried pattern: none needed.
- Defuddle: none needed. Existing wikis adopt it when they update.
- Sub-agents for ingest: none.
- Question style: existing wikis get the "Question style" setting in `settings.md` at update; the agent asks the user the question once (default `one by one`).
- "I don't know" answers: none.
- Commit mode and push frequency: existing wikis keep their current behavior until updated. At update, the agent asks the two questions once (commit mode, push frequency) and records the answers in `settings.md`.
- Obsidian Bases dashboard: at update, after validation, the agent creates `wiki/dashboard.base` (translating view and column names, adding views for domains that already have their own fields if the user wants) and adds `bases` to `.obsidian/core-plugins.json`.
- Obsidian skills: at update, the agent proposes installing kepano's Obsidian skills; installed only after validation and if the agent supports skills.
- Obsidian configuration: at update, add `"alwaysUpdateLinks": true` to `.obsidian/app.json`, and (when git is used) `.obsidian/cache` and `.trash/` to `.gitignore`.

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
