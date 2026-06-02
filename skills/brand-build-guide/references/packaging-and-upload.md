# Packaging & Upload

How to turn the generated `{{brand_slug}}-brand/` folder into a file that uploads cleanly to organizational skills. These rules are learned from real upload behavior — follow them exactly.

## 1. Hard requirements (upload will reject otherwise)

1. **Exactly one `SKILL.md`**, at the folder root (`{{brand_slug}}-brand/SKILL.md`). Supporting docs must NOT be named `SKILL.md` — put them in `references/` as `<topic>.md`. The upload API accepts only one SKILL.md per skill.
2. **Frontmatter** must have `name` and `description` as valid YAML between `---` fences.
3. **`description` ≤ 1024 characters.** This is a hard limit and the most common rejection. Count it; if over, trim (keep the core "what it does" + the most important trigger phrases). The error looks like: *"field 'description' in SKILL.md must be at most 1024 characters"*.
4. The upload accepts a **`.zip` or `.skill`** file that contains a `SKILL.md`. A zip with the skill folder at the top level works (e.g. `{{brand_slug}}-brand/SKILL.md` inside the archive) — this matches the convention of other skills in this workspace.

## 2. Exclude from the archive

`.DS_Store`, `__pycache__`, `*.pyc`, `node_modules`, and any hidden dotfiles.

## 3. Build the archive

Preferred — use the bundled packager (validates first, then zips):

```bash
python scripts/package_skill.py "<path>/{{brand_slug}}-brand" "<output-dir>"
```

It refuses to package if validation fails (missing/duplicate SKILL.md, bad frontmatter, description > 1024). On success it writes `{{brand_slug}}-brand.zip` with the folder at the top level.

Manual fallback (build in a local, non-synced dir like `/tmp`, then copy to the destination — synced/cloud folders can block zip's temp-file rename):

```bash
cd "<parent of the skill folder>"
zip -r -q -X "/tmp/{{brand_slug}}-brand.zip" "{{brand_slug}}-brand" -x '*.DS_Store' -x '*/.*'
cat "/tmp/{{brand_slug}}-brand.zip" > "<destination>/{{brand_slug}}-brand.zip"
unzip -t "<destination>/{{brand_slug}}-brand.zip"   # integrity check
```

> If `zip`/`rm` fails with "Operation not permitted" inside a synced folder, build in `/tmp` and copy the finished file with `cat … > …` (writing a new file works where in-place rewrite/delete does not).

## 4. Upload steps (organizational skills)

1. Open the skills area and choose **Upload skill**.
2. **Drag and drop** (or click to upload) the `{{brand_slug}}-brand.zip`.
3. If it reports the description is too long, trim the `description` to ≤ 1024 chars, rebuild the zip, and re-upload.
4. After upload, the skill triggers automatically on its description — no need to call it by name.

## 5. Naming

- File: `{{brand_slug}}-brand.zip`.
- Skill `name` in frontmatter: `{{brand_slug}}-brand` — match the folder name.
- Keep one brand = one skill. If the org also needs platform document templates (Current RMS, MoreApp, etc.), package those as a **separate** templates skill; do not bundle them here.
