# Design baseline

Prepared 23 September 2026. We use this summary to resolve conflicts between the supplied September working documents. It records design intent; acceptance still depends on the tests in [our verification plan](../testing/README.md).

| Item | Current design intent | Verification still needed |
| --- | --- | --- |
| Chassis | 6061-T6 aluminium tube and sheet | Installed section sizes, joints, stiffness and mass |
| Suspension | Four independent arms; two springs per wheel, one with a damper; eight springs and four dampers total | Loaded corner weights, wheel rates, preload, travel and stops |
| Wheels | Four team-made PETG rims and TPU 95A tyres; 215 mm overall diameter, 90 mm width, 188 mm rim outer diameter | Print settings, retention, deflection, traction and measured mass |
| Tyre radial span | (215 minus 188) divided by 2 = 13.5 mm from rim lip to tread peak | This is not the minimum printed wall thickness |
| Wheel support | Two spaced spindle bearings and a retained flange; clamping coupling with 6 mm motor-side bore | Select spindle-side bore, bearing fits and shaft retention |
| Drive | Four 12 V brushed gearmotors in the 200 RPM class; one motor per wheel | Delivered motor identity, continuous torque/current and gearbox capability |
| Steering | Two New Rain brushed ESCs; each drives the two motors on one side in parallel | 12.6 V compatibility, proportional reverse, braking and current capacity |
| Drive battery | One 3S, 5000 mAh LiPo; 11.1 V nominal, 12.6 V full | Secure enclosure, measured endurance and protection settings |
| Task battery | Separate 3S, 2200 mAh LiPo; 11.1 V nominal, 12.6 V full | Power stability and endurance through results review |
| Radio control | FlySky FS-i6X mixing to FS-iA10B PWM outputs; one compatible ESC BEC feeds the receiver | Calibrated neutral, both-channel failsafe and actual link-loss stopping |
| Documented dimensions | 655 mm length, 630 mm width, 421 mm ground-to-camera-top height | 421 mm excludes the antenna; measure the complete excursion-ready rover |
| Concept CAD envelope | Recorded bounds roughly 655.078 by 630.000 by 432.000 mm including the model antenna | CAD is a concept reference, not dimensional inspection of a built rover |
| Speed | 215 mm wheels at exactly 200 wheel RPM give 8.1053 km/h before slip | The configured limiter must work at full charge, in both directions and during turning/downhill operation |
| Mass | Documented estimate 10.919 kg; current verified installed mass unavailable | Rebuild the budget for aluminium, spindle bearings, couplings and all installed hardware |

## Drive interfaces

We mount each motor and its spindle-bearing supports on the same moving carrier. The coupling transfers torque; spindle bearings carry wheel impact and side loads. The older direct hex-coupler description in the source technical document does not define this revised assembly.

Battery positive passes through a main fuse and disconnect to both ESCs. Each motor branch has its own fuse. Both motor terminals connect to the reversible ESC output pair, not directly to battery negative. Only one verified receiver-compatible BEC supplies the receiver; the other positive lead is disconnected and insulated, with both signal and ground leads retained.

## Task interfaces

Task battery positive passes through the main fuse and switch to four fused branches: EP-0225 to Pi 5; 5 V UBEC to MG996R and AHCT125; separate 5.2 V DFR0379 converters to the TF03 and FS90. The Kemo M148A switches the shared **negative return**. All load and signal grounds must pass through its protected return without a raw-negative, chassis or drive-ground bypass.

Pi/PCA9685 logic is 3.3 V. The 5 V AHCT125 buffers the pan signal; the positional FS90 accepts 3.3 V PWM. The TF03 UART/CAN version uses a verified 3.3 V UART adapter with its power output disconnected. The exact supplied sensor revision and connector pinout must be checked.

We decode live APRS commands, preserve their order, capture fresh timestamped images and measure the intended target. Temporary ranging adjustments preserve the active filter and restore the commanded view, including after failure. The onboard display presents saved results at review. No deployed rover-control software or completed end-to-end hardware demonstration is supplied in this repository.
