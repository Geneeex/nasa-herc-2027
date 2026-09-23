# Planned test procedures

**Status: every procedure is NOT_RUN.** We will record actual results in a new run folder. These procedures are not evidence that the rover has passed.

Use the controlled [design baseline](../docs/design-baseline.md) and [open items](../docs/open-items.md) before the source-document wording. Source IDs refer to [sources.md](sources.md). Agree numerical team limits in `open-criteria.csv` before testing; do not choose them afterwards to fit a result.

## Before each run

We will record the complete configuration, part revisions, print settings, code commit, calibration version, battery condition, instruments, measurement uncertainty and test conditions. We will provide a clear test area, physical support for raised wheels, an accessible disconnect and a stop plan appropriate to the run. We will begin electrical checks with a current-limited supply and no moving load where practical. Stop for unstable behaviour, damage, overheating or a rating being approached. We will not force a stalled motor or short a LiPo pack to test a fuse.

## T01 — Ready-state configuration, mass and dimensions

**Sources:** DESIGN 3.1–3.3; NASA-2027 5.5.4, 6.4.2.1, 6.4.5–6.4.7 and 8.2.

We will inventory all installed mission parts, including both batteries, antenna, touchscreen, covers, wires and fixings. We will resolve the wheel coupling/spindle drawing difference and check the finished configuration against the released BOM. Using a checked scale and dimensional instruments, we will weigh the complete rover and measure the maximum ready-state length, width and height. We will separately record the camera-head height if useful, but never substitute it for overall height. Check each wheel's diameter, width, rim lip diameter, retention and material/print record.

**Acceptance:** the complete rover fits a 762 mm cube and meets the 60 lb mass limit. Report the below-20 lb team scoring objective separately; missing that target is not the same as exceeding the maximum. All mission hardware is included and both battery enclosures and main protection are present. Record uncertainty at each limit. Dimensional conformity to our drawings needs the released manufacturing tolerances.

**Record:** `mass-and-dimensions.csv`, BOM/drawing references, scale and full-envelope photos.

## T02 — Wheel, spindle and suspension module

**Sources:** DESIGN 3.2–3.3; NASA-2027 6.4.2.1 and applicable Section 10 obstacle descriptions.

We will start with one printed PETG/TPU wheel, retained spindle, two bearings, moving motor carrier, arm and paired springs. Record actual corner loads; do not assume exactly one quarter of rover weight. We will set test loads, proof margin, cycles and allowable permanent deflection from the released load calculation and component limits. Increase applied vertical and lateral loads in controlled steps, recording force, deflection and movement. Sweep suspension travel and check coupling alignment, clearance, cable flex and travel stops. Inspect rim, spokes, tyre seating, flange, bearings, pivots and fasteners before and after loading. Continue to a representative gap/rock test only after the static stage is accepted.

**Acceptance:** no cracking, separation, loose retention, binding or unintended contact; permanent set and travel are within the pre-agreed drawing/load criteria. Springs remain seated and the motor coupling stays aligned. Use the RC dimensions specified for each selected obstacle; do not scale every obstacle by a blanket factor. Record each surrogate's actual geometry and surface. No unsupported drop height, proof factor or endurance cycle count is prescribed here.

**Record:** `wheel-suspension.csv`, before/after photos, instrumented-load record, obstacle dimensions and video.

## T03 — Drive wiring, current, reverse, BEC and fuses

**Sources:** DESIGN 3.3; NASA-2027 6.4.6–6.4.7; COMPONENT.

We will verify exact motor/ESC models and 12.6 V input compatibility, continuous/peak current limits, reverse mode and LiPo protection. Before energising, trace the main positive fuse, disconnect, distribution and four individually fused motor branches. Each motor's two terminals must lead only to its ESC output pair. Check that one verified compatible BEC powers the receiver, the other BEC positive lead is insulated, and both signal grounds remain connected. Verify receiver voltage through startup and servo-free drive operation.

