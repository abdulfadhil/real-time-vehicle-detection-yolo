# Validation status

## Completed in this environment

- Python source compilation: passed
- `pytest` clean run: **4 passed, 1 skipped**
- Video I/O smoke test with the preserved 2024 `tf.mp4`: **5 passed**
- CLI help/startup without ML dependency: passed
- Source audit completed against preserved presentation, code, Git history and analytics artifacts
- No credentials, API keys or private datasets were copied into the reconstructed repository

## Not claimed

The YOLO inference path was **not executed in this environment** because the runtime does not have the `ultralytics` package installed and external package installation is unavailable here.

That is a tooling limitation, not a fabricated success. The repository therefore does not claim a new detection result, accuracy score, FPS measurement, or final model benchmark.

## First local verification

After installing the requirements and placing a permitted `models/yolov8s.pt` file in the model directory:

```bash
python run.py --source "path/to/video.mp4" --model "models/yolov8s.pt"
```

Successful execution should create:

```text
outputs/annotated.mp4
outputs/crossing_events.csv
outputs/summary.json
```

The next engineering gate is to run the real inference locally and review the annotated video plus summary counts before calling the project final.
