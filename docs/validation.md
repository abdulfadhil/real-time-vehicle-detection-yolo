# Validation status

## Completed in the development environment

- Python environment created and dependencies installed successfully
- `pytest` clean run: **6 passed, 1 skipped**
- Vehicle-counting regression tests cover direction A, direction B, duplicate counting prevention, non-vehicle filtering, and independent vehicle classes
- YOLOv8n model loaded successfully from `models/yolov8n.pt`
- End-to-end video processing completed on a controlled **640x360, 10-second sample**
- Sample video processing completed: **300/300 frames**
- Sample output included an annotated video, crossing-events CSV, and summary JSON
- Source audit completed against preserved project report, code, Git history, and historical analytics artifacts
- Model files, input videos, generated outputs, and virtual-environment files are excluded from Git
- No credentials, API keys, or private datasets were copied into the reconstructed repository

## Current validated configuration

```text
Model: YOLOv8n
Image size: 320
Confidence threshold: 0.35
Input sample: 640x360, 10 seconds
Frames processed: 300
```

These are sample-run event counts from the current reconstruction. They are not model accuracy, precision, recall, F1, or benchmark metrics.

## Full-source limitation

The preserved traffic video is approximately:

```text
Resolution: 1920x1080
Frame rate: 30 FPS
Frames: 9,184
Duration: approximately 5 minutes 6 seconds
```

Full-resolution processing was attempted locally but was not completed end-to-end because processing was too slow on the development laptop.

Therefore, this project does not claim successful full-video processing or a measured full-video FPS benchmark.

## Historical project evidence

Earlier 2024 project artifacts include a YOLOv8 vehicle-flow implementation and local analytics outputs. These are preserved as historical evidence and are not presented as new measurements from the 2026 reconstruction.

## Final validation boundary

The current reconstruction is technically functional for the validated sample pipeline:

**video input -> YOLO detection -> ByteTrack tracking -> line crossing -> CSV/JSON analytics -> annotated video**

Further performance optimization, full-source benchmarking, custom training, and advanced traffic analytics remain future work.