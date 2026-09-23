# Calculation results

**NASA HERC 2027 TEAM BANGLADESH**

**Current assembled mass is not yet verified.** We reproduce the source arithmetic below. The source mass document still uses a printed CF-PLA chassis and brass hex couplers; the current design specifies a 6061-T6 aluminium chassis and clamping couplings. A correct sum does not resolve that design difference.

## Dimensions and unit conversions

We use 25.4 mm per inch. These are proposal dimensions, not manufactured measurements.

| Dimension | mm | in |
|---|---:|---:|
| Overall wheel diameter | 215 | 8.4646 |
| Overall wheel width | 90 | 3.5433 |
| Rim lip outer diameter | 188 | 7.4016 |
| Rim lip to tread peak | 13.5 | 0.5315 |
| Rover length | 655 | 25.7874 |
| Rover width | 630 | 24.8031 |
| Ground to camera top, excluding antenna | 421 | 16.5748 |

Rim lip to tread peak = (215 - 188) / 2 = 13.5 mm. This is the radial span including tread, not a solid TPU wall. The 421 mm camera height excludes the antenna; it is not the complete excursion-ready height.

## Speed arithmetic

No-slip speed in km/h = pi x wheel diameter in mm x wheel RPM x 60 / 1,000,000.

| Wheel RPM scenario | km/h | mph |
|---:|---:|---:|
| 190 | 7.700044 | 4.784585 |
| 200 | 8.105309 | 5.036406 |

5 mph is exactly 8.04672 km/h; at 215 mm diameter this corresponds to 198.554304 wheel RPM. Our stricter 8 km/h target corresponds to 197.401480 wheel RPM.

The 190 RPM case is a scenario, not a measured or guaranteed loaded speed. Neither RPM figure defines a validated transmitter setting. We must measure full-charge forward/reverse speed, mixed steering, startup behaviour and downhill stopping, allowing for measurement uncertainty and tyre deflection.

## Battery nominal energy

Nominal Wh = nominal V x mAh / 1000.

| Separate battery | Nominal V | Capacity (mAh) | Nominal Wh |
|---|---:|---:|---:|
| Drive | 11.1 | 5000 | 55.50 |
| Task | 11.1 | 2200 | 24.42 |

Combined nominal stored energy: 55.50 + 24.42 = 79.92 Wh. The packs remain electrically separate. This sum is not a shared available energy pool or a runtime estimate. We do not use the 12.6 V full-charge voltage to calculate nominal Wh. Runtime requires measured loads, conversion losses, cutoff behaviour and reserve through results review.

## Updated analytical wheel in the source mass document

The Google Doc read on 23 September 2026 confirms the following simplified model. These are analytical planning volumes and densities, not CAD mesh material volumes or slicer results. The model treats the 188 mm outer lip as the barrel and tyre-seat diameter; final fit geometry must be checked.

| Calculation | Result |
|---|---:|
| Rim barrel: pi x (188 squared - 182 squared) x 90 / 4000 | 156.922553 cm3 |
| PETG volume: barrel + 55 solid + 0.375 x 45 core | 228.797553 cm3 |
| PETG mass: volume x 1.27 / 1000 | 0.290572892 kg |
| Tyre envelope: pi x (205 squared - 188 squared) x 90 / 4000 | 472.252062 cm3 |
| Tyre core: pi x (200.2 squared - 192.8 squared) x 85.2 / 4000 | 194.604889 cm3 |
| Solid skins: envelope - core | 277.647173 cm3 |
| TPU volume: skins + 0.15 x core + 60 solid tread | 366.837906 cm3 |
| TPU mass: volume x 1.21 / 1000 | 0.443873867 kg |
| Historical brass hex coupler allowance | 0.0186 kg |
| One analytical wheel including historical coupler | 0.753046759 kg |
| Four analytical wheels including historical couplers | 3.012187035 kg |