We will progress from supported-wheel checks to loaded forward/reverse, climbing and turning. Log individual motor, each side and battery currents where measurable, plus voltage and motor/ESC temperatures. Check reversal behaviour; brake-then-reverse behaviour must not be mistaken for direct proportional reverse. Compare measured current/time against the **actual** fuse curves, wire ratings and ESC/motor limits. Finalise the proposed 20 A main and 5 A time-delay branch values only after this review. Use an appropriately rated controlled load or supplier evidence for protection checks, not a battery short.

**Acceptance:** wiring matches the released diagram; correct voltage and neutral; no uncommanded motion; supplied ESC ratings cover two motors per side under tested conditions; currents/temperatures stay within verified limits and fuse/wire coordination is documented.

**Record:** `drive-electrical.csv`, manufacturer evidence, wiring photos, current traces and selected fuse part numbers.

## T04 — Speed limiting

**Sources:** DESIGN 3.3; NASA-2027 6.4.4.

We will measure true ground speed with a calibrated instrument or surveyed distance and reliable timing. A slow average over acceleration is not a maximum-speed measurement: record the fastest sustained and transient behaviour the instrument can resolve. We will test a fully charged 3S pack, loaded rover, forward, reverse and combined throttle/steering commands, then repeat after transmitter/receiver/ESC power cycles and startup calibration. Record mixed-channel outputs at command extremes. Repeat on the planned downhill test surface with a controlled stopping area.

**Acceptance:** each applicable case stays below our conservative 8.0 km/h criterion after allowing for uncertainty. Limiter settings persist and remain effective in both directions and during mixed steering. If the rover exceeds the limit downhill or after a power cycle, revise the limiting/braking design before accepting it. ESC output limiting alone is not evidence of closed-loop road-speed control.

**Record:** `speed-and-stopping.csv`, settings export/photos, instrument trace/video, run length, slope and full-charge voltage.

## T05 — Failsafe and stopping

**Sources:** DESIGN 3.3; COMPONENT receiver/ESC manuals.

After a supported-wheel test, we will use a clear controlled area to interrupt the RC link during forward, reverse and turning. Verify both final ESC channels reach their calibrated neutral, measure response time and stopping distance, and observe actual wheel behaviour. Test startup with transmitter absent, receiver restart and restoration of the link. Check deliberate neutral commands and the accessible disconnect separately. Log surface, slope, load and starting speed.

**Acceptance:** no unintended acceleration or restart; both channels fail to neutral; actual stopping meets the team's pre-agreed response time, distance and slope criteria. Neutral command does not itself prove braking or hill holding. These numerical limits remain TBC until the team defines its operating envelope.

**Record:** `speed-and-stopping.csv`, PWM traces, video and failsafe configuration.

## T06 — Task supplies, USB-PD and ground topology

**Sources:** DESIGN 3.4; TASK-DIAGRAM; 52PI; PI; COMPONENT.

With power removed, we will trace the four separate positive rails and confirm all task returns reach the Kemo protected load side. Check for bypasses through USB shields, mounting hardware, the drive system or test instruments. Do not attach a grounded oscilloscope or bench supply in a way that bridges the switched return; use a suitable measurement arrangement. Verify the CP2102 VCC pin is disconnected from the separately powered LiDAR.

Record EP-0225 input mode, negotiated PD capability and Pi power status. Measure 5 V UBEC and both 5.2 V converter outputs at their loads. Run the camera, SDR, screen, active cooler, LiDAR and both servo motions together. Observe voltage minima, ripple, input current, USB disconnections, undervoltage flags and resets. Verify PCA9685 logic and pull-ups at 3.3 V, pan-buffer supply/output at 5 V and FS90 signal compatibility. Check correct converter polarity before connecting loads.

**Acceptance:** verified 5 A PD capability; combined USB/fan draw fits the supported Pi budget; no backfeed, reset, USB loss or out-of-spec load voltage under the tested load sequence. Fuse, converter and guard limits are respected. The proposed 7.5/5/3/1/1 A fuses need actual current/curve review.

**Record:** `task-power.csv`, PD evidence, voltage traces, wiring photographs and power/USB logs.

