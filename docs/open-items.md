# Open engineering items

We close an item only after recording the responsible revision and evidence. These items are open as of this support-package edition.

| ID | Item | Required closure |
| --- | --- | --- |
| ENG-01 | Mass budget does not match the current aluminium chassis | Record installed quantities, finished aluminium mass, bearings, spindles, couplings and print masses; recompute without spare stock or double counting |
| ENG-02 | Source Section 3.2 says direct 6 mm hex coupler; Section 3.3 uses bearing-supported spindles and clamping couplings | Issue one assembly drawing and BOM for the supported-spindle design |
| ENG-03 | Source table height excludes the antenna | Measure and record the complete excursion-ready envelope, including antenna and any protruding task equipment |
| ENG-04 | 190 RPM is an example, not a measured loaded speed | Verify actual wheel speed and the limiter at full battery charge, mixed commands, restart and downhill |
| ENG-05 | Motor/ESC labels do not establish usable torque/current or supplied reverse mode | Identify delivered models and pass voltage, current, thermal, turning, climbing and stopping tests |
| ENG-06 | Receiver BEC voltage differs between some product listings | Measure the selected BEC and check receiver compatibility; retain only one positive feed |
| ENG-07 | Combined suspension wheel rate and travel have not been accepted | Measure corner loads; set geometry, spring rates, preload, travel stops and retention |
| ENG-08 | NASA packet framing, repeated-transmission handling and cumulative pan range remain to be confirmed | Configure the parser and pan hardware against the issued RC instructions, without deduplicating commands merely by letter |
| ENG-09 | RC distance reference and tolerance remain to be confirmed | Resolve sensor slant versus required reference, calibrate the correction and verify target association; do not borrow HP tolerance |
| ENG-10 | Task power and battery reserve have not been demonstrated | Verify PD negotiation, combined USB/fan loading, servo transients, low-side cutoff and endurance through review |
| ENG-11 | Technical source contains caption typo and older interface text | Use this baseline and current diagram exports when preparing the next proposal revision |
| ENG-12 | Development plan overview and detailed schedule differ | Use 30 January integration from the detailed schedule; preserve the earlier document as a source snapshot |
| ENG-13 | Historic CAD validation contains old filenames and a Blender byte-count mismatch | Fresh file hashes identify this package; old validation is labelled historical and must not be treated as a new full model inspection |

Our 20 lb mass objective is a scoring target. The handbook's RC maximum is 60 lb. This distinction does not establish that our rover has passed either mass inspection.
