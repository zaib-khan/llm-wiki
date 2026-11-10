# Règles du projet

## Git
- Ne jamais mentionner dans les messages de commit ou les descriptions de PR que le travail a été fait par Claude ou par une autre IA (pas de `Co-Authored-By`, pas de "Generated with…").

## Structure du projet
- `karpathy-llm-wiki-original.md` : prompt original de Karpathy, ne jamais le modifier.
- `prompt/` : les sept fichiers sources du prompt, organisés par sujet (voir le README). Modifier ces fichiers.
- `scripts/build_prompt.py` : assemble les sources dans l'ordre des sections d'origine ; `--check` vérifie le résultat sans écrire.
- `zaib-khan-llm-wiki.md` : prompt complet généré et distribué. Ne pas le modifier directement ; lancer `python3 scripts/build_prompt.py`, puis `python3 scripts/build_prompt.py --check`.
- `analyse-karpathy/` (ignoré par git) : le prompt de Karpathy découpé en fichiers par section, avec analyse, questions et mes décisions. On les traite un par un pour construire mon prompt.

## Méthode d'analyse des fichiers `analyse-karpathy/`
- Pour chaque fichier analysé, poser autant de questions que nécessaire (sans limite) pour bien comprendre ce que je souhaite avant de remplir « Tes décisions ».
- Poser les questions **une par une** (attendre ma réponse avant la suivante).
- Une fois toutes les questions posées : faire une synthèse/analyse de toutes mes réponses, puis attendre que je valide (OK ou non) avant de remplir « Tes décisions » et de passer au fichier suivant.
- Après validation, créer `analyse-karpathy/XX-nom-response.md` contenant toutes les questions posées et mes réponses (fidèlement).

## Versions et publication du prompt
- La ligne `Version: X.Y.Z` est définie dans `prompt/01-principles.md` et reproduite en haut du prompt généré (format `MAJEUR.MINEUR.CORRECTIF`). Lors d'une publication, modifier cette source puis régénérer le prompt avant de commiter.
- À chaque modification de `zaib-khan-llm-wiki.md`, ajouter l'entrée correspondante dans la section `[Unreleased]` de `CHANGELOG.md` (avec les instructions de migration si le changement touche un wiki existant).
- Le numéro de version et le tag ne changent que quand je dis « publie une version » : proposer le niveau (correctif, mineur, majeur), puis après validation : mettre à jour la ligne `Version`, renommer `[Unreleased]` en `[X.Y.Z] - AAAA-MM-JJ`, commiter, créer le tag `vX.Y.Z` et pousser (commit + tag).
- Seuls les tags comptent pour la commande `update wiki` des utilisateurs.
- Après le push du tag, créer une release GitHub avec `gh release create vX.Y.Z --title "LLM Wiki X.Y.Z" --notes "..."` : notes courtes en anglais (points forts, comment mettre à jour un wiki existant, lien vers `CHANGELOG.md`), rédigées à partir de l'entrée du CHANGELOG et validées par moi avant création.
- Si `gh` n'est pas installé ou pas connecté, fournir les notes à coller sur `github.com/zaib-khan/llm-wiki/releases/new`.

## Retours de test (prompts d'amélioration)
- Pour chaque prompt d'amélioration que je colle : d'abord expliquer simplement de quoi il parle, puis poser des questions (une par une) sur la façon d'apporter les changements, avant de modifier le prompt.
- Vérifier qu'il ne contredit pas une règle existante ; signaler tout conflit.
- Après modification : ajouter l'entrée dans `[Unreleased]` du CHANGELOG.
- Après chaque changement validé de cette série : commiter et pousser immédiatement (sans redemander).
- Préférer des petits changements ciblés (un sujet par modification et par commit) plutôt que de gros changements.
