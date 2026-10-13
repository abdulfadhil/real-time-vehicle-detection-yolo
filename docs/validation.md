# Sample Validation

## Configuration

The selected sample run used:

- Input: `traffic_sample.mp4`
- Model: YOLOv8s
- Frames processed: 300
- Frame rate: 30 FPS
- Resolution: 640 × 360
- Inference image size: 320
- Confidence threshold: 0.35
- Counting line: 50% of frame height

## Observed Results

| Metric | Result |
|---|---:|
| Direction A events | 0 |
| Direction B events | 14 |
| Cars | 13 |
| Trucks | 1 |
| Buses | 0 |
| Motorcycles | 0 |

The CSV records 14 crossing events. The JSON summary and annotated video are included in `outputs/sample_fixed/`.

## Interpretation

These figures describe this sample execution only. They do not establish detection accuracy, precision, recall, F1-score, ground-truth correctness, or real-time performance.

Results depend on the input footage, model weights, confidence threshold, tracking behaviour, and counting-line placement.

The full-resolution traffic video was not validated end-to-end as part of this sample run.
