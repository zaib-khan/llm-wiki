### 9.4 Lint — health check

**Trigger:** on demand (`lint`), and the agent **suggests** a lint when the threshold is reached: **10 ingests or 30 days since the last lint, whichever comes first** (configurable).

**Checks:**
- contradictions between pages;
- stale claims superseded by newer sources (may propose archiving the page, section 6);
- orphan pages (no inbound links);
- important topics mentioned without their own knowledge page;
- missing cross-references;
- gaps that a web search could fill;
- `CLAUDE.md` and `AGENTS.md` are identical;
- file names are unique across the wiki;
- pages follow their template (frontmatter, sections): all sections for most types; for `contact` and `company` pages, only the order and names of the sections present are checked, missing sections are not flagged;
- no link points to a folder or to a non-note file, and no empty note was created by mistake;
- no empty or useless subfolders (except the permanent system folders `raw/processed/`, `raw/assets/`, and `wiki/log/`, which are ignored by this check);
- files waiting in `raw/` for a long time;
- projects that seem inactive (propose to close and archive them);
- pages not updated for a long time (`user.md`, contact pages…), ignoring `archived` pages;
- every page is connected to `user.md`, directly or indirectly;
- every contact and company page links to its list (`<domain>-contacts.md`, `<domain>-companies.md`), and every list includes all pages of its folder;
- every contact page meets the contact rules (a name and a way to reach them, or marked as family);
- how-tos: `outdated` ones (may propose archiving them), `writing` ones not updated for a long time (suggest resuming them), `draft` ones never tested; `status` and its `howto/<status>` tag always match;
- pages of a domain with domain-specific fields (section 6) have those fields, with allowed values, and their mirrored tags match;
- a newer version of this prompt is published (section 9.6): if so, the lint report says so and suggests `update wiki`.
- wikilinks inside a markdown table escape the pipe of their alias: `[[page\|Name]]`, never `[[page|Name]]` (Obsidian's table formatting breaks the unescaped form);
- no wikilink points to a deleted page, including in `wiki/log.md` and the archived logs in `wiki/log/`. When pages are deleted, their wikilinks in the log are turned into plain text (the name is kept, the link is removed); otherwise a click in Obsidian creates empty notes at the root. This is the only edit allowed in the append-only log.

**Fixes:**
- **Mechanical, safe fixes** are done automatically: links, index, orphans, template formatting, empty folders.
- **Content decisions** need the user: contradictions, stale claims, merging or deleting pages.
- **Web searches** follow the Query rule: permission before searching, permission before integrating.

**Proactive part — the lint also brings:**
- questions to complete the wiki ("You often mention X, but I know nothing about…");
- sources worth looking for;
- 💡 insights: recurring patterns, links between domains, forgotten ideas worth revisiting;
- confused ideas to clarify together.

**Asking and skipping questions:** questions are asked according to the question style (section 15). The user may skip any question. Skipped questions are stored in the open questions files (section 11.3) and asked again at the next lint or at any other time. Once answered, they are removed.

The lint ends with a report, is logged (`lint`), and is followed by a commit proposal.

### 9.5 Project lifecycle

- **Start:** a project is created in its domain, `wiki/<domain>/projects/<project>/`, or in `wiki/projects/<project>/` when it is cross-domain with no main domain (proposed by the agent or asked by the user; section 5.6).
- **End:** when the user says a project is finished, or after the user accepts a lint proposal: bring long-term value up into the domains, then move the project to `wiki/archive/` (and its raw sources accordingly). Logged as `archive`.

### 9.6 Update — keeping the wiki in line with new versions of this prompt

This document evolves. A wiki created with an older version keeps its old rules until it is updated.

**Versioning.**
- This document carries a version (`Version: X.Y.Z`, at the top), following `MAJOR.MINOR.PATCH`: PATCH for clarifications with no impact on the wiki, MINOR for new rules or templates with a simple migration, MAJOR for structural changes.
- The source repository publishes each version as a **git tag** (`vX.Y.Z`) and describes what changed in `CHANGELOG.md`.
- The wiki stores, in `settings.md`, the version it applies (`prompt_version`) and where the prompt comes from (`prompt_source`, by default `https://github.com/zaib-khan/llm-wiki`).
- The wiki keeps a copy of the applied prompt in `.llm-wiki/prompt-<version>.md`. It is the reference used to detect the user's customizations. `.llm-wiki/` is a hidden folder, so Obsidian does not show it.

**Trigger:** on demand (`update wiki`, or `/update_wiki` in Claude Code). The lint also checks for a newer version and suggests an update (section 9.4).

**The procedure is written once, in `CLAUDE.md` and `AGENTS.md`**, so it works with any agent. In Claude Code, the skill `.claude/skills/update_wiki/SKILL.md` is only a shortcut: it tells the agent to apply the `update wiki` procedure of the schema, without repeating it.

**Procedure:**

1. **Check the versions.** Read `prompt_version` in `settings.md`. Find the **latest tag** of `prompt_source` (only tagged versions count; untagged changes on the main branch are ignored). If both are equal, say the wiki is up to date and stop.
2. **Read what changed.** Fetch the new version of this document and `CHANGELOG.md` at that tag, and list the changes between the two versions.
   - **Unknown version** (no `prompt_version` or no copy in `.llm-wiki/`): compare the whole wiki (schema, templates, `command.md`, `settings.md`, structure) with the new version. Without the copy, the agent cannot tell a user customization from an old rule of the prompt (e.g. automatic commits instead of proposed commits). So **every difference is presented as a possible conflict, one at a time**: the current version and the new version side by side, with the question "Is this your personal choice (keep it) or an old rule (replace it)?". If the user does not know, the new version is applied. Step 3 is skipped; the answers replace it.
3. **Detect customizations** by comparing three versions: the copy in `.llm-wiki/` (what was applied), the current wiki (what the user has now), and the new version. Anything that differs between the copy and the current wiki is a user customization.
4. **Secure the wiki before changing anything.**
   - **With git:** ask the user to commit their pending changes first, so everything can be undone.
   - **Without git:** copy the whole wiki to `../<wiki-name>_backup/` (next to the wiki, outside Obsidian, qmd, and the lint). A new backup replaces the previous one. Record its date in `settings.md`.
5. **Present the changes and get validation.** Questions to the user follow the question style (section 15).
   - **Simple changes** (new rule, new command, updated template, new setting): validated all at once.
   - **Changes touching the user's content** (moving, renaming, or modifying existing pages and files): validated one by one, each with an explanation.
   - **Migrating pages to a new template** (e.g. an old type replaced by a new one):
     - **Map the sections:** each old section is matched with the new section that has the same meaning (e.g. "Who" → "Identity", "Organization" → "Work", "History" → "Interaction history"). Old sections with no match are kept at the end of the page, unchanged.
     - **Validate the mapping once per template:** the agent shows the mapping table (old section → new section) and waits for the user's validation, then applies it to every page of that type. Special cases (e.g. a contact that does not meet the rules of section 5.5) are still validated one by one.
     - **Do not add empty sections**, unless the new template requires all its sections (section 6).
     - **Fill new frontmatter fields only when they can be deduced from the page's content**; otherwise leave them out.
     - **Keep all content and all links**: migrating a page never deletes information.
   - **Conflicts with a customization:** show the user's version and the new version side by side; the user chooses.
6. **Apply** the validated changes: `CLAUDE.md` and `AGENTS.md` (always identical), templates, `command.md`, `settings.md`, structure, and pages. Re-index search.
7. **Finish.** Update `prompt_version` in `settings.md`, replace the copy in `.llm-wiki/` with the new version, log the operation (`update`), and propose a commit (if git is used).
8. **Report.** Summarize what changed. Then:
   - **Without git:** explain that a backup was created in `../<wiki-name>_backup/`, and that the user can ask the agent to restore the previous state if the update does not suit them or broke something.
   - **For everyone:** briefly mention that problems can be reported by opening an issue on the source repository. **Remind the user never to paste wiki content in a public issue** (the wiki holds personal data): describe the problem only.

**If the user reports a problem after an update** ("it broke", "restore the previous state"): restore the previous state (git revert, or the backup), then suggest more strongly to open an issue on the source repository, with the same reminder about personal data.

**Backup cleanup:** the first time the agent is used more than 5 days after a backup, it asks the user before deleting `../<wiki-name>_backup/`.

---

## 11. Index, Log, and Open Questions

### 11.1 `wiki/index.md`

The full catalog of the wiki, organized by domain and type. Updated at every operation that creates or changes pages. When answering a question, the agent reads it first. Each entry contains:

- the link `[[page]]`;
- a one-line summary;
- the type;
- the creation date;
- the last update date;
- the number of sources feeding the page;
- tags (an `archived` page is marked as archived).

In addition, **each domain page lists its own pages**, so the agent can navigate both globally and domain by domain.

### 11.2 `wiki/log.md`

An append-only chronological record. Each entry starts with a consistent header, so the log stays parseable with simple tools (`grep "^## \[" wiki/log.md | tail -5`):

```
## [YYYY-MM-DD HH:MM] type | Title
Short summary (1–3 lines).
- Pages created: [[...]], [[...]]
- Pages modified: [[...]]
- Sources: raw/processed/...
```

**Event types:** `ingest`, `query` (only queries that used the wiki), `lint`, `capture`, `schema`, `domain`, `archive`, `user`, `manual`, `init`, `update`.

**Monthly rotation:** `log.md` holds the current month. When a new month starts, its content is moved to `wiki/log/YYYY-MM.md` and `log.md` starts empty.

### 11.3 Open questions

Questions waiting for the user's answer (skipped during a lint or an ingest, or born from the welcome interview) are split by domain, so no single file holds questions about everything.

- **Per domain, subdomain, and project:** each one has its own file, named `<name>-open-questions.md` and placed in its folder (e.g. `wiki/family/family-open-questions.md`, `wiki/work/company/company-open-questions.md`, `wiki/family/projects/japan-trip/japan-trip-open-questions.md`). The prefix keeps file names unique. Each question has its date and the related page.
- **Root file `wiki/open-questions.md`:**
  - a **General** section for questions about the user (`user.md`) or spanning several domains;
  - **links to the domain and project files that still have open questions**.
- **Links follow the hierarchy:** the root links to domains and projects, and a domain file links to its subdomains' files, like the index.
- **Created only when needed, deleted when empty:** a `<name>-open-questions.md` file is created with its first question. When all its questions are answered, the file is deleted and the link to it disappears from the parent level.

---