## T07 — Battery guard, alarm and shutdown

**Sources:** DESIGN 3.4; KEMO; COMPONENT.

We will first use an adjustable supply and suitable test load to verify the M148A's negative-return cutoff and reconnect behaviour without draining a LiPo below its limits. Record falling-voltage cutoff, delay, rising-voltage reconnect and every branch's response. Confirm that no return bypass keeps equipment energised. Test the per-cell alarm separately with an appropriate cell simulator or supplier-approved method; it is an audible warning, not a Pi shutdown command.

For the operational workflow, save a run record, perform software shutdown, wait for completion and operate the master switch. Restart and check the saved files. Characterise unexpected power interruption only on a recoverable test image/data set; do not sacrifice the only evidence copy. Set alarm and cutoff thresholds from the actual battery and voltage-sag/endurance results.

**Acceptance:** all four task branches disconnect through the common return; reconnect is characterised; alarm threshold is recorded; the normal workflow shuts the Pi down before power removal and preserves saved results. Do not claim that the Kemo or alarm automatically performs graceful shutdown or cell balancing.

**Record:** `task-power.csv`, shutdown log, file-integrity check and threshold evidence.

## T08 — Receive and decode while hardware runs

**Sources:** DESIGN 3.4; NASA-2027 Tasks pp. 40–41; DIREWOLF.

We will test decoder/parser behaviour first with labelled recorded or synthetic AFSK audio and messages; these are test stimuli, not NASA competition recordings. Keep their provenance. Decoder audio tests do not verify the antenna or SDR RF path. For end-to-end receiver tests, use a conducted/attenuated or shielded setup with suitable equipment, or a lawful receive-only signal source. This procedure does not authorise any over-air VHF transmission. Keep the rover receive-only.

We will deliver unfamiliar 1200-baud AX.25/APRS commands at 30-second intervals while camera, servos, data saving and drive electronics operate. Compare expected input records with decoder/parser logs. Repeat with antenna placement/cable routing changes and record gain and frequency settings. NASA's assigned channel, message format and repeated-message rules remain TBC.

**Acceptance:** no dropped, reordered or unintended commands in the agreed test set; reception continues during other operations; decode latency, signal conditions and errors are reported. A successful wired software test is not a venue RF acceptance result.

**Record:** `command-execution.csv`, original stimulus, receive/decoder logs and labelled RF-test setup photos.

## T09 — Command queue and state machine

**Sources:** DESIGN 3.4; NASA-2027 6.4.8.1 and Tasks p. 40.

We will test waiting, active and ended states and every command handler with unfamiliar orderings. Check 30-degree relative turns, filter replacement, D/H completion and result association. Include repeated filter changes, G reset, malformed input, a busy capture/ranging operation when the next command arrives, and a bounded ranging failure. Verify the controller keeps the receive path active. Do not decide duplicate-packet suppression from the command letter alone; the final behaviour must follow NASA's message format.

**Acceptance:** each valid in-sequence command has one ordered outcome according to the agreed protocol; no manual task input, stored competition sequence, unintended movement or fabricated result; no unbounded queue growth in the agreed duty cycle. Log status/error for unsuccessful operations. AAA reset, out-of-sequence handling and duplicate rules must be settled before final acceptance.

**Record:** `command-execution.csv`, input provenance, code/configuration revision and raw state/event logs.

## T10 — Pan, tilt and target alignment

**Sources:** DESIGN 3.4; TASK-DIAGRAM; NASA-2027 Tasks pp. 40–42; COMPONENT.

We will measure actual camera bearing for repeated B/C moves, including reversals and approaches from both directions. Check backlash, settling, platform load, cable clearance and travel limits. Measure camera/LiDAR boresight alignment and offsets at representative target distances and heights. Use a balanced, bearing-supported tilt assembly. Confirm NASA's required cumulative pan travel before accepting the proposed positional servo.

