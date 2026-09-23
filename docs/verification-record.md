# Verification record: 23 September 2026

The supplied archive contains the preparation checks below. Fresh repository preparation also passed all 16 calculation tests and independently reproduced all three calculation outputs; see [the new record](publication-verification.json). No new Blender or physical test was performed during this upload.

| Check | Result | Evidence and scope |
| --- | --- | --- |
| Calculation tests | 16 passed | [Recorded output](../tests/unit-test-results.json). Covers conversions, wheel geometry, energy, speed, historical mass and invalid inputs. |
| Task Blender scene | 17 passed | [Dated scene check](../cad/fresh-scene-check.json). Covers concept geometry and example timing; includes the tested model hash. |
| Diagram layout | Visually reviewed | Three exported PNG pages were checked for legible labels, complete boxes and arrow routing. These are architecture diagrams. |
| Package structure | Checked before delivery | The verifier checks JSON, CSV columns, local Markdown links, file sizes and manifest hashes. Run `python tools/verify_package.py` to repeat it. |
| Rover hardware | Not run | The [hardware matrix](../testing/verification-matrix.csv) remains `NOT_RUN`. The measurement forms are blank. |
| GitHub workflow | Current status recorded on GitHub | [Private Actions page](https://github.com/SABIKGIT/nasa-herc-2027/actions/workflows/checks.yml); local and historical reports are separate from hosted results. |

We have not validated mechanical strength, actual vehicle speed, stopping distance, radio reception, sensor accuracy or loaded battery endurance. We also have not verified the completed rover's mass or antenna-inclusive dimensions. Those checks require the built rover and recorded measurements.

The 10.919 kg mass is the reproduced historical estimate. Its printed-body and coupler assumptions do not establish the mass of the current aluminium design. We keep that distinction in the calculation outputs and open-items register.
