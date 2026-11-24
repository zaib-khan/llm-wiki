# Changelog

All notable changes to the LLM Wiki prompt (`zaib-khan-llm-wiki.md`) are documented here.
A wiki applies these changes with the `update wiki` command (`/update_wiki` in Claude Code).
Only tagged versions (`vX.Y.Z`) are proposed as updates.

Versions follow `MAJOR.MINOR.PATCH`:
- **PATCH**: clarifications, no impact on the wiki.
- **MINOR**: new rules, templates, or commands; simple migration.
- **MAJOR**: structural changes; pages or folders may move.

## [Unreleased]

## [0.15.0] - 2026-11-24

### Changed
- Navigation by domain pages (sections 4, 5.1, 5.4, 6, 7, 8, 9.2, 9.3, 9.4, 11.1, 12, 16): there is no full catalog and no per-domain index any more. `wiki/index.md` lists only the main domains (link + summary of 1 to 3 lines), the general pages (`user.md`, `open-questions.md`, the dashboard written as code) and the cross-domain projects; it changes only when a main domain is created, renamed, or archived, or when its summary changes. Each domain, subdomain, or project page becomes the navigation page of its level, with these sections in order, always present: Overview (at most 15 non-empty lines, no minimum) · Subdomains and projects (link + one-line summary) · Pages (by type, link + one-line summary) · Contacts and companies (links to the lists only) · Key facts (at most 20 points, no minimum; a finished project gets one "Outcome" line) · Open points (link to the open-questions file only). A domain page lists only its direct pages and direct subdomains or projects, never the pages of its subdomains; every page is listed exactly once, by the page of its own domain, except contact and company pages (listed by their lists), open-questions files (linked from Open points) and the domain page itself (listed by its parent or by `index.md`). A subdomain or project without its own contacts or companies links to its parent's lists. When a page is created, renamed, moved, or deleted, or its summary changes, only the page of its domain is updated; an overflowing overview or key facts list goes to a `synthesis` page of the domain. Search order: qmd first, otherwise the tree `index.md` → domain → subdomain → page, then grep. The lint checks these rules instead of the index size. Reason: the index (and the per-domain indexes) duplicated the domain pages, which doubled the token cost of navigation. The "Index size" setting and the index split rule are removed.

### Migration from 0.14.0
- Commit the pending changes first (the update's safety commit, step 4 of section 9.6).
- Rewrite every domain, subdomain, and project page with the new templates (section mapping validated once per template, section 9.6), reusing the one-line summaries of the old index (`wiki/index.md` or `<domain>-index.md`).
- Content that fits no new section, or that exceeds the overview or key facts limits, goes to a `synthesis` page of the domain, linked from the domain page.
- Questions written inline in domain or project pages move to that level's open-questions file; when their date is unknown, the agent writes "original date unknown" (in the wiki's language), never an invented date.
- Every page that was listed only in an index is added to the page of its own domain.
- Rewrite `wiki/index.md` with the main domains, general pages, and cross-domain projects only.
- Delete the `<domain>-index.md` files and the links to them; remove the "Index size" row from `settings.md`.
- No link and no information may be lost: before committing, check that every page is still reachable from `wiki/index.md` through the domain pages (lint navigation check).

## [0.14.0] - 2026-11-24

### Changed
- Always commit (section 14): every task that changes files ends with a commit (proposed or made, according to the commit mode) before the final report, including small edits, sub-agents' work, and any conversation, whatever the agent. Uncommitted changes make the `git diff` read at the start of every operation grow, which slows every agent down. A plain question creates no commit.
- No more log (sections 4, 5, 7, 8, 9, 11, 12, 14, 15, 16): `wiki/log.md` and `wiki/log/` are removed; commit messages are now the only history of the wiki. It cost many tokens, was rarely read, and git already keeps everything. Each operation that used to be logged as `x` is now committed as `x:`. Commit message format: first line `<type>: <short title>` (same types as the former log); a body proportional to the work (1–3 lines for a small commit, up to 5–7 for an ingest, lint, schema change, or update) with what was done and why, the sources (`raw/processed/...`), decisions, open questions, and what is not done or not verified, without listing the modified pages; a last line of at most 10 keywords after a label in the wiki's language (`Keywords:` by default), each keyword being exactly the file name of a wiki page (domain, subdomain or project, people and companies with a page), so `git log --grep` finds everything. History is read with `git log`; undoing uses `git revert` or restoring files. The lint threshold (10 ingests or 30 days) is found with `git log --grep '^lint:'` and `'^ingest:'`. The lint no longer checks links in the log. Section 11.3 (open questions) becomes 11.2.
- Without git: no history of operations. The date of the last operation (`settings.md`, "Last operation") is used to detect manual edits, and the date of the last lint (`settings.md`, "Last lint") to suggest a lint after 30 days.

### Migration from 0.13.0
- Commit the pending changes first (the update's safety commit, step 4 of section 9.6).
- Delete `wiki/log.md` and `wiki/log/`: with git, their content stays in the history. Without git, the agent asks the user before deleting them (their only copy is then the update backup).
- Remove the links to these pages (in pages, the schema files, `command.md`) and their `.gitkeep`; remove the "Log format" and "Log rotation" rows from `settings.md`.
- Without git: add "Last operation" and "Last lint" to `settings.md` (date of the last lint taken from the old log before deleting it, if any).

## [0.13.0] - 2026-11-10

### Added
- Interaction needs (sections 4, 7, 8, 9.4, 16): the welcome interview asks one optional question about a difficulty that should change how the agent talks to the user (dyslexia, ADHD, or similar); the user may also mention it at any time. If so, the agent says it will research it and does a thorough web search (the answer counts as permission), saves the sources in `raw/` and integrates them as a `knowledge` page, then writes short, concrete interaction guidelines into `CLAUDE.md` and `AGENTS.md`, applied in every session. Scope: conversation, questions and reports only; wiki pages keep full detail. The schema holds only how to interact, nothing medical; the difficulty is recorded in `user.md` (Health & wellbeing) only if the user agrees. The user can change the guidelines at any time (logged `schema`); the lint occasionally asks whether they still help. Migration: at update, the agent asks the user the new optional question once.

### Migration from 0.12.0
- Interaction needs: at update, the agent asks the user the new optional question once.

## [0.12.0] - 2026-11-10

### Changed
- Large index (sections 9.4, 11.1, 16): when `wiki/index.md` becomes too large to read efficiently (default about 50 KB, configurable in `settings.md`, "Index size"), the lint proposes to split it by domain: each domain gets `<domain>-index.md` in its folder (same entry format), and `wiki/index.md` keeps only an overview with links to the domain indexes, plus cross-domain projects and general pages. Applied only after validation; the index rules then apply to each domain index, and the agent reads the root index, then the relevant domain index, when answering. Migration: none; the split is proposed by the lint when the threshold is reached.
- Forgotten temporary files (section 9.4): the lint check on forgotten update review files (`changes-<version>.md` or its translation) now covers any temporary file the agent created and should have deleted (e.g. other temporary notes). The agent flags them and asks before deleting them. Migration: none.
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

### Migration from 0.11.0
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
