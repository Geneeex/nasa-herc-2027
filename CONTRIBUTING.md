# Updating our records

1. Start from the current design baseline and record what changed.
2. Update inputs and provenance when a component, quantity or dimension changes.
3. Run the calculation tests. After reviewing intended file changes, run `python tools/verify_package.py --update-manifest`, then `python tools/verify_package.py`. Commit the updated manifest with those changes.
4. Record physical test results in the appropriate template, with actual measurements and evidence paths. Blank values mean not measured.
5. Keep failed tests and the corrective revision; do not overwrite a failure with an unexplained pass.
6. Update the open-items register and schedule only when the evidence supports closure.

Code checks, CAD checks and physical tests have different scopes. Label them separately. Keep private travel/identity/financial records outside this technical repository.
