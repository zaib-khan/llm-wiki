## 13. Obsidian

The wiki is designed to be read in **Obsidian**.

- **Links:** wikilinks `[[page-name]]` by default (this is why file names must be unique).
- **Never link to a folder or to a file that is not a note** (no markdown link, no wikilink). In Obsidian, clicking a link that leads to no note creates an empty note with that name. Folder paths and system file paths are written as code (`raw/`, `templates/`), never as links. This applies everywhere, including `CLAUDE.md` and `AGENTS.md`.
- **Recommended plugins and tools:**
  - **Obsidian Web Clipper** (browser extension): converts web articles to markdown; configure it to save into `raw/`.
  - **Bases** (core plugin, no install): the recommended way to build dynamic tables and card views from the templates' frontmatter (e.g. all family members, all ongoing projects); used by the dashboard below.
  - **Dataview** (optional community plugin): an alternative for dynamic tables and lists written as queries inside notes.
  - **Templater** / core **Templates**: use the templates in `templates/` when editing by hand.
  - **Marp**: slide decks in markdown.
  - **Excalidraw** / **Canvas**: diagrams and visual maps of ideas.
- **Obsidian skills:** [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills), by the creator of Obsidian, in the Agent Skills format (Claude Code, Codex, and other agents supporting skills). At first launch the agent proposes to install them; it installs only after the user's validation and only if it supports skills: `npx skills add https://github.com/kepano/obsidian-skills` (other methods are described in the repository). Useful skills: `obsidian-markdown` (wikilinks, embeds, callouts, properties), `obsidian-bases` (valid `.base` files: views, filters, formulas, used for `wiki/dashboard.base`), `json-canvas` (`.canvas` files), `defuddle` (web extraction, used in ingest). Once installed, the agent uses them when writing pages, bases, or canvases. If installation fails or is declined, nothing changes: the rules of this document still apply.
- **Dashboard:** `wiki/dashboard.base`, an Obsidian Bases file (YAML), created at first launch. The file name stays in English; view names and column display names are written in the wiki's language. Its base filter keeps markdown pages with a `type`, except `source` pages. Five generic views:
  - **Recently updated**: the 30 most recently updated pages;
  - **How-tos by status**: how-tos grouped by `status`;
  - **Dormant pages**: not updated for more than 60 days, excluding contact and company pages;
  - **Orphans**: pages without backlinks, excluding `user`;
  - **Contacts**: contact pages as cards.

  When a domain gets its own fields (section 6), the agent may propose a dedicated view for it (e.g. bills filtered on that domain's folder, sorted by due date, with a sum of the amounts); nothing is added without validation. Generic content (display names to translate):

  ```yaml
  filters:
    and:
      - file.ext == "md"
      - type
      - type != "source"
  formulas:
    days_since_update: if(updated, (today() - date(updated)).days, "")
    domain: file.folder.split("/").slice(1, 2).join("")
    source_count: if(sources, list(sources).length, 0)
  properties:
    file.name:
      displayName: Page
    formula.domain:
      displayName: Domain
    formula.days_since_update:
      displayName: Days since update
    formula.source_count:
      displayName: Sources
    last_used:
      displayName: Last used
  views:
    - type: table
      name: Recently updated
      order:
        - file.name
        - type
        - formula.domain
        - updated
        - formula.source_count
      sort:
        - property: updated
          direction: DESC
      limit: 30
    - type: table
      name: How-tos by status
      filters:
        and:
          - type == "howto"
      groupBy:
        property: status
        direction: ASC
      order:
        - file.name
        - formula.domain
        - status
        - last_used
        - updated
    - type: table
      name: Dormant pages
      filters:
        and:
          - formula.days_since_update > 60
          - type != "contact"
          - type != "company"
      order:
        - file.name
        - type
        - formula.domain
        - updated
        - formula.days_since_update
      sort:
        - property: formula.days_since_update
          direction: DESC
    - type: table
      name: Orphans
      filters:
        and:
          - file.backlinks.isEmpty()
          - type != "user"
      order:
        - file.name
        - type
        - formula.domain
        - updated
    - type: cards
      name: Contacts
      filters:
        and:
          - type == "contact"
      order:
        - file.name
        - relationship
        - role
        - company
        - formula.domain
  ```
- **Graph view:** the best way to see the shape of the wiki — hubs, clusters, orphans.
- **Configuration at first launch:** the agent writes these settings to `.obsidian/`, so the setup is reproducible:
  - `app.json`: `"useMarkdownLinks": false` (wikilinks), `"newLinkFormat": "shortest"`, `"attachmentFolderPath": "raw/assets"`, and `"userIgnoreFilters": ["templates/"]` (templates are excluded from search, graph, and link suggestions);
  - `templates.json`: `"folder": "templates"` (core Templates plugin);
  - `core-plugins.json`: enable the core plugins used by the wiki (templates, graph, backlinks, canvas, file explorer, search, bases);
  - `.gitignore`: add `.obsidian/workspace*.json`.

  The agent then guides the user step by step for the rest (installing community plugins, the browser extension).
- **Images:** the agent downloads only useful images (diagrams, charts) when fetching web content. To view an article with images, it reads the text first, then looks at the images separately.

---

## 14. Git

- Git is **optional**, chosen by the user at first launch. If the user does not use git, the agent never runs any git command and never proposes or makes commits or pushes; everything below applies only when git is used. The user can turn git on later by asking the agent.
- With git, the wiki is a git repository: history, branches, and collaboration for free.
- **Commit mode** (`settings.md`, asked at first launch, section 8): at the end of each operation (ingest, lint, capture, query with a kept answer, schema change…), the agent commits according to this setting:
  - `propose` (default): the agent proposes the commit; the user validates.
  - `automatic`: the agent commits without asking and reports the commit hash.
- **Push frequency** (`settings.md`, a number N, default 5; 1 = push after every commit): the agent pushes once N commits are not yet pushed. In `propose` mode the push is proposed; in `automatic` mode it is done and reported.
- **End of a work session:** when the session ends (or the user says they are done), the agent also pushes the pending commits even if N is not reached (proposed or done according to the commit mode), so nothing stays only on the local machine.
- **No remote:** if `git remote -v` is empty, the agent commits only (according to the commit mode) and says that pushing is not possible until a remote is added.
- **Commit messages are clear and never mention AI** (no "Co-Authored-By", no "Generated with…"). This rule is written in the schema and **takes precedence over any automatic attribution** the agent would add by default.
- Git is also how the agent detects the user's manual edits (section 4). Without git, the agent compares file modification dates with its last logged operation.

---

