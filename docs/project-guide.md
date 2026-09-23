# Project guide

This repository documents a proposed four-wheel rover and its camera/ranging task system for the 2027 NASA Human Exploration Rover Challenge. It brings design intent, source documents, procurement lists, reproducible calculations, diagrams, concept previews and a hardware verification plan into one place. It does not establish NASA acceptance, endorsement or competition compliance.

Start with the [repository overview](../README.md), then use this guide to follow the engineering decisions. The [design baseline](design-baseline.md) resolves differences between September source snapshots; [open engineering items](open-items.md) identify decisions still requiring evidence.

## 1. What exists today

| Material | What it establishes |
| --- | --- |
| Python calculations and tests | Reproducible arithmetic, input validation and historical mass accounting; the supplied record contains 16 successful checks. |
| Mechanical figure gallery | Eight supplied rover views and dimensioned figures, preserved at their original resolution. |
| Concept previews and scene reports | An illustrative rover and task scenario; a supplied historical report records 17 successful Blender scene checks. |
| Architecture diagrams | Proposed power, control, mechanical-support and task-data relationships. |
| Source documents and procurement tables | The recorded design rationale and candidate parts, including known conflicts and spares. |
| Physical verification matrix | Fourteen planned procedures, all supplied as `NOT_RUN`, with blank measurement templates. |

The supplied archive contains **no deployed rover-control firmware, editable `.blend` model, STL mesh or separate CAD release ZIP**. Scene reports and hashes identify earlier model work; the underlying native files are not available here for a fresh check. Simulated images and timestamps are demonstrations, not camera measurements. See the [verification record](verification-record.md), [CAD notes](../cad/README.md) and [test plan](../testing/README.md).

## 2. Two systems, two kinds of control

### Manual driving

A pilot commands motion using a FlySky FS-i6X transmitter. The proposed FS-iA10B receiver provides separate left/right commands to two brushed electronic speed controllers (ESCs). Each ESC controls the two motors on its side. Equal side commands move approximately straight; different commands turn by skid steering.

The planned structure uses 6061-T6 aluminium, four independent suspension arms, eight springs and four dampers. Four 12 V, 200 RPM-class gearmotors turn PETG rims with TPU 95A tyres. Each wheel is planned at 215 mm diameter and 90 mm width. A clamping coupling transfers motor torque to a supported spindle; bearings carry wheel impact and side loads. Motor and spindle supports move together with the carrier to preserve alignment.

These are design selections. Actual motor identity, usable torque, ESC reverse/braking behaviour, current limits, wheel durability, spring rates and stopping performance remain to be measured. The older direct hex-coupler description is unresolved source history, not an alternative approved assembly. Follow the [baseline](design-baseline.md) and [chassis diagram](../diagrams/README.md) before interpreting a purchase list.

### Proposed autonomous task execution

After manual positioning, the task system is intended to perform commanded camera and ranging actions onboard. Its proposed receive path is:

```text
Receive-only radio signal → RTL-SDR → FM audio → Dire Wolf decoder
                         → protocol parser → ordered queue → task controller
```

The Raspberry Pi 5 is the proposed task controller. Camera Module 3 supplies images, pan/tilt hardware changes the view, and a TF03 LiDAR supplies range samples. A carried touchscreen presents saved results. This architecture describes software that still needs implementation and integration; the calculation and diagram scripts are not that controller.

Reception must continue while the controller moves, focuses, measures and saves. An ordered queue prevents a slow action from silently losing or reordering later commands. The diagram's branches show alternative handlers, not a predetermined mission sequence. Packet framing, repeated-transmission handling and initial state still need confirmation before implementation is accepted. See [task diagrams](../diagrams/README.md) and ENG-08 in [open items](open-items.md).

## 3. Independent power domains

The drive system uses a proposed 3S 5000 mAh battery; the task system uses a separate 3S 2200 mAh battery. Their nominal energies are 55.50 Wh and 24.42 Wh respectively. Adding them gives stored-energy accounting only: one pack does not supply the other's loads, and nominal capacity does not establish endurance.

The drive architecture includes a main disconnect, protection and one verified receiver-compatible BEC supply. The task architecture distributes regulated power to the Pi, servos and LiDAR. It also includes a battery guard that switches the task return path. Correct protection, converter capability, USB power negotiation and return-path isolation must be verified on the actual assembly.

An audible battery alarm is not an automatic Pi shutdown command. The intended operating workflow must preserve results, complete a software shutdown and retain enough energy for onboard review. The [power diagram](../diagrams/README.md) is an architectural reference; complete assembly details and component acceptance belong to controlled drawings and [T03, T06 and T07 procedures](../testing/test-procedures.md).

## 4. From command to reviewable evidence

The proposed controller maintains sequence status, commanded view and active filter. A new filter selection replaces the previous selection. Temporary sensor aiming must preserve that state, including when a measurement fails.

For **images**, the design calls for motion and autofocus to settle before acquiring a fresh frame. A queued frame from before the command cannot represent its result. Capture metadata must be associated with a checked calendar clock; an RTC backup battery preserves time but does not prove its accuracy. The selected image processing occurs onboard, and the saved image is associated with its capture time and command.

For **range**, the controller must associate the sample with the intended target. Camera/LiDAR offset and alignment require calibration; a valid sensor reading can still describe the wrong surface. Samples need freshness, checksum and firmware-specific validity checks. Stale or invalid frames must produce an explicit unavailable result after bounded recovery, never a fabricated distance.

