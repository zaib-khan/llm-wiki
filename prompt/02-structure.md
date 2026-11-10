## 5. Architecture

### 5.1 Overview

```
my-wiki/
├── CLAUDE.md              ← schema (always identical to AGENTS.md)
├── AGENTS.md              ← schema (always identical to CLAUDE.md)
├── settings.md            ← user settings (see section 15)
├── command.md             ← commands the user can give the agent (see section 7)
├── .llm-wiki/             ← copy of the prompt version applied (see section 9.6)
├── .claude/skills/update_wiki/SKILL.md  ← short Claude Code skill for `/update_wiki`
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
    ├── <domain>/          ← one folder per domain (named with the user's word), with its projects in `projects/`
    ├── projects/          ← cross-domain projects without a main domain
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
- **Filing rules:** when a domain has subdomains (or projects) and it is unclear where a kind of content belongs, the agent proposes a short filing rule for that domain (e.g. "anything about the company as a whole → `work/company/`; anything about client X → `work/client-x/`; work outside the company → directly in `work/`"). Once validated, it is recorded in `settings.md` (one "Filing rule (<domain>)" row per domain) and applied at every ingest and capture without asking again. Changing it follows section 15 (logged `schema`).

### 5.5 Type subfolders

Inside a domain, pages are grouped in type subfolders, **created only when the first page of that type exists**:

```
wiki/family/
├── family.md
└── entities/
    ├── dad.md
    └── mom.md
```

Type subfolders are named **in the wiki's language** and are reserved (never used as domain names). Their names are chosen once, at first launch, from the language picked by the user, and recorded in `settings.md` so they never change. The agent always uses the names from `settings.md`. Example for a French wiki:

| Type subfolder | English | French |
|---|---|---|
| Sources | `sources/` | `sources/` |
| Entities | `entities/` | `entites/` |
| Knowledge | `knowledge/` | `connaissances/` |
| How-tos | `how-to/` | `comment-faire/` |
| Syntheses | `syntheses/` | `syntheses/` |
| Contacts | `contacts/` | `contacts/` |
| Companies | `companies/` | `entreprises/` |

Folder names use lowercase letters without accents or spaces. The list pages follow the same names: `<domain>-contacts.md`, `<domain>-entreprises.md` in a French wiki. In this document, the English names are used.

Contacts and companies have their own folders **at the domain level**, also created only when needed. Each one holds a list page that links all its pages. `entities/` keeps only the other entities:

```
wiki/football/
├── football.md
├── contacts/
│   ├── football-contacts.md    ← contact list of the domain (type contact-list)
│   └── coach-martin.md         ← one contact (type contact)
├── companies/
│   ├── football-companies.md   ← company list of the domain (type company-list)
│   └── acme.md                 ← one company (type company)
└── entities/
    └── stade-de-france.md      ← any other entity
