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
| `new contact` | Creates a contact page after validation, in the right domain's `contacts/`, and adds it to the list `<domain>-contacts.md` (section 5.5). |
| `new domain` / `new project` | Creates a domain, subdomain, or project after validation. |
| `close project` | Brings long-term value into the domains, then archives the project (section 9.5). |
| `settings` | Shows the current settings and lets the user change one (section 15). |
| `commands` | Shows the content of `command.md`. |
| `update wiki` / `/update_wiki` | Checks whether a newer version of this prompt is published, shows what changed, and updates the wiki's rules, templates, and structure after validation (section 9.6). |

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
2. **Create the structure:** `raw/` (with `processed/` and `assets/`), `templates/` (all `template-<type>.md` files), `wiki/` (`index.md`, `log.md`, `log/`, `open-questions.md`), `CLAUDE.md`, `AGENTS.md`, `settings.md` (including `prompt_version` and `prompt_source`, see section 9.6, and the type subfolder names in the wiki's language, see section 5.5), `command.md`. Save a copy of this document in `.llm-wiki/prompt-<version>.md`. If the agent is Claude Code, create the short skill `.claude/skills/update_wiki/SKILL.md` (section 9.6).
3. **Install search:** check whether qmd is already installed; install it only if needed. Create the wiki's collections with prefixed names and index them (section 12). If installation fails, explain why and fall back to the index plus grep.
4. **Configure Obsidian:** write the settings listed in section 13 to `.obsidian/` and give the user a step-by-step guide for the rest.
5. **Initialize git** (only if the user chose to use git): run `git init` only if the folder is not already a repository, and add the remote repository given by the user, if any (section 14).
6. **Log** the initialization and give the user a short summary of what was created, pointing to `command.md` to see what they can ask.

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
| Type subfolder names | Wiki's language (fixed at first launch in `settings.md`) |
| Domain names | The word given by the user, as is (spelling checked) |
| Number of wikis | One (several possible) |
| Domains | Chosen by the user; agent proposes, user validates |
| Subdomain depth | Unlimited (unique names, created only when justified) |
| Type subfolders | Created only when needed (`contacts/`, `companies/` included) |
| Raw file naming | `YYYY-MM-DD-short-title.ext` |
| Raw capture fidelity | Errors corrected, meaning and wording unchanged |
| Ingest trigger | On demand (`ingest` / `processRaw`) |
| Ingest mode | Autonomous, questions grouped at the end |
| Captured idea | Agent asks: integrate now or at next ingest |
| New contact page | Requires validation; needs a name and a way to reach them (family: a name is enough) |
| List pages | `<domain>-contacts.md` and `<domain>-companies.md` |
| New company page | Created freely |
| How-to pages | Created freely; only "Goal" required; `status` + `howto/<status>` tag |
| Manual writing | Small edits only, except `howto` pages in `writing` status |
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
| Prompt updates | On demand (`update wiki` / `/update_wiki`) + checked by the lint; latest tag of `prompt_source` |
| Update validation | Simple changes: all at once · Content changes: one by one · Conflicts: user chooses |
| Update safety | Git: commit first · No git: `../<wiki-name>_backup/`, deleted after 5 days with confirmation |

---

