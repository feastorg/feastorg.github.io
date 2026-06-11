# Changelog

All notable changes to the `feastorg.github.io` documentation site.

This changelog is date-based rather than semantic-version based. It was
reconstructed from the git history so it reads as though the changelog had been
maintained continuously from the first site commit.

The format follows the spirit of Keep a Changelog, with entries grouped under
`Added`, `Changed`, `Fixed`, `Removed`, and `Security` where applicable.

---

## 2026-06-11

### Added

- Added the Slice Registry at `/slices/`, backed by `_data/slice-index.json`.
- Added `scripts/generate_slice_index.py` to discover `Slice_*` repositories,
  fetch each repository's `slice.yaml`, and generate the slice registry data.
- Added category-specific Slice Registry pages for actuation, sensing,
  integrated, power, interface, template, and prototype slices.
- Added slice status badges and registry table styling in
  `_sass/custom/custom.scss`.
- Added `CHANGELOG.md` back to the repository and seeded it with recent history.

### Changed

- Switched the BREAD specification import source from the archived
  `feastorg/BREADS` repository to `feastorg/bread-infra`, mounted from `spec`
  into `projects/bread-infra`.
- Moved slices out of `_data/linked_projects.json`; slices are now surfaced
  through the Slice Registry instead of the linked-project list.
- Changed linked project redirect stubs so non-slice linked projects appear as
  direct children of `Projects`.
- Changed slice registry URLs to point at each slice's GitHub Pages site rather
  than the GitHub repository URL.
- Moved linked project marker text before the linked project title and shortened
  "KiCad Simulation Examples" to "KiCad Sim Examples" for sidebar fit.
- Pushed linked project stubs to the bottom of the Projects navigation with
  high `nav_order` values.

### Fixed

- Fixed imported section `index.md` handling so `ensure_front_matter.py` no
  longer overwrites section parent front matter created by
  `ensure_section_index`.

### Removed

- Removed the old `projects/linked.md` linked-project grouping page.
- Removed the temporary `PLAN-nav-restructure.md` planning document after the
  navigation restructure was implemented.

---

## 2026-05-19

### Added

- Added the BREAD project history page, migrated from the archived BREADS
  repository.

---

## 2026-05-01

### Added

- Added Pico template repositories to the linked project data:
  `Slice_TEMP_PICO_S2L-r1` and `Slice_TEMP_PICO_L4L-r1`.

---

## 2026-04-21

### Added

- Added `.gitattributes` to enforce consistent line endings.
- Added a browser-default light/dark theme switcher with persistent local
  preference.
- Added the current compact pill-style theme toggle.
- Added a GitHub icon button in the header, replacing the previous text aux
  link.
- Added a header divider between the theme control and GitHub aux control.
- Added retry and backoff behavior for sparse clone imports.
- Added canonical linked project redirect stubs under `projects/linked` with
  legacy stubs under `docs/projects/linked`.

### Changed

- Brought CI closer to Pages behavior by making CI run import and linked stub
  generation before the Jekyll build.
- Updated CI and Pages workflows to install `jq` and `rsync` explicitly.
- Made the footer year dynamic.
- Updated site architecture documentation to match the current import and
  linked-project model.
- Reworked the theme switcher design through segmented-control and pill-toggle
  iterations.
