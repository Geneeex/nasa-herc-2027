# Concept CAD and task visualisation

We use this model to explain the proposed rover and task sequence. The site layout and camera results are illustrative. They do not prove radio reception, autonomous execution, sensor accuracy, climbing ability or structural strength.

![Illustrative task-site layout](previews/01-Task-site.png)

## Preview figures

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