The 2.4 mm skins set core diameters to 205 - 2 x 2.4 = 200.2 mm and 188 + 2 x 2.4 = 192.8 mm, and width to 90 - 2 x 2.4 = 85.2 mm. The raised tread height is (215 - 205) / 2 = 5 mm. The 55 cm3 solid and 45 cm3 core rim allowances and 60 cm3 tread allowance still need final CAD/slicer reconciliation.

The source adds its displayed values: 0.2906 + 0.4439 + 0.0186 = 0.7531 kg per wheel; four give 3.0124 kg, carried as 3.012 kg. We also retain unrounded results so rounding is visible. Bearings, spindles and motors were counted in legacy Group A; they are not added again here.

## Historical installed-equipment and body audit

We reproduce all 64 ledger rows, including exclusions, in [legacy-installed-mass.csv](legacy-installed-mass.csv). The source notes distinguish allocations, references and unresolved masses. Supplier links are retained as historical provenance, not new verification.

Legacy drive equipment: 3001.100 g. Legacy task equipment: 1458.706 g. Group A = 4.459806 kg, carried as 4.460 kg.

Legacy body formula: mass in kg = 1.21 x (solid cm3 + 0.375 x core cm3) / 1000.

| Legacy printed body part | Solid cm3 | Core cm3 | kg |
|---|---:|---:|---:|
| Chassis deck | 391.680000 | 593.920000 | 0.743424000 |
| Frame rails | 432.375904 | 207.624096 | 0.617384277 |
| Four suspension arm and bracket sets | 280.000000 | 120.000000 | 0.393250000 |
| Outer covering | 840.000000 | 0.000000 | 1.016400000 |
| Two battery and two electronics enclosures | 340.000000 | 0.000000 | 0.411400000 |
| Guards, mast and sensor/display supports | 200.000000 | 50.000000 | 0.264687500 |

Legacy Group C is 3.4465457774 kg, carried as 3.447 kg. These printed chassis volumes must not be reused for the aluminium chassis.

| Source accounting | kg |
|---|---:|
| Group A carry | 4.460 |
| Updated Group B carry | 3.012 |
| Legacy Group C carry | 3.447 |
| Source carry total | 10.919 |
| Same analytical scenario without intermediate rounding | 10.918538813 |

The earlier 185 mm rim calculation carried 10.973 kg. Revising only its wheel dimensions changes the four-wheel analytical mass by -0.053924345 kg and reproduces the source's 10.919 kg total. This reconciles the arithmetic, not the current material and hardware configuration.

## Documented estimate and scoring target

20 lb x 0.45359237 = 9.0718474 kg. The source's 10.919 kg estimate equals 24.072274 lb.

Source estimate minus target = 10.919 - 9.0718474 = 1.8471526 kg (4.072274 lb). The 60 lb maximum converts to 27.2155422 kg. These comparisons do not establish current rover compliance.

## What remains before we can report a current mass

- Replace the printed-chassis mass model with the retained aluminium sections, sheets, joints and actual suspension/carrier parts. Purchased stock and offcuts are not installed mass.
- Reconcile the current clamping couplings, spindle bearings, flanges and retention parts with the older hex-coupler accounting; count each fitted part once.
- Confirm final materials, print geometry and slicer settings for rims, tyres, covers and enclosures, then weigh representative finished parts.
- Replace planning allocations and unresolved supplier net weights with measured installed quantities and masses.
- Weigh the full excursion-ready assembly with both batteries and all fitted equipment. Keep the scale record and configuration alongside the result.

We exclude the other archived PA12/aluminium/TPU wheel mass report because it describes different materials. We do not blend that mass into the PETG/TPU design.

Generated from [inputs.json](inputs.json), [the source excerpt](../data/source-mass-calculation-excerpt.json), [the legacy ledger](../data/legacy-installed-mass-ledger.json) and [provenance](../data/calculation-provenance.json). Unit conversions use exact international inch, foot, pound and mile factors; pi-based geometry uses Python double precision. Extra digits expose the arithmetic and do not imply measurement accuracy.
