# Real-Time Vehicle Detection & Traffic Flow Analytics

A computer-vision project that detects vehicles in traffic videos, tracks their movement across frames, counts virtual line crossings, and exports traffic-flow results.

## Features

- Vehicle detection using YOLOv8
- Multi-object tracking with ByteTrack
- Direction-based line-crossing counts
- Vehicle classification for cars, motorcycles, buses, and trucks
- Annotated video output
- Crossing-event CSV and summary JSON exports
- Video file and webcam input support

## How It Works

**Video Input → YOLOv8 Detection → ByteTrack Tracking → Line-Crossing Detection → Traffic-Flow Results**

The system tracks vehicles across frames and records each tracked vehicle's first qualifying line-crossing event. It reports counts by vehicle class and direction.

## Tech Stack

- Python
- Ultralytics YOLOv8
- OpenCV
- ByteTrack
- NumPy
- pytest

## Project Structure

```text
real-time-vehicle-detection-yolo/
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── run.py
├── docs/
│   └── validation.md
├── models/
│   └── README.md
├── outputs/
│   └── .gitkeep
├── src/
│   └── vehicle_flow/
│       ├── __init__.py
│       └── counter.py
└── tests/
    ├── test_counter.py
    ├── test_run.py
    └── test_video_io.py
```

## Requirements

- Python 3.10 or newer
- A compatible YOLOv8 model weight file
- Video input or a webcam

## Setup

Create and activate a virtual environment.

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Model Setup

The tested configuration used YOLOv8n with an image size of 320 and a confidence threshold of 0.35. The default image size is 640.

Place the permitted model weights at:

```text
models/yolov8n.pt
```

See [`models/README.md`](models/README.md) for model setup instructions.

## Run the Project

To process a video file:

```bash
python run.py --source "path/to/video.mp4" --model "models/yolov8n.pt"
```

To use your default webcam:

```bash
python run.py --source 0 --model "models/yolov8n.pt" --display
```

By default, the application writes its results to `outputs/`:

- `annotated.mp4` — video with detections and tracking information
- `crossing_events.csv` — individual crossing events
- `summary.json` — aggregated counts

Press `q` during display mode to stop processing early.

## Testing

Run the automated tests with:

```bash
python -m pytest -q
```

The current test suite contains seven tests covering counting logic, runner error handling, and video input handling.

## Validation

The pipeline was tested on a controlled 10-second video at 640 × 360 resolution.

- Frames processed: 300/300
- Line-crossing events: 15
- Cars: 13
- Buses: 1
- Trucks: 1
- Generated outputs: annotated video, CSV, and JSON

The full-resolution traffic video was not processed end-to-end. These sample results demonstrate pipeline execution; they do not establish model accuracy, precision, recall, F1-score, or real-time performance.

## Limitations and Future Work

Current results depend on the input video, tracking behaviour, model configuration, and available hardware. The system provides line-crossing analytics rather than calibrated physical traffic-density measurements.

Potential improvements include region-of-interest filtering, speed estimation, lane-level analysis, custom model training, and performance benchmarking.

## Project Background

Developed as a team project focused on vehicle detection, tracking, and traffic-flow analysis using computer vision.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See [`LICENSE`](LICENSE) for the full license text.

Ultralytics YOLO is a third-party dependency subject to its applicable license terms.