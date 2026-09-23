# Reproducible rover calculations

**NASA HERC 2027 TEAM BANGLADESH**

We keep the arithmetic visible so reviewers can check our unit conversions, speed scenarios, nominal battery energy and the source mass budget. [Read the generated results](results.md).

**The current aluminium-chassis rover mass is not yet verified.** The source's 10.919 kg total can be reproduced, but its mass model still counts a printed CF-PLA chassis and brass hex couplers. It must be reconciled with the 6061-T6 chassis and clamping-coupling design before it is used as a current installed mass.

## Run

From the repository root, with Python 3.10 or newer:

```text
python calculations/calculate.py
python -m unittest discover -s tests -p test_calculations.py -v
```

There are no third-party Python dependencies or network calls. The calculation script resolves its input paths relative to itself, so it can also be run from another working directory. To write comparison outputs elsewhere, use `--output-dir PATH`. `--inputs PATH` and `--ledger PATH` accept explicit alternative files for numerical exploration; the report's source-context prose describes the committed proposal, so review that prose when changing the baseline.

## Files

| File | Purpose |
|---|---|
| `inputs.json` | Current proposal dimensions and analytical planning parameters, with their status. |
| `calculate.py` | Standard-library formulas, validation, mass reconciliation and report generation. |
| `results.md` | Readable arithmetic and the remaining limits of the mass estimate. |
| `results.json` | Machine-readable calculations; current verified mass deliberately remains `null`. |
| `legacy-installed-mass.csv` | All 64 historical component rows, quantities, unit masses, exclusions and subtotals. |
| `../data/legacy-installed-mass-ledger.json` | Source ledger with original component-reference URLs and allocation notes. |
| `../data/source-mass-calculation-excerpt.json` | Selected current Google Doc calculation text, read on 23 September 2026. |
| `../data/calculation-provenance.json` | Source descriptions and hashes, without private computer paths or author metadata. |
| `../tests/test_calculations.py` | Arithmetic, accounting and input-validation tests. |

## What these calculations establish

- The stated 215 mm wheel diameter, 90 mm width, 188 mm rim lip diameter and 13.5 mm rim-to-tread span are internally consistent. They do not establish tyre wall thickness, load rating or print fit.
- At exactly 200 wheel RPM, the no-slip speed is 8.105309 km/h. At 190 RPM it is 7.700044 km/h. The 190 RPM value is a scenario, not a measured loaded result.
- Five mph is exactly 8.04672 km/h. Our 8 km/h engineering target is slightly stricter. Neither conversion establishes a safe or effective ESC setting; actual motion must be measured at full charge in the planned operating conditions.
- The separate drive and task packs store 55.50 and 24.42 nominal Wh. Their combined 79.92 Wh is not a shared electrical supply or a runtime prediction.
- The updated source wheel formulas reproduce a 3.012187035495 kg analytical four-wheel group, including the older couplers. The source's rounded carry values reproduce 4.460 + 3.012 + 3.447 = 10.919 kg.
- The historical 10.919 kg estimate is 1.8471526 kg above the 20 lb target. This gap belongs to the old mass scenario and is not a newly measured current-rover gap.

The analytical print model separates solid skins from infilled core. It does not multiply the entire part by the infill percentage or add the overlap setting again as extra material. The 55 cm3 solid rim allowance, 45 cm3 rim-core allowance, 60 cm3 tread volume, body allowances and supplied densities are inherited planning inputs. We still need final geometry, slicer output and retained-part weights. Extra decimal places make the arithmetic traceable; they are not manufacturing accuracy claims.

## Evidence and exclusions

The current source Google Doc confirms the revised 188/182 mm rim arithmetic. A local earlier read still contained the 185/179 mm version; both are reproduced to explain the change from 10.973 to 10.919 kg. The current source still excludes aluminium stock and counts a CF-PLA body. We do not silently add raw purchased stock or combine incompatible versions.

The unrelated archived wheel report using PA12, aluminium and TPU is excluded from the PETG/TPU mass calculation. Likewise, the camera-only 421 mm height is not used to claim a complete excursion-ready height including the antenna.

The historical installed-equipment ledger contains both supplier references and design allocations. Its source URLs are provenance; they have not all been freshly reverified for this publication. Zero quantity marks exclusion or counting elsewhere, not a zero-mass component. A fitted item with missing mass causes an error instead of being silently treated as zero.

**Passing the included tests demonstrates software arithmetic, not physical rover performance, strength, runtime, task accuracy or competition compliance.** We will attach real test records after the corresponding hardware tests are performed.

Competition reference: [2027 NASA HERC Handbook](https://www.nasa.gov/wp-content/uploads/2026/08/2027-herc-handbook-layout-aug6-508-1.pdf). See the main repository design baseline and open items for integration decisions.
