# Test sources

Prepared: 23 September 2026. Page references below are the handbook's **printed page numbers**, not zero-based PDF page indices. Recheck the official handbook and NASA clarifications before the final acceptance campaign.

| Source ID | Source and use |
|---|---|
| `DESIGN` | [Technical design source](../docs/source-documents/technical-design-reference.docx), Sections 3.1–3.5; interpreted through the controlled [design baseline](../docs/design-baseline.md) and [open items](../docs/open-items.md): our proposed dimensions, construction, electrical topology, task process and development decisions. This is a design statement, not measured evidence. |
| `TASK-DIAGRAM` | `Task-Diagram-Content.json` and `Canva-Task-Design.json`: two-page task-system diagram, saved Canva design `DAHVPxPfYbI`. |
| `DRIVE-DIAGRAM` | `Chassis-Diagram-Content.json` and `Canva-Chassis-Design.json`: drive-system diagram. Where older export wording differs, use the reviewed Section 3.3 design and record the resolved revision. |
| `NASA-2027` | [NASA 2027 HERC Handbook](https://www.nasa.gov/wp-content/uploads/2026/08/2027-herc-handbook-layout-aug6-508-1.pdf): Rules 5.3.14, 5.5.4, 6.4.2.1 and 6.4.4–6.4.8.1; RC mass scoring in Section 8.2; task details on printed pages 40–42; obstacle-specific descriptions in Section 10. |
| `KEMO` | [M148A manufacturer data](https://www.kemo-electronic.de/en/Car/Modules/M148A-Battery-guard-12-V-DC.php): negative-line switching, pack cutoff and automatic reconnect behaviour. |
| `52PI` | [EP-0225 manufacturer documentation](https://wiki-md.52pi.com/docs/EP-0225): input range, single-input selection and USB-PD output. |
| `PI` | [Raspberry Pi hardware documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html): Pi 5 power, USB budget and RTC behaviour. Match the tested OS/firmware revision. |
| `PICAMERA2` | [Picamera2 manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf): autofocus, capture queue and timing behaviour. Match the installed version. |
| `DIREWOLF` | [Dire Wolf project documentation](https://github.com/wb2osz/direwolf): software packet decoding. Record the installed version and decoder configuration. |
| `TF03` | [DFRobot SEN0328 documentation](https://wiki.dfrobot.com/sen0328/) and [communication protocol](https://wiki.dfrobot.com/sen0328/docs/21565): UART interface and frame validation. The actual TF03 revision and firmware determine the applicable pinout, frame fields and error values. |
| `COMPONENT` | Manufacturer datasheets for the **actually supplied** motors, ESCs, receiver, regulators, servos, couplings, bearings, wire and fuses. These are an acceptance prerequisite; a similar product listing cannot establish their ratings. Planned parts are listed in the [drive purchase list](../docs/source-documents/drive-purchase-list.docx) and [task purchase list](../docs/source-documents/tasks-purchase-list.docx). |
| `CAD-ONLY` | Existing `HERC-2027-Task-Visualization/Validation.json` and `Scene-measurements.json`: digital scene checks only. Their PASS status does not apply to any physical test in this folder. |

## Criteria classification

A NASA limit is labelled as a rule. A more conservative value or repeatability goal chosen by us is labelled a team criterion. A supplier rating applies only to the verified part revision and operating conditions. Unknown limits remain `TBC` in `open-criteria.csv` until we record their source and approving reviewer.

The speed rule gives 5 mph with 8 km/h in parentheses. We use **below 8.0 km/h, including measurement uncertainty**, as our conservative team acceptance criterion. Do not treat the no-slip RPM calculation as a speed measurement.

The 20 lb mass value is a scoring objective. The RC maximum is 60 lb. We will report both comparisons separately and include all mission hardware in the measured ready-state configuration.

The published task text does not resolve every parser or geometry detail. We will confirm NASA's exact message format, repeated-transmission handling, required cumulative pan range, start-state convention and RC distance datum/tolerance. We will not borrow the HP distance margin for RC.

