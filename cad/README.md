# Rover figures, concept CAD and task visualisation

The mechanical figures show the proposed rover's form and annotated dimensions. The task previews explain an illustrative mission sequence. These materials document design intent; they do not establish physical performance or a completed hardware test.

## Rover views and dimensions

[![Oblique concept rendering of the four-wheel rover, suspension, camera mast and antenna](figures/rover-oblique.jpg)](figures/rover-oblique.jpg)

The [mechanical figure gallery](figures/README.md) contains all eight supplied images at their original resolution: four unannotated views and four dimensioned figures. The source images are preserved unchanged.

| View | What to inspect |
| --- | --- |
| [Front view](figures/rover-front.jpg) and [width annotation](figures/rover-width.png) | The frontal layout and the annotated 630 mm overall width. |
| [Side view](figures/rover-side.jpg) and [length/height annotations](figures/rover-length-height.png) | The annotated 655 mm length and 421 mm ground-to-camera-top height; the antenna extends above this height reference. |
| [Wheel and suspension](figures/wheel-suspension.jpg) and [wheel-width annotation](figures/wheel-width.png) | The wheel module, spring arrangement and annotated 90 mm wheel width. |
| [Wheel dimensions](figures/wheel-dimensions.png) | The annotated 215 mm overall diameter, 188 mm rim outer diameter and 13.5 mm radial span. |

The wheel figure labels the last quantity as tyre radial thickness including tread. Here, `(215 − 188) / 2 = 13.5 mm` describes the **rim-lip-to-tread span**, not the minimum printed wall thickness. Likewise, the 421 mm annotation is **camera-top height**, not the full antenna-inclusive envelope. See the [design baseline](../docs/design-baseline.md) for the dimensions and remaining verification work.

These raster figures do not supply editable CAD or establish the geometry of the separately referenced native models. The saved Blender check history below retains its original scope.

## Task-scene previews

![Illustrative task-site layout](previews/01-Task-site.png)

The site layout and camera results are illustrative. They do not prove radio reception, autonomous execution, sensor accuracy, climbing ability or structural strength.

- [Target geometry](previews/02-Target-dimensions.png)
- [Image capture](previews/03-Rover-image-capture.png)
- [Distance measurement](previews/04-Distance-measurement.png)
- [Simulated results](previews/05-Task-results.png)

The `simulation/` images are rendered examples, not Camera Module 3 photographs. Their dates are simulation labels. All three example targets use known placed coordinates: 20, 35 and 48 ft from the start mark. Sensor-to-target slant ranges differ because the sensor is offset and elevated. See [example scene measurements](example-scene-measurements.json).

## Editable models

The source package references a separate `NASA-HERC-2027-CAD-Release.zip` with the following expected assets. **That ZIP and these native files were not supplied with this repository upload:**

- `NASA-HERC-2027-Team-Bangladesh-Tasks.blend`: eight scenes, packed simulated captures and 1,062 separate rover parts.
- `NASA-HERC-2027-Rover-Concept.blend`: separate-parts concept assembly.
- `NASA-HERC-2027-Rover-Concept-mm.stl`: full assembled mesh in millimetres, retaining independent component surfaces.

When that ZIP becomes available, verify it against `release-assets.json` and attach it to a release in this private repository. No CAD release or download link is available in this edition.

Open the task Blender file and select a scene. Playback is illustrative and accelerated: one playback second represents 30 mission seconds. It does not decode radio or run the rover's task software. These concept models are not released manufacturing drawings for the revised aluminium chassis and supported spindle assembly.

STL carries no unit metadata or component tree. Import this STL as **millimetres**; CAD software may merge touching bodies. A SolidWorks import test is not established by the source files. Blender preserves the separate named objects.

## Check history and integrity

Our [fresh task-scene check](fresh-scene-check.json), run with Blender 4.3.2 on 23 September 2026, passed 17 checks covering object count, bounds, target geometry and illustrative timing. Its recorded model hash matches the expected entry in `release-assets.json`; the native model was not available for a new check during this upload. This check does not validate the separate rover-only file or physical performance. [Historical scene validation](historical-scene-validation.json) records earlier geometry checks. [Release file hashes](release-assets.json) identify the expected native model bytes for the separately referenced CAD bundle. A checksum verifies identity, not mechanical performance. The source package notes a historical Blender byte-count mismatch; native files are unavailable here, so no new verification of that discrepancy is claimed.

The saved task scene records an envelope near 655.078 by 630.000 by 432.000 mm. The proposal's 421 mm height excludes its antenna. Neither number replaces measurement of the completed rover.

For a fresh concept-scene check, extract the release ZIP and run:

```text
blender --background PATH_TO_TASKS_BLEND --python tools/check_task_scene.py -- --output cad/fresh-scene-check.json
```

Use the actual file path in place of `PATH_TO_TASKS_BLEND`. This optional check runs inside Blender and writes its own date and tested scope. It does not run in the ordinary Python/GitHub test job.
