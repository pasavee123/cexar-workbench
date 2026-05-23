# CeXaR Repo Hunt

This folder collects external repositories, papers, model cards, datasets, and tools before they are trusted.

External sources are candidates only. Popularity does not imply safety, compatibility, or clinical validity.

## Folder Layout

- `candidates/` contains raw candidate notes.
- `reviews/` contains Codex-reviewed assessments.

## Candidate Flow

1. Add a candidate file using `candidates/TEMPLATE.md`.
2. Codex reviews compatibility, license, dependencies, assumptions, and risks.
3. If promising, create an isolated experiment in `experiments/`.
4. Runner executes only the approved experiment plan.
5. Codex reviews results before any integration proposal.

