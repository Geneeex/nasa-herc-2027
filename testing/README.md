# Verification and test evidence

We will use this folder to plan, run and record rover tests. **No physical rover tests or live-radio acceptance tests are claimed in this package.** The CSV measurement fields are intentionally blank and every planned test starts at `NOT_RUN`.

Existing Blender scene checks and arithmetic checks belong to design verification. They do not establish wheel strength, motor torque, electrical reliability, radio performance, autonomy or competition compliance. Rendered task images and simulated timestamps are illustrations, not captured hardware evidence.

## Start here

1. Read [the verification matrix](verification-matrix.csv) and [test procedures](test-procedures.md).
2. Freeze the tested hardware, drawing, software and calibration revisions. Record instruments and their accuracy in the [run record](templates/run-record.md).
3. Resolve the relevant items in [open criteria](open-criteria.csv). Agree test loads, limits and measurement uncertainty **before** taking an acceptance result. `TBC` is not a passing criterion.
4. Copy the relevant blank CSV from `templates/` into a dated run folder under `evidence/`. Keep the original template blank.
5. Run only the applicable approved procedure. Preserve raw logs and unedited photos; record unsuccessful attempts as well as successful ones.
6. Review the evidence and update the matrix only for the exact build and conditions tested. A changed wheel print, motor, ESC, wiring, code or calibration may require a new run.

## Status and result rules

| Status | Meaning |
|---|---|
| `NOT_RUN` | We have not performed this test. |
| `IN_PROGRESS` | We have begun but have no complete acceptance result. |
| `PASS` | Measured evidence satisfies the recorded criterion for this build and condition. |
| `FAIL` | Evidence does not satisfy the criterion. Preserve the result and corrective action. |
| `BLOCKED` | A missing part, unresolved requirement or unavailable instrument prevents a valid test. |

Leave unmeasured numeric fields blank. Do not enter zero, a calculated prediction, an illustrative render measurement or a catalogue value as a measured result. Use a separate `not_measured_reason` or notes field for missing data. `N/A` belongs in notes with an explanation, not in a numeric column. Blank reviewer and test-date fields are not signatures or evidence of completion.

## Current design baseline

We used the supplied September design snapshots and task/chassis diagram records to prepare these procedures on 23 September 2026. Use the controlled [design baseline](../docs/design-baseline.md), [open items](../docs/open-items.md) and [development schedule](../docs/development-schedule.md) for the current decisions. The unchanged [technical source document](../docs/source-documents/technical-design-reference.docx), Sections 3.1–3.5, remains a reference with the known differences below.

- Our design uses four 215 mm by 90 mm wheels, 188 mm rim outer diameter, four suspension arms, eight springs and four dampers.
- We plan one 3S 5000 mAh drive pack and a separate 3S 2200 mAh task pack. Nominal capacity and energy are not measured endurance.
- The source reports a theoretical mass of 10.919 kg. The finished aluminium chassis, spindle hardware, batteries and all installed task parts must be weighed together before we claim a measured mass.
- The source's 421 mm height stops at the camera housing. The ready-state size check must include the antenna and every installed projection. An earlier Blender check recorded about 432 mm inclusive height; neither value substitutes for a finished-rover measurement.
- Section 3.2 still mentions a direct 6 mm hex coupler; Section 3.3 specifies a clamping coupling and bearing-supported spindle. We will resolve that drawing/BOM difference before the wheel-module acceptance test.

The source plan's 14 November 2026 drawing release and 30 January 2027 integration targets are planning dates, not dates on which tests have been performed.

## Files

- [verification-matrix.csv](verification-matrix.csv): test ID, source, criterion, evidence and current status.
- [test-procedures.md](test-procedures.md): practical steps and acceptance conditions.
- [open-criteria.csv](open-criteria.csv): rules, design decisions and numerical limits still to be confirmed.
- [sources.md](sources.md): source references used in the matrix.
- [templates/](templates/): blank run records and measurement tables.
- [evidence/README.md](evidence/README.md): evidence naming and publication instructions.

We will add real results as the rover is built. We will not use synthetic logs, generated photographs or reconstructed timestamps to fill gaps in the record.

