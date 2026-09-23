# Measurement templates

Each CSV is a blank form. We will copy it into a run folder, duplicate rows as needed and fill actual observations. The single starter row has `NOT_RUN` status and no measured numbers.

- `mass-and-dimensions.csv`: one row per configuration/item measurement. Whole-rover mass and wheel dimensions can use separate rows.
- `wheel-suspension.csv`: one row per module and load/cycle/obstacle case. A mass in kg is not a force in N; preserve the distinction.
- `drive-electrical.csv`: one row per mode/load/motor/instrumented case. Record trace paths if peaks occur at different times.
- `speed-and-stopping.csv`: one row per direction, mixed command, power-cycle, slope or stop case. A distance/time average does not establish peak speed unless the method resolves the fastest relevant interval.
- `task-power.csv`: one row per rail/load scenario or cutoff/shutdown case. Record the probe reference so a measurement cannot silently bypass the Kemo.
- `command-execution.csv`: one row per input/executed command. Expected input is a stimulus, not a measured result. Mark stimulus type as `RECORDED_AUDIO`, `SOFTWARE_INJECTED`, `CONDUCTED_RF`, `SHIELDED_RF` or another accurately described method. Keep decoder-only and RF-path results distinct.
- `pointing-and-images.csv`: one row per pointing or capture case. Sensor timestamps are not automatically civil date/time; record the tested mapping.
- `ranging.csv`: one row per sample or defined sample aggregation. Preserve raw and corrected values separately. Define the sign of `range_error_cm` as corrected result minus independent reference. `reported_distance_ft` is derived from corrected centimetres divided by 30.48, not a second independent measurement. If validity/freshness checks fail, leave reported distance blank and record the error.
- `endurance-and-per.csv`: one row per logged phase/sample and additional rows for final review/shutdown checks. Measured energy is blank unless an instrument or documented integration of measured current/voltage/time supplies it.
- `evidence-manifest.csv`: one row per real evidence file after collection. No files or hashes are invented.

All `_iso8601` times need an explicit timezone offset or `Z`. All measurement units are in the column names. Record instrument uncertainty or a referenced method; do not add apparent precision beyond the instrument. For fields that do not apply to that row, leave the value blank and explain in notes. A real observed zero may be entered only after performing and documenting that observation; blank means unmeasured.

Use `PASS`, `FAIL`, `IN_PROGRESS` or `BLOCKED` only when justified by the actual run and criteria. Store the overall judgement and scope in `run-record.md`; one successful measurement does not pass a whole procedure. Never fill templates with catalogue specifications, the theoretical mass estimate or Blender-render values as if measured on the rover.
