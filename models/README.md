# Model files

The project expects a YOLO detection checkpoint at:

```text
models/yolov8s.pt
```

The original 2024 implementation used this model family.

The weight file is intentionally excluded from Git via `.gitignore` because model artifacts can be large and may have separate licensing/distribution considerations.

For a local run:

1. Obtain the permitted YOLOv8 small detection weights.
2. Place them at `models/yolov8s.pt`.
3. Run the project with `--model models/yolov8s.pt`.

Do not commit private, modified, or unlicensed model weights to this repository.
