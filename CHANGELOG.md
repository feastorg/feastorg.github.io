# Changelog

All notable changes to the feastorg.github.io site.

Format is date-based (not semver). Most recent first.

---

## 2026-06-11

### Added
- **Slice Registry** (`/slices/`): auto-generated page listing all 40 `Slice_*` repos, grouped by category with status badges. Powered by `scripts/generate_slice_index.py` which fetches each repo's `slice.yaml` manifest via the GitHub API. Data written to `_data/slice-index.json` at build time.
- **Slice status badge styles**: `.slice-badge` CSS in `_sass/custom/custom.scss` with per-status color variants (released, validated, prototype, concept, deprecated).
- `scripts/generate_slice_index.py`: Python script to generate `_data/slice-index.json`.
- CI step in `.github/workflows/pages.yml` to run `generate_slice_index.py` before build.

### Changed
- **BREAD spec source**: `_data/sources.json` updated to import spec docs from `feastorg/bread-infra` (at `spec/`) instead of the now-archived `feastorg/BREADS` repo.
- **Linked projects nav restructure**: removed all `Slice_*` entries from `_data/linked_projects.json` (slices are now surfaced via the registry). Remaining 4 non-Slice linked projects (CAN Nano Shield, CAN Nano Fieldbus, KiCad Simulation Examples, KNEEAD) are now direct children of **Projects** in the nav, with `🔗` appended to their titles. Removed the "Linked Projects 🔗" grouping page (`projects/linked.md`).
- **Slice registry URLs**: `generate_slice_index.py` now constructs each slice's URL as `https://feastorg.github.io/{repo}/` (GitHub Pages site) rather than the GitHub repo URL from `slice.yaml`.
- `scripts/generate_linked_redirects.py`: stubs now use `parent: "Projects"` (no `grand_parent`).

### Removed
- `projects/linked.md`: the "Linked Projects 🔗" grouping/hub page.

---

## 2026-05-19

### Added
- BREAD project history page migrated from the archived BREADS repo.

---

## 2026-05-01

### Added
- Pico templates added to linked projects (`Slice_TEMP_PICO_S2L-r1`, `Slice_TEMP_PICO_L4L-r1`).

---

## 2026-04-21

### Added
- GitHub icon button in site header (replaces plain text aux link).
- Light/dark theme toggle as a pill button with persistent user preference (localStorage).

### Changed
- `import_sources.sh`: hardened manifest path validation to prevent unsafe mount targets and destructive syncs.
- `generate_linked_redirects.py`: reconcile stale redirect stubs on each run; hardened config validation.
- SCSS: replaced undefined `\/\` escapes with literals for sass-embedded 1.97.3 compatibility.

### Fixed
- Header: removed site-button inheritance from GitHub aux icon to correct boxed layout.

---

## 2026-04-20

### Changed
- Org casing renamed from `FEASTorg` to `feastorg` across site config and nav.

### Removed
- anolis* and fluxgraph sources/pages removed from site (repos migrated/archived).

---

## 2026-03-28

### Added
- KiCad Simulation Examples linked as an external project with redirect stub.

---

## 2026-01-26

### Changed
- Site rehauled: removed implementation domains and system-level sections.
- Upgraded `just-the-docs` from 0.11.1 to 0.12.0.