**Acceptance:** measured angle error, repeatability and settling meet pre-agreed team criteria; the confirmed commanded range is reachable without cable strain, collision or invalid wraparound. End-stop clipping is a logged failure, not a valid 30-degree move. Target dimensions follow the handbook: the green triangle's 12 in is its height, not its side length.

**Record:** `pointing-and-images.csv`, angle references, alignment calibration and physical target measurements.

## T11 — Fresh photographs, filters and capture time

**Sources:** DESIGN 3.4; PICAMERA2; NASA-2027 Tasks p. 40.

We will change the visible scene between commands so a stale image is detectable. After motion and autofocus settle, issue D and correlate the acquired frame's timing with the checked system clock. Test E then F then D, and G then D, to show replacement rather than filter stacking. Confirm each stored image and the onboard results page display the capture date/time. Power-cycle with the RTC battery installed and verify clock retention against a known reference; the RTC does not establish the correct time by itself.

**Acceptance:** a fresh image after the required settling point; the selected filter is correct; timestamps refer to capture rather than file-write time; the clock error and method are recorded; images remain legible and saved successfully. Numeric clock/angle tolerances are team criteria, not invented NASA tolerances.

**Record:** `pointing-and-images.csv`, original camera files with metadata, independent time reference and run log.

## T12 — TF03 distance and failure handling

**Sources:** DESIGN 3.4; TF03; NASA-2027 Tasks pp. 40–42.

We will record TF03 hardware/firmware, pinout and applicable frame protocol. Confirm 3.3 V UART logic, 115200 baud and correct byte parsing/checksum. Do not apply another sensor's error codes or interpret reserved bytes as signal strength. Test known tape/survey distances to the intended board, varying lighting, target height and off-axis background surfaces. After each aim, discard old frames and validate fresh samples. Record raw sensor-to-surface range separately from the confirmed reporting datum; apply any required geometric correction before converting corrected centimetres to feet by dividing by 30.48.

We will use labelled corrupted/stale frames for software checks and safely remove/occlude the target for hardware failure checks. Verify bounded retry, `distance unavailable` output and restoration of commanded view after both success and failure. Confirm that H does not overwrite the active image filter.

**Acceptance:** correct board, valid fresh frame and range error within the agreed criterion; no old/error frame becomes a distance; reporting datum and uncertainty are stated; view/filter state is restored. Final RC distance accuracy acceptance remains blocked until NASA's reference and tolerance are confirmed. Software-injected frames prove handling logic only.

**Record:** `ranging.csv`, raw UART bytes, firmware/manual reference, independent distance survey, alignment images and event log.

## T13 — Mission and PER endurance

**Sources:** DESIGN 3.1 and 3.4; NASA-2027 5.3.14 and Tasks p. 40.

We will start with documented battery state and run a representative 12-minute excursion profile, including drive/turning loads and autonomous tasks. Continue task-system operation through a declared results-review period. Record elapsed time, current/energy where available, cell voltages, resets, temperature and task completion. The review duration and reserve margin are team criteria to set before the run. Test it; do not calculate endurance by assuming the pack's full rated capacity is usable.

**Acceptance:** required mission profile plus agreed PER duration and reserve; saved results remain available; no reset, unsafe discharge or thermal/current limit breach. Record the actual achieved duration, profile and condition rather than a general promise of runtime.

**Record:** `endurance-and-per.csv`, current/voltage/time logs and mission video.

## T14 — Onboard results presentation

**Sources:** DESIGN 3.4; NASA-2027 Tasks p. 40.

We will conduct a rehearsal with one or both pilots using only the carried rover/results display. After ZZZ, show the original captured images, capture dates/times, feet-based distances, target associations and invalid-result notices to a reviewer. Demonstrate access without pit return, external processing or help from a non-pilot. Verify that review navigation does not edit the record or trigger new task actions. Save and shut down normally after review.

**Acceptance:** every retained result is readable and traceable to the run; invalid results are not hidden; pilots can present without prohibited assistance or post-processing; saved files survive the normal shutdown/restart check.

**Record:** `endurance-and-per.csv`, reviewer observations, screen photos and the original run folder.
