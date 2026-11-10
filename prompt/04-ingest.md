## 9. Operations

### 9.1 Capture — ideas told to the agent

When the user tells the agent an idea, a thought, or any information in conversation (without dropping a file):

1. The agent **saves a raw source first**: a dated file in `raw/` (`YYYY-MM-DD-short-title.md`) containing what the user said, **faithfully**. Transcription and typing errors are corrected; the meaning and the wording are not changed.
2. The agent **asks**: "Shall I integrate it now, or keep it for the next ingest?"
3. The capture is logged (`capture`).

Capturing an idea must cost the user almost nothing: no forms, no required structure.

### 9.2 Ingest — processing the inbox

**Trigger:** only on demand, when the user says `ingest` or `processRaw`.

**Rhythm:** the agent processes all sources in `raw/` **autonomously**. It only needs the user for things that require their judgment (contradictions, new domains or subdomains, new contact pages, classification doubts). It **does not stop**: it sets these points aside and asks **all its questions at the end**, according to the question style (section 15).

**Safe progress:** before writing, list the files waiting directly in `raw/` and check whether any already has a source page or a copy in `raw/processed/` (including after an interrupted ingest). Process one source at a time. A source is complete only when its raw file, source page, related pages, links, domain page, and index agree. Only then move the raw file and record that completed source in the log. If processing stops midway, the next ingest reconciles those existing files and finishes the source instead of creating a second source page or duplicating facts. Report any incomplete source that cannot be reconciled; never silently discard it.

When a decision is needed before a source can be filed or a page can be created, leave that source pending in `raw/` and ask at the end. Continue with independent sources. A text extraction beside a PDF, image, audio, or video is part of the same source, not a second item to ingest.

**Sub-agents (optional):** for a large ingest, if the agent can launch sub-agents, it may hand each independent source to its own sub-agent, working in parallel.
- Each sub-agent handles one source and writes only that source's own pages (source page and its entity, knowledge, how-to pages). It reports back the pages it created or changed, what the shared files need, and its pending questions.
- Only the main agent writes the shared files (`index.md`, the log, domain pages, list pages, `user.md`, open questions) and makes the commit, so two agents never write the same file.
- Sub-agents never create domains, subdomains, or contact pages; questions needing the user's judgment go back to the main agent, who asks them all at the end.
- Two sub-agents never update the same existing page: sources touching the same page are handled one after the other by the main agent.
- Each source is still completed as a unit (safe progress above): once its sub-agent reports, the main agent finalizes the shared files, then moves the raw file and logs that source.

**For each source, the agent:**

1. Reads it (for a non-text source, creates the text version first).
2. If the user gave a URL: fetches the content (article text, video transcript) and saves it as a raw source. For web pages, uses [Defuddle](https://github.com/kepano/defuddle) first: `npx -y defuddle parse <url> --md` gives the clean article in markdown (no menus, ads, or clutter); `--json` also gives the title, author, and publication date for the source page's metadata. If Defuddle fails (or Node/npx is unavailable), falls back to a plain fetch. Useful images (diagrams, charts) are downloaded to `raw/assets/`. If the content cannot be fetched, keeps the link with a note "content not retrieved".
3. Renames it to `YYYY-MM-DD-short-title.ext`.
4. Determines its main domain (and related domains), applying the domain's filing rule from `settings.md` when there is one (section 5.4); if filing is ambiguous and no rule exists, proposes one in the end-of-ingest questions.
5. Writes a `source` page.
6. Creates or updates the related entity, knowledge, how-to, and synthesis pages. A single source may touch 10–15 pages.
   - The agent **creates pages freely** inside existing domains.
   - **Exceptions requiring validation:** a new **contact** page (only if the contact rules of section 5.5 are met), a new domain, a new subdomain. Company pages are created freely.
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
- pending questions (asked now, according to the question style, section 15).

Then it proposes a commit (section 14).

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

