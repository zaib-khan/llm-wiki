# LLM Wiki — A Second Brain Built and Kept by Your Agent

A prompt that turns your LLM agent (Claude Code, Codex, OpenCode, Cursor…) into the librarian of your personal second brain.

**Current version: 0.13.0** — still in testing; `1.0.0` will mark the first stable release. See [`CHANGELOG.md`](CHANGELOG.md).

## Why I built this

Too much information reaches me every day: articles, videos, documents, conversations — and my own thoughts. Over time I noticed the cost. I forget details. I forget where something came from. My ideas get confused, and I lose focus. Sometimes I have a really good idea, then I read a website or watch a video, and the idea is gone.

So I wanted a place where I could **get everything out of my head** — what I read and watch, but also my ideas, my thoughts, what I know about the people around me — and trust that it will be kept, organized, and found again. Once it is out of my head, my mind is free to focus on the result. And I keep a trace of how my thinking evolves.

## Where it comes from

This project started from Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). His core idea is brilliant: instead of an LLM rediscovering your documents from scratch at every question (RAG), the LLM **builds and maintains a persistent wiki** that gets richer with every source. Humans abandon wikis because the bookkeeping grows faster than the value; an LLM never gets bored of it.

What I loved: you drop anything into a `raw/` folder, the agent processes it, links it, files it, and you can ask questions to get context quickly.

But his document is intentionally abstract — a base for everyone to build on. In practice, two things were missing for me:

- **The agent organized things its own way.** After dropping a lot of content, I had trouble finding my way. I need a structure that is defined in advance and predictable.
- **It was about documents, not about a life.** I wanted more.

The original prompt is kept unchanged in [`karpathy-llm-wiki-original.md`](karpathy-llm-wiki-original.md). My version is [`zaib-khan-llm-wiki.md`](zaib-khan-llm-wiki.md).

## My vision

### The wiki is a library

The wiki is **a library that grows over time**. You are the **owner**: you decide what enters it. The agent is the **librarian**: it classifies everything according to clear rules and finds the right book for the task at hand. And a good librarian also knows the owner — it brings back an old forgotten notebook when it becomes relevant, notices connections between two books, and asks questions to fill the empty shelves.

### Your thoughts are sources too

Articles, PDFs, YouTube videos — yes. But also **what is in your head**. An idea told to the agent in a few words is saved as a source, exactly like an article. Capturing a thought must cost almost nothing.

And when an idea evolves — idea A in January becomes idea B in June — that is not noise, it is information. Sources are immutable, the new version is added, and the agent links both and keeps a dated history.

### A model of your life, with you at the center

The wiki is not only knowledge. It represents **you and your world**: a `user.md` at the center, then domains you choose — family, work, your company, a hobby, anything. Each domain is a folder. The people around you (contacts) and the companies in your life get their own pages, with a list per domain linking them all.

Everything lives in **one wiki**, on purpose: a detail from your private life can be the key to a professional question, and the other way around. With the full context, the agent can see what you miss.

### A proactive agent

The agent does not only file and answer. It reminds you of forgotten ideas that are relevant to your question (marked with 💡), spots links and patterns across domains, helps you clarify confused ideas, and asks you questions to complete the wiki.

### Structure, simplicity, and you in control

- A defined structure: `raw/` as an inbox, `raw/processed/` mirroring the wiki, domains as folders (named with your own words), templates for every page type (`template-<type>.md`), unique file names.
- Simplicity first: nothing is created before it is needed.
- Open questions are never lost: when you skip one, it waits in its domain's own question file until you answer it.
- The agent proposes, you validate: new domains, person pages, schema changes, web searches, commits.
- You always know what you can ask: a `command.md` file at the root of your wiki lists every command and explains what it does.

## How to use it

1. Create a new, empty folder for your wiki (your wiki lives in its own repository — this one only contains the prompt).
2. Open your LLM agent in that folder and give it [`zaib-khan-llm-wiki.md`](zaib-khan-llm-wiki.md).
3. Answer a few short questions: your language, your name, your first domain, and whether you want to use git (and your remote repository link). Everything else comes with time.
4. Open `command.md` to see what you can ask. Drop sources into `raw/` and say `ingest`. Tell the agent your ideas. Ask it questions. Run `lint` from time to time.

Open the wiki in [Obsidian](https://obsidian.md) to browse it, follow links, and watch the graph grow. The agent configures Obsidian for you at first launch and installs [qmd](https://github.com/tobi/qmd) for local search. If you choose to use git, the agent proposes a commit (and a push, if you have a remote) after each operation.

Every rule in the prompt is a default: change anything by asking your agent.

## Keeping your wiki up to date

The prompt evolves. Each version is published as a git tag, and [`CHANGELOG.md`](CHANGELOG.md) describes what changed. Your wiki remembers which version it applies.

Say `update wiki` (or `/update_wiki` in Claude Code): the agent checks the latest published version, shows you what changed, keeps your own customizations unless you choose otherwise, and secures your wiki first (a git commit, or a backup next to it). If something goes wrong, ask it to restore the previous state, and feel free to [open an issue](https://github.com/zaib-khan/llm-wiki/issues) — describe the problem, but never paste personal content from your wiki.

## Maintaining the prompt

The editable sources live in [`prompt/`](prompt/). The distributed file
[`zaib-khan-llm-wiki.md`](zaib-khan-llm-wiki.md) is generated and committed to the
repository, so users can still give a single file to their agent.

| Source | Contents |
|---|---|
| [`01-principles.md`](prompt/01-principles.md) | Introduction, version, vision, roles, shared principles, credits |
| [`02-structure.md`](prompt/02-structure.md) | Folders, naming, page types and templates |
| [`03-setup.md`](prompt/03-setup.md) | Schema files, first launch, customization and defaults |
| [`04-ingest.md`](prompt/04-ingest.md) | Capture, ingestion, contradictions and idea evolution |
| [`05-query.md`](prompt/05-query.md) | Answers, citations and search |
| [`06-maintenance.md`](prompt/06-maintenance.md) | Lint, project lifecycle, updates, index, log and open questions |
| [`07-integrations.md`](prompt/07-integrations.md) | Obsidian and Git |

Edit these source files rather than the generated prompt, then run:

```sh
python3 scripts/build_prompt.py
python3 scripts/build_prompt.py --check
```

The script requires Python 3 and no additional packages. It restores the original
section order and preserves the text exactly, including section numbers and
cross-references. Source files group related sections even when they appear at
different places in the complete prompt. The section ownership and output order
are defined in [`scripts/build_prompt.py`](scripts/build_prompt.py); update those
lists if you add, remove or move a numbered section between source files.

`--check` does not modify files and exits with an error if the complete prompt is
missing or out of date. The builder also rejects missing, duplicate or unexpected
sections. Its checks can be tested with `python3 -m unittest discover -s tests`.

Include source changes, the regenerated prompt and the corresponding
`CHANGELOG.md` entry together. Change the version in `prompt/01-principles.md`
only when preparing an explicitly requested release, then regenerate the prompt.
Existing wikis still use the complete prompt from a published tag; splitting the
repository sources requires no wiki migration.

## Credits

Inspired by Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
