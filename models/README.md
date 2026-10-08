# Model files

The project uses a YOLO detection checkpoint for vehicle detection.

The current validated configuration uses:

```text
models/yolov8n.pt
```

The original 2024 implementation used YOLOv8s. The 2026 reconstruction uses YOLOv8n as the validated local configuration.

The weight file is intentionally excluded from Git via `.gitignore` because model artifacts can be large and may have separate licensing or distribution considerations.

For a local run:

1. Obtain permitted YOLOv8n detection weights.
2. Place them at `models/yolov8n.pt`.
3. Run the project with `--model models/yolov8n.pt`.

Do not commit private, modified, or unlicensed model weights to this repository.
