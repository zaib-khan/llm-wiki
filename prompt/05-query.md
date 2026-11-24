### 9.3 Query — answering questions

1. The agent searches first with the search engine (`qmd search`, or `qmd vsearch` when needed, section 12) across `wiki/` and `raw/processed/`, then reads the domain page of the topic for context. Without it, it walks the tree `index.md` → domain page → subdomain page → page, and uses grep only as a last resort. Then it reads the relevant pages.
2. It answers in **the format best suited to the question** (text, markdown page, table, Mermaid diagram, chart, Marp slides, Obsidian canvas…).
3. **Citations:** it cites both the wiki pages (`[[page]]`) and, when useful, the original raw sources.
4. **Proactive section:** when — and only when — something relevant exists, the answer ends with a dedicated section where each item starts with 💡: forgotten ideas related to the question, details from the user's life that shed light on it, links the user may have missed.
5. **Keeping valuable answers:** when an answer has lasting value (analysis, comparison, discovered connection), the agent proposes to keep it. If the user agrees, it creates a `synthesis` page in the relevant domain **and** saves a trace of the conversation in `raw/processed/<domain>/`.
6. **When the wiki is not enough:**
   1. the agent says so and **asks permission** to search the web;
   2. it proposes an answer;
   3. if the answer suits the user, it fetches the raw content of the sites or documents used and saves it to `raw/` (web pages with Defuddle first, as in ingest);
   4. it **asks permission** to integrate these sources, then integrates them with all relevant links.
7. A plain question changes no file and creates no commit. A kept answer (step 5) is committed (`query:`, section 14).

## 12. Search

- **qmd** (https://github.com/tobi/qmd) is installed at first launch: a local search engine for markdown with keyword (BM25) and semantic (vector) search plus LLM re-ranking, available as a CLI and as an MCP server — so it works with any agent.
- **Scope:** `wiki/` **and** `raw/processed/`, so a precise detail can be found even if it was not carried into the wiki.
- **Collection names:** qmd collections are global to the machine, so generic names like `wiki` or `raw` would clash with another wiki. Prefix them with the wiki's folder name: `<wiki>-wiki` (on `wiki/`) and `<wiki>-raw` (on `raw/processed/`).
- **Re-indexing:** after every ingest and after any change to the wiki or the sources, run `qmd update && qmd embed`. Run `qmd cleanup` if qmd reports orphaned chunks.
- **Search order:** `qmd search` first (keywords), or `qmd vsearch` (semantic) when the exact words are not enough; never `qmd query` (re-ranking), too slow for everyday use (over 2 minutes in a test, where `qmd search` was twice as fast as the tree and used a third fewer tokens, for about 10% less information found). Then the agent reads the domain page of the topic for context. If qmd is not installed or fails, the agent walks the tree `index.md` → domain page → subdomain page → page (section 11.1); grep comes last.
- **Other scripts:** when a mechanical task becomes repetitive (checking that `CLAUDE.md` = `AGENTS.md`, unique names, broken links…), the agent may **propose** to write a small script in `scripts/`. Nothing is created without validation.

---