- Replaced undefined Sass `\/\` escapes with literal values for
  sass-embedded compatibility.
- Reconciled linked redirect generation so stale generated files are removed on
  each run.

### Fixed

- Fixed archive navigation visibility.
- Fixed inherited button styling that caused the GitHub icon control to render
  with an incorrect boxed layout.

### Removed

- Removed unused `_data/navigation.yml`; navigation now relies on Just the Docs
  front matter and data-driven linked project stubs.

### Security

- Hardened `scripts/import_sources.sh` manifest path validation to reject unsafe
  mount targets and destructive sync destinations.
- Hardened `scripts/generate_linked_redirects.py` configuration validation.

---

## 2026-04-20

### Changed

- Renamed visible organization casing from `FEASTorg` to `feastorg`.
- Merged Dependabot updates for the `json` gem and
  `actions/upload-pages-artifact`.

### Removed

- Removed Anolis, anolis-provider, anolis-protocol, and FluxGraph source
  integrations after those docs were migrated or archived.

---

## 2026-04-14

### Changed

- Updated `actions/upload-pages-artifact` from v4 to v5 through Dependabot.

---

## 2026-04-07

### Changed

- Updated the `json` gem from 2.18.0 to 2.19.2 through Dependabot.

---

## 2026-04-06

### Changed

- Merged the Dependabot update for `actions/configure-pages` v6.

---

## 2026-03-30

### Changed

- Updated `actions/configure-pages` from v5 to v6 through Dependabot.

---

## 2026-03-28

### Added

- Added KiCad Simulation Examples as a linked external project.
- Added guidance for navigating to the KiCad Simulation Examples site and its
  downloadable PDF package.
- Added a Developer Resources redirect stub so KiCad Simulation Examples appears
  under Developer Resources in the navigation.

### Changed

- Merged the Dependabot update for `actions/deploy-pages` v5.

---

## 2026-03-26

### Changed

- Updated `actions/deploy-pages` from v4 to v5 through Dependabot.

---

## 2026-03-06

### Added

- Added temporary documentation source entries for Anolis, anolis-provider-sim,
  anolis-protocol, and FluxGraph.

---

## 2026-01-27

### Changed

- Updated project TODO tracking after the January site restructure.

### Removed

- Removed archived repository source entries after their content had been merged
  into the hub.
- Removed the prior changelog until the project was ready to maintain one
  consistently.

---

## 2026-01-26

### Added

- Added a new-year update post summarizing the state of the site and project.

### Changed

- Upgraded Just the Docs from 0.11.1 to 0.12.0 through Dependabot.
- Rehauled the active site structure to remove implementation domains and system
  levels from primary navigation.
- Moved implementation-domain, system-level, and related conceptual material
  into the archive.
- Simplified `_data/sources.json` after archived repositories were merged or
  retired.

### Removed

- Removed active navigation for the old implementation-domain and system-level
  pages.
- Removed some introductory, FAQ, and concept content that no longer matched the
  rehauled active structure.

---

## 2026-01-25

### Added

- Added an experimental redirect for KiCad Master Lib.

### Removed

- Removed the KiCad Master Lib redirect experiment after discovering it
  overwrote that repository's default GitHub Pages slug.

---

## 2026-01-24

### Changed

- Updated TODO tracking for upcoming documentation and project-linking work.

---

## 2026-01-23

### Added

- Added KNEEAD to the navigation and linked project data.
- Added a redirect stub for KNEEAD.
- Added "scientific automation" positioning language to the landing page.

### Changed

- Excluded the 404 fallback page from the navigation tree.
- Enforced nav ordering for implementation-domain and system-level pages.
- Converted linked project rendering to use Liquid and data-driven JSON.
- Renamed linked project data from a dotted filename to an underscore filename
  so Liquid could load it reliably.
- Merged the old Development tab into broader site documentation.
- Merged the Dependabot update for Just the Docs 0.11.1.

### Fixed

- Fixed a Liquid/JSON loading issue in linked project rendering.

### Removed

- Removed the old Development section pages after merging their content into
  the main site documentation.

---

## 2026-01-22

### Changed

- Removed syntax highlighting behavior from the site.
- Removed pyCRUMBS from navigation after it was deprecated and privately
  archived.

---

## 2026-01-05

### Changed

- Updated Just the Docs from 0.10.1 to 0.11.1 through Dependabot.

---

## 2025-11-25

### Added

- Added a call for visitors to reach out from the landing page.
- Added `Slice_RLHT`, `Slice_THRM_31855`, and `Slice_THRM_31856` to the
  projects page.

### Changed

- Renamed the docs deployment workflow for cleaner badge display.

---

## 2025-11-23

### Added

- Added `linux-wire` as an imported documentation source.
- Added KNEEAD-related TODO tracking.

### Changed

- Updated the landing page to more clearly include software in FEAST's scope.
- Merged the Dependabot update for `actions/checkout` v6.

---

## 2025-11-21

### Changed

- Updated `actions/checkout` from v5 to v6 through Dependabot.

---

## 2025-11-11

### Changed

- Removed non-ASCII characters from runnable code to improve script portability.

---

## 2025-09-26

### Changed

- Moved JSON configuration files into `_data`.
- Moved the FEAST concept draw.io asset into `assets`.
- Updated import and linked redirect scripts to read data from the new `_data`
  paths.
- Updated site architecture documentation for the new data-file layout.

---

## 2025-09-24

### Added

- Added split template slice repositories to linked project data.
- Added four PRTO slice repositories to linked project data.
- Added `Slice_THRM_31855`, `Slice_THRM_31856`, and `Slice_RLHT` to linked
  project data.

### Changed

- Reordered linked slice entries.
- Updated the projects index for the new PRTO slice entries.
- Updated site architecture documentation to match the current project and
  linked-source model.
- Shortened "nuclear" naming to `nucl` in relevant linked entries.

---

## 2025-09-14

### Added

- Added ProtoKit and DevBoardDepot to the Projects section.
- Added breakoutpack to the site.
- Added CRUMBS and pyCRUMBS as imported project sources.
- Added links to PCB projects and a new project-oriented button on the landing
  page.
- Added a custom footer.
- Added a favicon from the cornucopia logo and configured it in `_config.yml`.
- Added include-cache support and enabled the search button.
- Added the first external-project sidebar stub generator.
- Added linked project redirect generation and linked-project visual markers.

### Changed

- Updated project navigation, project descriptions, and project nav ordering.
- Added the `logger` gem to avoid Ruby standard-library deprecation issues.
- Fixed the DCMT link.
- Silenced Dart Sass dependency warnings.
- Removed an extra horizontal line from the index page.
- Renamed the "external" project model to the "linked" project model.
- Updated linked redirect generation to match exact linked project titles.

### Removed

- Removed the temporary `projects/external.md` page after moving to linked
  project terminology.
- Removed the placeholder `projects/project1.md` stub.

---

## 2025-09-13

### Added

- Added a larger initial site bootstrap with core pages, archive content,
  project pages, and a stronger landing page.
- Added a changelog for the first time.
- Added and refined a major site infrastructure post.
- Added automated redirect support for short project URLs.
- Added `jekyll-redirect-from` support.
- Added a 404 page with lowercase redirect fallback for case-variant URLs.

### Changed

- Reworked `_config.yml` to align more closely with official Just the Docs
  conventions.
- Corrected page parent references and archive paths.
- Renamed implementation-domain URLs to the plural
  `implementation-domains`.
- Simplified archive page titles by removing leading words.
- Rewrote `scripts/ensure_front_matter.py` with a cleaner structure,
  docstrings, and robust helper functions.
- Refactored the importer and front matter normalizer for redirect support.
- Updated source data for imported docs and redirect metadata.
- Polished the landing page and early warning callout.
- Updated contributing content.
- Corrected post front matter, dates, and category usage.

### Fixed

- Fixed redirect generation and imported-doc working-directory handling.
- Fixed an overly broad exception in scripts by catching a more specific error.

### Removed

- Removed the old `index.markdown` page in favor of the modern `index.md`.
- Removed the one-off `breads.html` redirect after redirect front matter support
  replaced it.

---

## 2025-09-07

### Added

- Added GitHub Actions CI and GitHub Pages deployment workflows.
- Added Dependabot configuration.
- Added `Gemfile.lock` for reproducible builds.
- Added `jekyll-seo-tag`.
- Added the x86_64 Linux platform to the lockfile for CI compatibility.
- Added site architecture documentation.
- Added archive, posts, data, and asset directories.
- Added the FEAST banner/logo asset and wired it into site configuration.
- Added FROOTS, PROTINS, SUGIRS, VEGIES, SLICE, LOAF, BATCH, and OVEN
  conceptual documentation.
- Added the first imported-docs pipeline with `scripts/import_sources.sh`,
  `scripts/ensure_front_matter.py`, and source data.
- Added KiCad Hierarchical Designs, KiCad Simulation Examples, and KiCad Master
  Lib project entries.
- Added a scheduled Pages deployment cron.

### Changed

- Moved nav ordering into page front matter.
- Improved the About page and project/content structure.
- Enforced navigation so only intended pages appeared in the sidebar.
- Updated slice links in posts to point to project sites rather than repository
  pages.
- Iterated on project URL shape, including adding/removing the `projects/`
  prefix and updating scripts accordingly.
- Updated import filtering, grouping, and front matter behavior.
- Removed private repository token handling from the import process.
- Updated README and TODO tracking.
- Restored and refined the index after several landing-page experiments.
- Fixed casing for KiCad and related project links.

### Fixed

- Fixed YAML config syntax by wrapping wildcard values.
- Fixed script delimiter handling.
- Added safety to the import script to avoid runaway or overly broad expansion.

---

## 2025-05-03

### Added

- Added `TODO.md` as a planning and project-tracking scratchpad.

---

## 2025-04-26

### Changed

- Continued iterative landing page and documentation refinements.
- Removed the standalone `feast_concept.md` file after the concept content was
  folded into the evolving site structure.

---

## 2025-04-25

### Added

- Created the repository with `.gitignore`, `LICENSE`, and `README.md`.
- Added the first Jekyll/GitHub Pages configuration and index page.
- Added the first FEAST welcome post, replacing the starter Jekyll post.
- Added early FEAST concept materials, including the draw.io concept artifact.
- Established the initial FEAST landing page content and public site identity.

### Changed

- Iterated repeatedly on the main index page copy and structure during initial
  setup.

### Removed

- Removed the default Jekyll welcome post.
