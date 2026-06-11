# Nav Restructure Plan — feastorg.github.io
> Temp planning doc. Delete after implementation is complete and changelog is written.

## Goal

1. Surface Slice repos through the Slice Registry (`/slices/`) instead of the "Linked Projects" nav grouping.
2. Flatten the remaining non-Slice linked projects directly under the **Projects** nav section.
3. Slice registry table links point to each Slice's **GitHub Pages site** (not the GitHub repo).
4. Start keeping a `CHANGELOG.md` in this repo.

---

## Decision: Slice URL → GitHub Pages site

`generate_slice_index.py` currently sets `url` from `manifest.repository.url`, which resolves to
`https://github.com/feastorg/Slice_DCMT` (the GitHub repo).

We want `https://feastorg.github.io/Slice_DCMT/` instead.

**Fix:** in `extract()`, replace the `url` lambda with a constructed Pages URL:

```python
("url", lambda m: None),  # will be overridden per-repo in extract()
```

Then in `extract()`, after building the entry dict:

```python
entry["url"] = f"https://feastorg.github.io/{repo}/"
```

This is always derivable from the repo name and doesn't rely on slice.yaml content.

---

## File-by-file changes

### 1. `scripts/generate_slice_index.py`

- Remove `url` from the `EXTRACT` list.
- In `extract()`, after building `entry` from `EXTRACT`, add:
  ```python
  entry["url"] = f"https://feastorg.github.io/{repo}/"
  ```

### 2. `_data/linked_projects.json`

Remove all `Slice_*` entries. Keep only:
- `can-nano-shield`
- `can-nano-shield-fieldbus`
- `KiCad-Simulation-Examples`
- `KNEEAD`

These 4 entries keep their current `{name, title, url}` shape.

### 3. `scripts/generate_linked_redirects.py`

Change the canonical stub front matter so these 4 projects sit **directly under Projects** in the nav (no "Linked Projects" grouping):

- `parent: "Projects"` (was `"Linked Projects 🔗"`)
- Remove `grand_parent` line
- Keep `nav_order` (renumber 1–4)
- Titles: append ` 🔗` to signal external link (e.g. `"CAN Nano Shield 🔗"`)

The legacy stubs under `docs/projects/linked/` can stay as-is (nav_exclude: true).

After running the script, stale Slice_* stub files under `projects/linked/` are auto-deleted
by the existing `remove_stale_files()` call.

### 4. `projects/linked.md`

Delete this file. The "Linked Projects 🔗" grouping page is no longer needed because:
- Slices are covered by the registry at `/slices/`.
- Non-slice projects are now direct children of Projects.

Note: deleting this page will also remove the `has_children: true` parent that the old
`projects/linked/*.md` stubs depended on. The new stubs use `parent: "Projects"` which
already has `has_children: true` in `_pages/projects.md`.

### 5. `_pages/projects.md`

Remove (or simplify) the Liquid loop that renders the linked projects list. The nav itself
now carries these entries; the page body can be prose + links to child sections instead.

Also verify `has_children: true` is set (it likely already is from the Sources children).

### 6. `_pages/slices.md`

No structural change needed. The registry table already links directly to each slice's
Pages URL (after fix #1 above). The page is already a top-level nav item under Projects.

Optionally add `has_children: false` to be explicit (it doesn't need dropdown children —
the registry table *is* the listing).

### 7. `_data/slice-index.json`

Regenerate after the `generate_slice_index.py` fix so all `url` values become Pages URLs.
Can be done locally with `GITHUB_TOKEN` set, or will self-heal on next CI deploy.

---

## CHANGELOG.md (new file)

Start `CHANGELOG.md` at the repo root. Use Keep a Changelog format, date-based (no semver —
this is a site, not a versioned library).

Seed it with the major changes already made:
- Slice Registry page + auto-generation pipeline
- Badge styles
- bread-infra replacing BREADS in sources.json
- This nav restructure (once complete)

---

## Files touched summary

| File | Action |
|---|---|
| `scripts/generate_slice_index.py` | Edit — construct Pages URL from repo name |
| `_data/linked_projects.json` | Edit — remove all Slice_* entries |
| `scripts/generate_linked_redirects.py` | Edit — parent → Projects, title suffix 🔗, drop grand_parent |
| `projects/linked.md` | Delete |
| `_pages/projects.md` | Edit — remove linked projects Liquid loop |
| `_data/slice-index.json` | Regenerate (local or via CI) |
| `CHANGELOG.md` | Create |

---

## Order of operations

1. Edit `generate_slice_index.py` (Pages URL fix)
2. Edit `linked_projects.json` (drop Slice_* entries)
3. Edit `generate_linked_redirects.py` (parent/title changes)
4. Run `python3 scripts/generate_linked_redirects.py` — auto-creates 4 flat stubs, auto-deletes old Slice_* stubs
5. Delete `projects/linked.md`
6. Edit `_pages/projects.md`
7. Create `CHANGELOG.md`
8. Regenerate `_data/slice-index.json` with `GITHUB_TOKEN`
9. Commit all together
