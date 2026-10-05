# LLM Wiki — A Second Brain Built and Kept by Your Agent

A pattern for building a personal knowledge base — a second brain — with an LLM agent.

This is a source file. Give it to your LLM agent (Claude Code, Codex, OpenCode, Cursor, or any other). The agent will read it, ask you a few short questions, and build your wiki with you: the folder structure, the templates, and the schema files (`CLAUDE.md` and `AGENTS.md`) that will guide every future session. The rules below are defaults: precise enough to be applied as-is, and every one of them can be changed to fit you.

---

## 1. Why

Too much information reaches us every day. Articles, videos, conversations, documents — and our own thoughts. The result is familiar: details get forgotten, we no longer remember where something came from, ideas become confused, focus is lost. A great idea appears, then vanishes after the next website or video.

The goal of this wiki is to **get as much as possible out of your head and into a place you can trust**. Once it is written down and organized, your mind is free to focus on what matters, and you keep a reliable trace of your thoughts, your ideas, and what you have read or seen — with their sources.

And because the wiki holds the context of your whole life (you, the people around you, your work, your projects, your ideas), the agent can see what you miss: a link between two ideas, a forgotten detail, a pattern that keeps coming back. A detail from your private life may hold the key to a professional question, and the other way around.

Why does it work where personal wikis usually fail? The hard part of a knowledge base is not reading or thinking — it is the bookkeeping: updating cross-references, keeping summaries current, noting contradictions, staying consistent across hundreds of pages. Humans abandon wikis because this maintenance grows faster than the value. An LLM does not get bored, does not forget to update a link, and can touch fifteen files in one pass. The cost of maintenance drops to almost zero, so the wiki stays alive.

Unlike retrieval-based systems (RAG) that rediscover knowledge from scratch on every question, this wiki is **compiled once and kept current**. Every source you add and every question you ask makes it richer.

---

## 2. The Library

Think of the wiki as **a library that grows over time**.

- **The user is the owner of the library.** The owner decides which books, articles, notes, and ideas enter it.
- **The agent is the librarian.** The librarian classifies everything according to clear rules, keeps the shelves in order, and finds the right book, article, or answer for the task at hand.
- **A good librarian also knows the owner.** They bring back an old forgotten notebook when it becomes relevant, notice connections between two books, and ask questions to fill the empty shelves.

---

## 3. Core Principles

The agent must follow these principles at all times:

1. **Keep it as simple as possible.** Never create a folder, file, or structure that is not needed yet.
2. **Sources are immutable.** Everything that enters `raw/` is never modified in content. Files may be renamed and moved, never rewritten.
3. **Everything goes through a raw source first.** Even an idea spoken in conversation is first saved as a raw source, then integrated into the wiki.
4. **The structure is defined, not improvised.** The agent files content according to the rules of this document, not according to its own taste. The user must always be able to find their way.
5. **The agent proposes, the user validates** for every structural or sensitive decision: new domains and subdomains, new person pages, schema changes, keeping a query answer, web searches, commits and pushes.
6. **`user.md` is the center of everything.** Every page is connected to it, directly or indirectly.
7. **Language.** The wiki content, `command.md`, and the templates' content are written in the user's preferred language. The schema files (`CLAUDE.md`, `AGENTS.md`, `settings.md`) are written in English. System files and folders keep English names (see section 5).
8. **Transparency.** The agent always reports what it created, changed, or deleted.

---

## 4. Roles

**The user (owner):**
- decides what enters the library (drops sources, tells ideas);
- explores the wiki and asks questions;
- validates the agent's proposals;
- may make **small edits** directly in the wiki. Larger changes should go through the agent.

**The agent (librarian):**
- writes and maintains the whole wiki: summaries, entity and concept pages, syntheses, cross-references, index, log;
- classifies everything according to the rules;
- finds and synthesizes answers, with citations;
- keeps the wiki consistent and healthy.

