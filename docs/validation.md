# Validation

## Test Results

- Automated tests: **7 passed**
- Video input: successfully processed a controlled 10-second sample at 640×360 resolution
- Frames processed: **300/300**
- Outputs generated: annotated video, crossing-events CSV, and summary JSON

## Detection Pipeline

The application uses YOLOv8 for vehicle detection, ByteTrack for tracking, and virtual line crossing to count vehicles by direction. Results are exported as CSV and JSON, with an annotated video for visual review.

## Configuration

- Model: YOLOv8n
- Image size: 320
- Confidence threshold: 0.35

## Limitations

The full 1080p traffic video was not processed end-to-end because processing was too slow on the development laptop. Full-video performance and benchmark results have not been established.

The sample results demonstrate that the tested pipeline runs; they do not establish model accuracy, precision, recall, or F1-score.