Raw sensor slant range and the final reporting reference are distinct quantities. Preserve both raw and corrected values, apply the accepted geometric correction, then convert corrected centimetres to feet by dividing by 30.48. The required reference and tolerance remain open. A temporary ranging movement must restore the commanded view after success or failure without replacing the active image filter.

Every received command, action outcome and saved result should remain traceable in a local run record. The proposed onboard gallery and distance log should expose errors as well as successes. These behaviours are design requirements tested by [T08–T14](../testing/test-procedures.md); no implemented end-to-end controller or hardware demonstration is supplied.

## 5. What the numbers mean

The [calculation results](../calculations/results.md) expose formulas and assumptions rather than hiding them behind a single headline specification. Use the [mechanical figure gallery](../cad/figures/README.md) to read the supplied dimensions alongside front, side, oblique and suspension views. These are design renderings, not measurements of an assembled rover.

- **Speed:** 215 mm wheels at exactly 200 wheel RPM yield 8.105309 km/h without slip. The 190 RPM case yields 7.700044 km/h. Both are scenarios, not measured loaded speeds or validated limiter settings.
- **Tyre geometry:** `(215 − 188) / 2 = 13.5 mm` is the rim-lip-to-tread span, not minimum printed wall thickness.
- **Height:** 421 mm is the documented camera-top height excluding the antenna. The saved concept report records about 432 mm including its model antenna. Neither establishes the complete built-rover envelope.
- **Mass:** 10.919 kg reproduces a historical estimate. Its printed CF-PLA chassis and brass couplers do not match the present aluminium and supported-spindle design. Current verified assembled mass remains unknown.

The earlier 10.973 kg estimate changed when the analytical rim dimensions were revised. Reproducing that difference reconciles arithmetic; it does not update every material and fitted part. The mass model must be rebuilt from retained aluminium, installed hardware, final printed parts and measured quantities. Purchased stock, spare parts and duplicate allocations must not inflate the installed total.

Use the [64-row historical ledger](../calculations/legacy-installed-mass.csv), [source excerpt](../data/source-mass-calculation-excerpt.json) and [provenance record](../data/calculation-provenance.json) to trace those assumptions. Extra decimal places show calculation precision, not manufacturing or measurement accuracy.

## 6. Reproduce the software checks

Use Python 3.10 or newer from the repository root:

```text
python calculations/calculate.py
python -m unittest discover -s tests -p test_calculations.py -v
python tools/verify_package.py
```

The calculation script uses Python's standard library and makes no network calls. To preserve committed reports while exploring, supply `--output-dir PATH`; alternative input and ledger options are documented in the [calculation guide](../calculations/README.md). Review source-context prose whenever changing assumptions.

The package verifier checks local links, structured-file consistency and manifest integrity. The unit tests check arithmetic and accounting behaviour. Neither executes rover hardware. Diagram regeneration has a separate Pillow dependency; see [diagram instructions](../diagrams/README.md). A new Blender scene check requires the missing native model and Blender.

## 7. Turn planned tests into real evidence

1. Select the relevant row in the [verification matrix](../testing/verification-matrix.csv) and read its [procedure](../testing/test-procedures.md).
2. Freeze hardware, drawing, software and calibration revisions. Record instruments, uncertainty and conditions in a copied [run record](../testing/templates/run-record.md).
3. Resolve applicable [open criteria](../testing/open-criteria.csv) before testing. An unset limit cannot support acceptance.
4. Copy blank forms from [templates](../testing/templates/README.md) into a dated evidence folder. Preserve templates and leave unmeasured values blank.
5. Record real observations, unsuccessful attempts, raw logs and original photographs. Link every result to the tested configuration.
6. Review the complete procedure before changing its status. Preserve failures and corrective actions; rerun affected checks after design changes.

Start with configuration, wheel/suspension and electrical checks; progress through controlled drive, receive/execute, pointing, capture and ranging tests before integrated endurance and review rehearsals. The matrix's `NOT_RUN` state is intentional. A correct calculation, catalogue rating or simulated image cannot fill a measured field.

## 8. Next milestones and repository map

The [schedule](development-schedule.md) targets orders by **16 October 2026**, bench checks by **6 November**, and wheel/suspension checks with drawing release by **14 November**. Specialist handovers target **30 December**; integrated checks target **30 January 2027**. Fault closure/retest targets **17 February**, planned ORR upload **20 February**, and three consecutive course/task runs **27 February**. These are planned gates. Because the final runs follow the upload target, readiness claims must reflect only evidence actually available on the upload date.

| Folder | Use it for |
| --- | --- |
| [`docs/`](.) | Baseline, unresolved decisions, schedule and unchanged source snapshots. |
| [`calculations/`](../calculations/README.md) | Inputs, formulas, generated reports and historical mass audit. |
| [`data/`](../data/README.md) | Procurement records and calculation provenance. |
| [`diagrams/`](../diagrams/README.md) | Architecture images and editable diagram sources. |
| [`cad/`](../cad/README.md) | Rover views and dimensioned figures, task previews, simulated results and historical scene reports. |
| [`testing/`](../testing/README.md) | Acceptance plan, open criteria, blank forms and future evidence. |
| [`tests/`](../tests/test_calculations.py) | Calculation regression and input-validation checks. |

**Terms:** ESC = electronic speed controller; BEC = receiver power regulator; APRS/AX.25 = the proposed radio-message decoding stack; LiDAR = optical ranging sensor; BOM = bill of materials; PER = post-excursion review; ORR = operational readiness review.