**The agent is also proactive. It must:**
- ask the user questions to complete the wiki ("You mentioned X — can you tell me more?");
- remind the user of forgotten ideas, especially when they are relevant to the current question;
- help clarify ideas that are still confused;
- spot what escapes the user: links between ideas or domains, recurring patterns, weak signals, overlooked details.

**Manual edits by the user:** at the start of each operation, the agent detects manual changes (via git, or via file modification dates when git is not used). It treats them as true, propagates them where needed (index, links, related pages), and reports any contradiction they create with other pages.

---

## 5. Architecture

### 5.1 Overview

```
my-wiki/
├── CLAUDE.md              ← schema (always identical to AGENTS.md)
├── AGENTS.md              ← schema (always identical to CLAUDE.md)
├── settings.md            ← user settings (see section 15)
├── command.md             ← commands the user can give the agent (see section 7)
│
├── raw/                   ← inbox: everything arrives here
│   ├── assets/            ← temporary: images downloaded by the agent
│   └── processed/         ← processed sources, mirroring the wiki structure
│
├── templates/             ← one template per page type
│
└── wiki/
    ├── index.md           ← full catalog of all pages
    ├── log.md             ← log of the current month
    ├── log/               ← archived monthly logs (YYYY-MM.md)
    ├── open-questions.md  ← general questions + links to domain question files
    ├── user.md            ← the center of the wiki
    ├── <domain>/          ← one folder per domain (named with the user's word)
    ├── projects/          ← ongoing, time-bound projects
    └── archive/           ← finished projects
```

### 5.2 The three layers

1. **Raw sources (`raw/`)** — the source of truth. Articles, PDFs, videos, images, audio, conversations, ideas. Immutable.
2. **The wiki (`wiki/`)** — markdown pages written and maintained by the agent.
3. **The schema (`CLAUDE.md`, `AGENTS.md`, `settings.md`, `templates/`)** — the rules, conventions, workflows, and settings that make the agent a disciplined librarian.

### 5.3 `raw/` — the inbox

- Everything is dropped flat into `raw/`, all domains and formats mixed.
- After processing, each source is **moved** to `raw/processed/`, into a folder structure that **mirrors the wiki**. Example: a source about the user's father (wiki page `wiki/family/entities/dad.md`) goes to `raw/processed/family/`.
- A source that concerns several domains is filed under its **main domain**. Pages in other domains link to it.
- `raw/assets/` is a temporary area for images downloaded by the agent from the web. When the related article is processed, its images follow it into `raw/processed/<domain>/`.
- **The original file name is a hint.** A file dropped as `dad.jpg` tells the agent it relates to the user's father. The agent reads the original name to understand the file, then renames it during ingest.
- **Naming:** during ingest, every raw file is renamed to `YYYY-MM-DD-short-title.ext` (the date the source was added). The content is never changed.
- **Permanent system folders:** `raw/processed/`, `raw/assets/`, and `wiki/log/` are part of the structure even when empty. Git does not track empty folders, so if one is missing (e.g. after a clone), the agent simply recreates it.
- **Non-text sources** (PDF, images, audio, video): the original is kept, and the agent creates a markdown text version next to it (extraction, transcription, or description), with the same base name. The text version is used for integration.

### 5.4 `wiki/` — domains