```

`contacts/` and `companies/` are reserved names too, and so is `projects/` (a domain's projects, section 5.6).

**Contact rules:**

- **To exist in the wiki**, a contact needs **a first name or a last name, and at least one way to reach them** (phone, e-mail, address, or other). Otherwise, their name stays plain text wherever it is mentioned.
- **Exception — family:** when the user says a person is a member of their family and what the relationship is, a first name or a last name is enough. The relationship is recorded in the `relationship` field. The agent never guesses it.
- **Every new contact page requires the user's validation.** Company pages are created freely.

**List pages:**

- Each `contacts/` folder contains `<domain>-contacts.md` (type `contact-list`), and each `companies/` folder contains `<domain>-companies.md` (type `company-list`). They list and link every page of their folder and are created with the folder.
- Every contact or company page links back to its list, and the domain page links to both lists.
- **Organization tables:** a company page keeps a table of the people known there. Each name is linked to its contact page when one exists; otherwise it stays plain text.

### 5.6 Projects and archive

- Time-bound topics (reading a book, planning a trip, a research of a few weeks) are projects, with a project page `<project>.md`, following the same rules as domains.
- **A project attached to a domain or subdomain lives inside it:** `wiki/<domain>/projects/<project>/<project>.md` (e.g. `wiki/family/projects/japan-trip/japan-trip.md`). The domain page links its projects. Its raw sources mirror this path: `raw/processed/<domain>/projects/<project>/`.
- `projects/` inside a domain is a reserved name (like the type subfolders, never used as a domain or subdomain name), created only when the domain's first project exists.
- **Cross-domain projects without a main domain** live in `wiki/projects/<project>/`. When the main domain is unclear, the agent chooses it with the user.
- When a project is finished: the agent first **brings what has long-term value up into the relevant domains** (a lesson learned, a fact about a person, a reusable idea), then **moves the project to `wiki/archive/`**. Its raw sources follow the same move in `raw/processed/`.

### 5.7 Naming rules (summary)

| Item | Rule |
|---|---|
| System files and folders | English: `user.md`, `index.md`, `log.md`, `open-questions.md`, `<name>-open-questions.md`, `settings.md`, `command.md`, `.llm-wiki/`, `raw/`, `processed/`, `assets/`, `templates/`, `wiki/`, `projects/`, `archive/` |
| Type subfolders | Wiki's language, fixed once in `settings.md` (section 5.5) |
| Domains and subdomains | The word given by the user, as is (spelling checked) |
| Wiki page files | Lowercase, hyphenated, **unique across the wiki** |
| Raw files | `YYYY-MM-DD-short-title.ext` |
| Contacts and companies | `<domain>/contacts/` with `<domain>-contacts.md`, `<domain>/companies/` with `<domain>-companies.md` |
| Projects | `<domain>/projects/<project>/<project>.md`; `wiki/projects/<project>/` only for cross-domain projects |
| Templates | `templates/template-<type>.md` (e.g. `template-user.md`), so they never share a name with a wiki page |

---

## 6. Page Types and Templates

The `templates/` folder holds one template per page type, named `template-<type>.md`: `template-user.md`, `template-domain.md`, `template-project.md`, `template-contact.md`, `template-contact-list.md`, `template-company.md`, `template-company-list.md`, `template-entity.md`, `template-knowledge.md`, `template-howto.md`, `template-source.md`, `template-synthesis.md`. The prefix keeps file names unique across the vault (otherwise `templates/user.md` and `wiki/user.md` would make `[[user]]` ambiguous). The templates' section headings are written in the user's language. Every page the agent creates must follow its template. The user may edit the templates; the agent then follows the new version.

| Type | Purpose |
|---|---|
| `user` | The user: identity, situation, goals, values, preferences, health, psychology, relationships — the center of the wiki |
| `domain` | Overview of a domain or subdomain, with the list of its pages |
| `project` | A time-bound project: goal, status, dates, related pages |
| `contact` | A person: identity, relationship to the user, contact details, work, personality, history |
| `contact-list` | The list page of a `contacts/` folder, linking all its contact pages |
| `company` | A company: identity, activity, location, relationship to the user, organization, people known there |
| `company-list` | The list page of a `companies/` folder, linking all its company pages |
| `entity` | Any other entity: place, object, tool, organization that is not a company |
| `knowledge` | What the user knows or has learned: an idea, topic, method, explanation — including the user's own ideas |
| `howto` | How to do something, step by step (a procedure, a runbook, a checklist). `knowledge` is for understanding, `howto` is for doing |
| `source` | Summary of one raw source |
| `synthesis` | Comparison, analysis, overview, or a kept answer to a question |

**Every template starts with a YAML frontmatter**, at least:

```yaml
---
type: entity            # user | domain | project | contact | contact-list | company | company-list | entity | knowledge | howto | source | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []             # links to raw files in raw/processed/
tags: []
---
```

**Extra frontmatter fields** (names stay in English so queries work in any language):

- **contact**: `relationship`, `birthday`, `company` (link to the company page), `role`, `address`
- **howto**: `status` (`writing` · `draft` · `tested` · `outdated`), `last_used`. The matching tag `howto/<status>` is always added and kept in sync with `status`; `status` is the reference.
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
- **domain**: Overview · Pages (by type) · Contacts (link to `<domain>-contacts.md`) · Companies (link to `<domain>-companies.md`) · Subdomains · Projects (links to the domain's projects) · Key facts · Open points
- **project**: Goal · Status · Timeline · Key information · Related pages · Outcome (when finished)
- **contact**: Identity · Relationship to the user · Contact details · Work · Personality · Interests · Important dates · Close circle · Facts & information · Interaction history · Ideas & gifts · Links
- **contact-list**: Overview · Contacts (table: name linked to the contact page, relationship, role, organization) · Links
- **company-list**: Overview · Companies (table: name linked to the company page, industry, relationship to the user) · Links
- **company**: Identity · Activity · Size & figures · Location · Relationship to the user · Organization · People known there (table, names linked to contact pages when they exist) · Culture & values · Tools & methods · Competitors & partners · News & history · Facts & information · Links
- **entity**: Who / what · Relationship to the user · Facts · History · Links
- **knowledge**: Summary · Details · The user's view · Evolution · Related knowledge · Sources
- **howto**: Goal · When to use it · Prerequisites · Steps · Verification · Known issues · History · Links
- **source**: Metadata (author, date, URL, format) · Summary · Key points · Pages updated · Quotes worth keeping
- **synthesis**: Question or purpose · Answer / analysis · Sources · Related pages

**Required and optional sections:**

- For most types, a page has **all the sections of its template**, even when some are still empty.
- For **`contact` and `company` pages, every section is optional**: the page keeps the order and the names of its template's sections, but only shows the sections that have content. A new section is added when there is something to put in it. (What a contact needs to exist is defined in section 5.5.)
- For **`howto` pages, only "Goal" is required**; the other sections are optional.

**How-to status:**

| `status` | Meaning |
|---|---|
| `writing` | Still being written; steps may be missing |
| `draft` | Finished, not yet tested end to end |
| `tested` | Followed successfully; reliable |
| `outdated` | No longer works; needs review |

- A `writing` how-to may be used to answer a question, but the agent says so: "⚠️ this how-to is still being written". The agent never completes it on its own.
- When the user says a how-to is finished, the agent sets its status to `draft` (or `tested` if the user has already followed it).

---

