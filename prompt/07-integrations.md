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

