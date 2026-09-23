# Maintaining the private repository

This support package is maintained in **[SABIKGIT/nasa-herc-2027](https://github.com/SABIKGIT/nasa-herc-2027)**. Repository visibility is **private**, as selected by the owner. Only authorized collaborators can read it. Do not change visibility or enable public Pages as part of an ordinary update.

## Update the source and evidence

```bash
git clone https://github.com/SABIKGIT/nasa-herc-2027.git
cd nasa-herc-2027
git switch -c design-update
```

Edit the intended baseline, code, documentation or real test record. Follow [CONTRIBUTING.md](CONTRIBUTING.md), preserving the source snapshots and distinguishing calculations, concept scenes and measured evidence.

```bash
python -m unittest discover -s tests -v
python calculations/calculate.py
# Only after reviewing the intended changes:
python tools/verify_package.py --update-manifest
python tools/verify_package.py
git add .
git commit -m "Update rover design and verification records"
git push -u origin design-update
```

Open a pull request to `main` and check [GitHub Actions](https://github.com/SABIKGIT/nasa-herc-2027/actions/workflows/checks.yml). The workflow validates software arithmetic and package integrity; it does not validate rover hardware. Python 3.12 matches the hosted environment.

The manifest normalizes text line endings, including the SVG README banner. Its source byte counts describe the captured files; normalized hashes provide the cross-platform integrity comparison. Generated reports should be reviewed before refreshing checksums.

## Native CAD remains a separate delivery

The supplied support ZIP includes CAD previews, scene measurements, hashes and historical reports, but no native Blender or STL models. The separate `NASA-HERC-2027-CAD-Release.zip` was not supplied for this upload, so no CAD release has been created.

When it is provided, verify its assets against [cad/release-assets.json](cad/release-assets.json), add it to a release in this same private repository, and record the private release URL in [cad/README.md](cad/README.md). Keep the transport ZIP outside the normal source tree. Repository access is required to download private release assets.

## Reuse terms

The original software code listed in [LICENSING.md](LICENSING.md) is covered by the [MIT License](LICENSE), copyright (c) 2026 **Sabik Bin Sultan**. This grant does not cover research and design documents, CAD, figures, photographs, diagrams, data or other excluded materials. Existing attribution, coauthor rights and third-party terms remain unchanged. Keep the repository private; access does not expand the licensing scope or grant additional redistribution rights for excluded materials.