- **A domain is a folder.** Each domain folder contains a domain page with the same name: `wiki/family/family.md`. The domain page gives an overview and lists all pages of the domain.
- Domains are **chosen by the user** (family, work, health, a hobby — anything). Domain folders are named **exactly with the word the user gives**, whatever its language (e.g. "work" stays `work/` in a French wiki): no translation, no confirmation needed. The agent only checks the spelling: if it spots a typo, it proposes the corrected name before creating the folder.
- **Subdomains** follow exactly the same rule, recursively: `wiki/work/company/company.md`.
- **No depth limit**, with two safeguards:
  - **file names are unique across the whole wiki** (wikilinks resolve by file name — two `marc.md` files would make `[[marc]]` ambiguous; use `marc-dupont.md` and `marc-cousin.md`);
  - **a subdomain is created only when it is justified** (enough pages on the subject, or at the user's request).
- **Creating a domain or subdomain:** the agent may propose one (e.g. "I have 8 pages about your team — shall I create `work/team/`?"). Nothing is created without the user's validation.

### 5.5 Type subfolders

Inside a domain, pages are grouped in type subfolders, **created only when the first page of that type exists**:

```
wiki/family/
├── family.md
└── entities/
    ├── dad.md
    └── mom.md
```

Type subfolders keep English names and are reserved (never used as domain names): `sources/`, `entities/`, `concepts/`, `syntheses/`.

Inside `entities/`, people and companies have their own subfolders, also created only when needed. Other entities stay directly in `entities/`:

```
wiki/work/
└── entities/
    ├── personne/        ← person pages
    │   └── marc-dupont.md
    ├── companies/       ← company pages
    │   └── acme.md
    └── jira.md          ← any other entity
```

`personne/` and `companies/` are reserved names too.

### 5.6 Projects and archive

- Time-bound topics (reading a book, planning a trip, a research of a few weeks) live in `wiki/projects/<project>/`, with a project page `<project>.md`, following the same rules as domains.
- When a project is finished: the agent first **brings what has long-term value up into the relevant domains** (a lesson learned, a fact about a person, a reusable idea), then **moves the project to `wiki/archive/`**. Its raw sources follow the same move in `raw/processed/`.

### 5.7 Naming rules (summary)

| Item | Rule |
|---|---|
| System files and folders | English: `user.md`, `index.md`, `log.md`, `open-questions.md`, `<name>-open-questions.md`, `settings.md`, `command.md`, `raw/`, `processed/`, `assets/`, `templates/`, `wiki/`, `projects/`, `archive/`, type subfolders |
| Domains and subdomains | The word given by the user, as is (spelling checked) |
| Wiki page files | Lowercase, hyphenated, **unique across the wiki** |
| Raw files | `YYYY-MM-DD-short-title.ext` |
| Entity subfolders | `entities/personne/` (people), `entities/companies/` (companies) |
| Templates | `templates/template-<type>.md` (e.g. `template-user.md`), so they never share a name with a wiki page |

---

## 6. Page Types and Templates

The `templates/` folder holds one template per page type, named `template-<type>.md`: `template-user.md`, `template-domain.md`, `template-project.md`, `template-person.md`, `template-company.md`, `template-entity.md`, `template-concept.md`, `template-source.md`, `template-synthesis.md`. The prefix keeps file names unique across the vault (otherwise `templates/user.md` and `wiki/user.md` would make `[[user]]` ambiguous). The templates' section headings are written in the user's language. Every page the agent creates must follow its template. The user may edit the templates; the agent then follows the new version.

| Type | Purpose |
|---|---|
| `user` | The user: identity, situation, goals, values, preferences, health, psychology, relationships — the center of the wiki |
| `domain` | Overview of a domain or subdomain, with the list of its pages |
| `project` | A time-bound project: goal, status, dates, related pages |
| `person` | A person: identity, relationship to the user, contact, work, personality, history |
| `company` | A company: identity, activity, location, relationship to the user, organization, people known there |
| `entity` | Any other entity: place, object, tool, organization that is not a company |
| `concept` | An idea, topic, method, theory — including the user's own ideas |
| `source` | Summary of one raw source |
| `synthesis` | Comparison, analysis, overview, or a kept answer to a question |

**Every template starts with a YAML frontmatter**, at least:

```yaml
---
type: entity            # user | domain | project | person | company | entity | concept | source | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []             # links to raw files in raw/processed/
tags: []
---
```

**Extra frontmatter fields** (names stay in English so queries work in any language):

- **person**: `relationship`, `birthday`, `company` (link to the company page), `role`, `address`
- **company**: `relationship`, `industry`, `website`, `size`, `founded`, `address` (headquarters)

`address` is detailed as much as possible:

```yaml
address:
  street: ""
  postal_code: ""
  city: ""
  region: ""
  country: ""
```

Each template then defines its sections (headings written in the user's language). Suggested defaults:

- **user**: Identity · Current situation · Goals · Values & preferences · Health & wellbeing · Personality · Key people · Domains · History
- **domain**: Overview · Pages (by type) · Subdomains · Key facts · Open points
- **project**: Goal · Status · Timeline · Key information · Related pages · Outcome (when finished)
- **person**: Identity · Relationship to the user · Contact details · Work · Personality · Interests · Important dates · Close circle · Facts & information · Interaction history · Ideas & gifts · Links
- **company**: Identity · Activity · Size & figures · Location · Relationship to the user · Organization · People known there · Culture & values · Tools & methods · Competitors & partners · News & history · Facts & information · Links
- **entity**: Who / what · Relationship to the user · Facts · History · Links
- **concept**: Summary · Details · The user's view · Evolution · Related concepts · Sources
- **source**: Metadata (author, date, URL, format) · Summary · Key points · Pages updated · Quotes worth keeping
- **synthesis**: Question or purpose · Answer / analysis · Sources · Related pages

---

## 7. Schema Files

- The wiki has **two schema files: `CLAUDE.md` and `AGENTS.md`**, so that any agent can use it. They are two real files with **identical content**.
- **Whenever one is modified, the other must be modified in the same way, at the same time.** They must never differ.
- They contain the rules of this document, adapted to the user's choices, and reference `settings.md` and `templates/` as code, never as links (see section 13).
- **The schema evolves with the user.** When the agent sees that a new convention would help, it proposes the change; the user validates before anything is written.
- Every schema change is logged (`schema`).

### `command.md` — the user's command reference

At the root of the wiki, `command.md` lists **every command the user can give the agent**, so the user always knows what they can do. Each command has its name, its aliases, how to trigger it, and a short text explaining **what it does** step by step and what the user gets at the end. Default content:

| Command | What it does |
|---|---|
| `ingest` / `processRaw` | Processes every file waiting in `raw/`: reads it, renames it, writes a source page, creates or updates related pages, flags contradictions, updates the index, moves the file to `raw/processed/`, then reports and asks the pending questions at the end (section 9.2). |
| `lint` | Runs a health check of the wiki: fixes mechanical issues, asks about content issues, and brings questions, sources to look for, and 💡 insights (section 9.4). |
| Tell an idea | Just tell the agent a thought or an idea: it saves it as a raw source and asks whether to integrate it now or at the next ingest (section 9.1). |
| Ask a question | Ask anything: the agent answers from the wiki with citations and 💡 reminders, and offers to keep valuable answers or to search the web if the wiki is not enough (section 9.3). |
| `open questions` | Shows the open questions (general ones and those of each domain or project, section 11.3) so the user can answer them. The user can also ask for the questions of one domain only. |
| `new domain` / `new project` | Creates a domain, subdomain, or project after validation. |
| `close project` | Brings long-term value into the domains, then archives the project (section 9.5). |
| `settings` | Shows the current settings and lets the user change one (section 15). |
| `commands` | Shows the content of `command.md`. |

`command.md` must stay in sync with the schema: whenever a command is added, changed, or removed, the agent proposes the update of `command.md` together with `CLAUDE.md` and `AGENTS.md`.

---

## 8. First Launch

When the agent receives this document for the first time, it performs these steps in order:

1. **Short welcome interview.** The agent asks only these questions, **one at a time**, waiting for each answer before the next:
   1. **Language:** "Which language do you want your wiki in?"
   2. **Name:** "What is your name?" — nothing more. It creates `wiki/user.md` with the name only.
   3. **First domain:** "What first domain do you want to create?" (work, family, or anything else). It creates the domain folder and its domain page.
   4. **Git:** "Do you want to use git for your wiki?" If the answer is **no**, the agent does nothing related to git, now or later (section 14). If the answer is **yes**, it asks: "What is the link of your remote repository?" (the user may answer that there is none yet).

   That is all. Everything else (who the user is, other domains, settings) will come with time, through captures, ingests, and the agent's questions. Open questions that arise from the interview (e.g. the user's job, a short self-presentation) are added to the open questions (section 11.3). The defaults (section 16) apply until the user changes them.
2. **Create the structure:** `raw/` (with `processed/` and `assets/`), `templates/` (all `template-<type>.md` files), `wiki/` (`index.md`, `log.md`, `log/`, `open-questions.md`), `CLAUDE.md`, `AGENTS.md`, `settings.md`, `command.md`.
3. **Install search:** check whether qmd is already installed; install it only if needed. Create the wiki's collections with prefixed names and index them (section 12). If installation fails, explain why and fall back to the index plus grep.
4. **Configure Obsidian:** write the settings listed in section 13 to `.obsidian/` and give the user a step-by-step guide for the rest.
5. **Initialize git** (only if the user chose to use git): run `git init` only if the folder is not already a repository, and add the remote repository given by the user, if any (section 14).
6. **Log** the initialization and give the user a short summary of what was created, pointing to `command.md` to see what they can ask.

---

## 9. Operations

### 9.1 Capture — ideas told to the agent

When the user tells the agent an idea, a thought, or any information in conversation (without dropping a file):

1. The agent **saves a raw source first**: a dated file in `raw/` (`YYYY-MM-DD-short-title.md`) containing what the user said, **faithfully**. Transcription and typing errors are corrected; the meaning and the wording are not changed.
2. The agent **asks**: "Shall I integrate it now, or keep it for the next ingest?"
3. The capture is logged (`capture`).

Capturing an idea must cost the user almost nothing: no forms, no required structure.

### 9.2 Ingest — processing the inbox

**Trigger:** only on demand, when the user says `ingest` or `processRaw`.

**Rhythm:** the agent processes all sources in `raw/` **autonomously**. It only needs the user for things that require their judgment (contradictions, new domains or subdomains, new person pages, classification doubts). It **does not stop**: it sets these points aside and asks **all its questions at the end**.

**For each source, the agent:**

1. Reads it (for a non-text source, creates the text version first).
2. If the user gave a URL: fetches the content (article text, video transcript) and saves it as a raw source. Useful images (diagrams, charts) are downloaded to `raw/assets/`. If the content cannot be fetched, keeps the link with a note "content not retrieved".
3. Renames it to `YYYY-MM-DD-short-title.ext`.
4. Determines its main domain (and related domains).
5. Writes a `source` page.
6. Creates or updates the related entity, concept, and synthesis pages. A single source may touch 10–15 pages.
   - The agent **creates pages freely** inside existing domains.
   - **Exceptions requiring validation:** a new **person** page, a new domain, a new subdomain. Company pages are created freely.
7. Updates `user.md` freely when it learns something about the user — and **reports to the user exactly what was added, changed, or removed**.
8. Flags contradictions (section 10) and records the evolution of the user's ideas.
9. Adds all links (wikilinks) both ways where relevant.
10. Updates the domain pages and `index.md`.
11. Moves the source (and its assets) to `raw/processed/<main domain>/`.
12. Logs the ingest (`ingest`).

**After all sources, the agent re-indexes search and presents a report:**
- sources processed;
- pages created and modified;
- key points of each source;
- 💡 insights and links spotted;
- ⚠️ contradictions detected;
- changes made to `user.md`;
- pending questions (asked now).

Then it proposes a commit (section 14).

### 9.3 Query — answering questions

1. The agent reads `index.md` and the relevant domain pages, searches (qmd) across `wiki/` and `raw/processed/`, and reads the relevant pages.
2. It answers in **the format best suited to the question** (text, markdown page, table, Mermaid diagram, chart, Marp slides, Obsidian canvas…).
3. **Citations:** it cites both the wiki pages (`[[page]]`) and, when useful, the original raw sources.
4. **Proactive section:** when — and only when — something relevant exists, the answer ends with a dedicated section where each item starts with 💡: forgotten ideas related to the question, details from the user's life that shed light on it, links the user may have missed.
5. **Keeping valuable answers:** when an answer has lasting value (analysis, comparison, discovered connection), the agent proposes to keep it. If the user agrees, it creates a `synthesis` page in the relevant domain **and** saves a trace of the conversation in `raw/processed/<domain>/`.
6. **When the wiki is not enough:**
   1. the agent says so and **asks permission** to search the web;
   2. it proposes an answer;
   3. if the answer suits the user, it fetches the raw content of the sites or documents used and saves it to `raw/`;
   4. it **asks permission** to integrate these sources, then integrates them with all relevant links.
7. Queries that used the wiki are logged (`query`).

### 9.4 Lint — health check

**Trigger:** on demand (`lint`), and the agent **suggests** a lint when the threshold is reached: **10 ingests or 30 days since the last lint, whichever comes first** (configurable).

**Checks:**
- contradictions between pages;
- stale claims superseded by newer sources;
- orphan pages (no inbound links);
- important concepts mentioned without their own page;
- missing cross-references;
- gaps that a web search could fill;
- `CLAUDE.md` and `AGENTS.md` are identical;
- file names are unique across the wiki;
- pages follow their template (frontmatter, sections);
- no link points to a folder or to a non-note file, and no empty note was created by mistake;
- no empty or useless subfolders (except the permanent system folders `raw/processed/`, `raw/assets/`, and `wiki/log/`, which are ignored by this check);
- files waiting in `raw/` for a long time;
- projects that seem inactive (propose to close and archive them);
- pages not updated for a long time (`user.md`, person pages…);
- every page is connected to `user.md`, directly or indirectly.

**Fixes:**
- **Mechanical, safe fixes** are done automatically: links, index, orphans, template formatting, empty folders.
- **Content decisions** need the user: contradictions, stale claims, merging or deleting pages.
- **Web searches** follow the Query rule: permission before searching, permission before integrating.

**Proactive part — the lint also brings:**
- questions to complete the wiki ("You often mention X, but I know nothing about…");
- sources worth looking for;
- 💡 insights: recurring patterns, links between domains, forgotten ideas worth revisiting;
- confused ideas to clarify together.

**Skipping questions:** the user may skip any question. Skipped questions are stored in the open questions files (section 11.3) and asked again at the next lint or at any other time. Once answered, they are removed.

The lint ends with a report, is logged (`lint`), and is followed by a commit proposal.

### 9.5 Project lifecycle

- **Start:** a project is created in `wiki/projects/` (proposed by the agent or asked by the user).
- **End:** when the user says a project is finished, or after the user accepts a lint proposal: bring long-term value up into the domains, then move the project to `wiki/archive/` (and its raw sources accordingly). Logged as `archive`.

---

## 10. Contradictions and Evolution

**Contradictions between sources:** when new information contradicts what the wiki says, the agent:
1. flags it **visibly in the page**: `⚠️ Contradiction: [[source-a]] says A, [[source-b]] says B`;
2. **asks the user to decide** (during the ingest's final questions);
3. updates the page according to the decision and keeps the flag's resolution traceable.

**Evolution of the user's ideas:** a change of mind is not a contradiction — it is valuable information. When an idea A (January) has become idea B (June):
- the new version enters as a **new raw source** (the old one is never modified);
- the agent **links** the two;
- the page keeps a **visible, dated history** of the evolution, e.g. in an "Evolution" section: `2026-01 — A → 2026-06 — B`.

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
- tags.

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

**Event types:** `ingest`, `query` (only queries that used the wiki), `lint`, `capture`, `schema`, `domain`, `archive`, `user`, `manual`, `init`.

**Monthly rotation:** `log.md` holds the current month. When a new month starts, its content is moved to `wiki/log/YYYY-MM.md` and `log.md` starts empty.

### 11.3 Open questions

Questions waiting for the user's answer (skipped during a lint or an ingest, or born from the welcome interview) are split by domain, so no single file holds questions about everything.

- **Per domain, subdomain, and project:** each one has its own file, named `<name>-open-questions.md` and placed in its folder (e.g. `wiki/family/family-open-questions.md`, `wiki/work/company/company-open-questions.md`, `wiki/projects/japan-trip/japan-trip-open-questions.md`). The prefix keeps file names unique. Each question has its date and the related page.
- **Root file `wiki/open-questions.md`:**
  - a **General** section for questions about the user (`user.md`) or spanning several domains;
  - **links to the domain and project files that still have open questions**.
- **Links follow the hierarchy:** the root links to domains and projects, and a domain file links to its subdomains' files, like the index.
- **Created only when needed, deleted when empty:** a `<name>-open-questions.md` file is created with its first question. When all its questions are answered, the file is deleted and the link to it disappears from the parent level.

---

## 12. Search

- **qmd** (https://github.com/tobi/qmd) is installed at first launch: a local search engine for markdown with keyword (BM25) and semantic (vector) search plus LLM re-ranking, available as a CLI and as an MCP server — so it works with any agent.
- **Scope:** `wiki/` **and** `raw/processed/`, so a precise detail can be found even if it was not carried into the wiki.
- **Collection names:** qmd collections are global to the machine, so generic names like `wiki` or `raw` would clash with another wiki. Prefix them with the wiki's folder name: `<wiki>-wiki` (on `wiki/`) and `<wiki>-raw` (on `raw/processed/`).
- **Re-indexing:** after every ingest and after any change to the wiki or the sources, run `qmd update && qmd embed`. Run `qmd cleanup` if qmd reports orphaned chunks.
- **Fallback:** if qmd cannot be installed or fails, the agent uses `index.md`, the domain pages, and grep.
- **Other scripts:** when a mechanical task becomes repetitive (checking that `CLAUDE.md` = `AGENTS.md`, unique names, broken links, log rotation…), the agent may **propose** to write a small script in `scripts/`. Nothing is created without validation.

---

## 13. Obsidian

The wiki is designed to be read in **Obsidian**.

- **Links:** wikilinks `[[page-name]]` by default (this is why file names must be unique).
- **Never link to a folder or to a file that is not a note** (no markdown link, no wikilink). In Obsidian, clicking a link that leads to no note creates an empty note with that name. Folder paths and system file paths are written as code (`raw/`, `templates/`), never as links. This applies everywhere, including `CLAUDE.md` and `AGENTS.md`.
- **Recommended plugins and tools:**
  - **Obsidian Web Clipper** (browser extension): converts web articles to markdown; configure it to save into `raw/`.
  - **Dataview**: dynamic tables and lists from the templates' frontmatter (e.g. all family members, all ongoing projects).
  - **Templater** / core **Templates**: use the templates in `templates/` when editing by hand.
  - **Marp**: slide decks in markdown.
  - **Excalidraw** / **Canvas**: diagrams and visual maps of ideas.
- **Graph view:** the best way to see the shape of the wiki — hubs, clusters, orphans.
- **Configuration at first launch:** the agent writes these settings to `.obsidian/`, so the setup is reproducible:
  - `app.json`: `"useMarkdownLinks": false` (wikilinks), `"newLinkFormat": "shortest"`, `"attachmentFolderPath": "raw/assets"`, and `"userIgnoreFilters": ["templates/"]` (templates are excluded from search, graph, and link suggestions);
  - `templates.json`: `"folder": "templates"` (core Templates plugin);
  - `core-plugins.json`: enable the core plugins used by the wiki (templates, graph, backlinks, canvas, file explorer, search);
  - `.gitignore`: add `.obsidian/workspace*.json`.

  The agent then guides the user step by step for the rest (installing community plugins, the browser extension).
- **Images:** the agent downloads only useful images (diagrams, charts) when fetching web content. To view an article with images, it reads the text first, then looks at the images separately.

---

## 14. Git

- Git is **optional**, chosen by the user at first launch. If the user does not use git, the agent never runs any git command and never proposes commits or pushes; everything below applies only when git is used. The user can turn git on later by asking the agent.
- With git, the wiki is a git repository: history, branches, and collaboration for free.
- At the end of each operation (ingest, lint, capture, query with a kept answer, schema change…), the agent **proposes a commit and a push** together. The user validates.
- **No remote:** if `git remote -v` is empty, the agent proposes the commit only and says that pushing is not possible until a remote is added.
- **Commit messages are clear and never mention AI** (no "Co-Authored-By", no "Generated with…"). This rule is written in the schema and **takes precedence over any automatic attribution** the agent would add by default.
- Git is also how the agent detects the user's manual edits (section 4). Without git, the agent compares file modification dates with its last logged operation.

---

## 15. Customization

Every rule in this document is a default. The user can change them:

- **at any time**, by asking the agent. The agent proposes the change to `settings.md` (and to `CLAUDE.md` / `AGENTS.md` if a rule changes), and applies it only after validation.

User settings live in **`settings.md`** at the root of the wiki, referenced by the schema files.

---

## 16. Defaults

| Setting | Default |
|---|---|
| Wiki language | User's preferred language |
| System file and folder names | English |
| Schema files language | English (`CLAUDE.md`, `AGENTS.md`, `settings.md`) |
| `command.md` and templates language | User's language |
| Template file names | `template-<type>.md` |
| Domain names | The word given by the user, as is (spelling checked) |
| Number of wikis | One (several possible) |
| Domains | Chosen by the user; agent proposes, user validates |
| Subdomain depth | Unlimited (unique names, created only when justified) |
| Type subfolders | Created only when needed (`entities/personne/`, `entities/companies/` included) |
| Raw file naming | `YYYY-MM-DD-short-title.ext` |
| Raw capture fidelity | Errors corrected, meaning and wording unchanged |
| Ingest trigger | On demand (`ingest` / `processRaw`) |
| Ingest mode | Autonomous, questions grouped at the end |
| Captured idea | Agent asks: integrate now or at next ingest |
| New person page | Requires validation |
| New company page | Created freely |
| `user.md` updates | Free, always reported to the user |
| Citations | Wiki pages and raw sources |
| Keeping an answer | Agent proposes, user validates (synthesis page + conversation trace) |
| Answer format | Best suited to the question |
| Proactive section | 💡 section at the end, only when relevant |
| Web search | Permission before searching and before integrating |
| Lint trigger | On demand + suggested after 10 ingests or 30 days |
| Lint fixes | Mechanical: automatic · Content: user decides |
| Open questions | One `<name>-open-questions.md` per domain, subdomain, and project (created when needed, deleted when empty); `wiki/open-questions.md` holds general questions and links |
| Contradictions | ⚠️ flag in page + user decides |
| Idea evolution | Visible dated history in the page |
| Log format | `## [YYYY-MM-DD HH:MM] type \| Title` + summary + pages touched |
| Log rotation | Monthly (`wiki/log/YYYY-MM.md`) |
| Search | qmd on `wiki/` + `raw/processed/` (collections `<wiki>-wiki`, `<wiki>-raw`), fallback index + grep |
| Scripts | Proposed by the agent when needed |
| Reading tool | Obsidian |
| Link format | Wikilinks `[[...]]` |
| Git | Optional, chosen at first launch (remote link asked if used) |
| Commits / push | Proposed at the end of each operation, user validates (commit only if no remote) |
| AI mention in commits | Never |

---

## 17. Credits

Inspired by Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
