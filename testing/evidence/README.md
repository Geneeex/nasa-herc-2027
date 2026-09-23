# Real test evidence

This folder contains no completed physical-test results yet. We will add evidence only after a test is performed. The initial files in `../templates/` are forms, not results.

## Folder and file names

Use `YYYYMMDD_Txx_runNN/` for each actual run, with the real local date and a timezone in the run record. For example, the pattern `YYYYMMDD_T04_runNN/` is a naming pattern, not evidence of a speed test.

Inside a run folder use:

- `run-record.md` — configuration, method, observations and review.
- `measurements.csv` — a copy of the relevant filled template.
- `raw/` — original instrument exports, UART bytes, decoder/event logs and camera images.
- `photos/` — unedited setup and inspection photographs.
- `video/` — original test clips, or a link to an authorised team-hosted copy if too large.
- `derived/` — charts or annotated copies, clearly separated from raw files.

Name evidence files `Txx_runNN_stepNN_description.ext`. Use names such as `setup`, `scale-reading`, `wheel-before`, `wheel-after`, `receiver-power-trace` or `range-reference` only for files that actually contain that evidence. Keep each original filename in the manifest if renamed.

## What we preserve

We will photograph the tested assembly, relevant instrument reading/setup and before/after condition. Where the test depends on timing or motion, we will keep the original time series or continuous video; a single photograph cannot demonstrate maximum speed or sequence order. Record instrument units, timebase and calibration. Keep failed attempts and identify any data cleaning or excluded samples in the derived file's notes.

We will copy `../templates/evidence-manifest.csv` into the run folder and list every file, its source, type and relationship to the test. Hashes may be added after collecting real files; an empty hash field is not a verified checksum. Do not generate images, logs, signatures or timestamps to substitute for missing evidence. Label renders and injected test stimuli explicitly as `ILLUSTRATION` or `TEST_STIMULUS`, never `RAW_MEASUREMENT`.

Before publishing, we will check that we have permission to share photographs and remove personal contact details, credentials and unrelated information. Keep any redacted publication copy separate and document the redaction. Do not edit a source measurement to improve its outcome.
