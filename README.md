# Real-Time Vehicle Detection & Traffic Flow Analytics

An academic computer-vision project that detects vehicles in traffic video, tracks them across frames, counts line crossings, and produces simple traffic-flow analytics.

> **Project history:** This is treated as a **2024 academic object-detection project**. The preserved source material includes an older report file dated **October 2023**, and later YOLOv8 vehicle-flow implementation evidence dates to **November 2024**. This repository is a **2026 reconstruction/publication** based on preserved materials and implementation artifacts. The reconstruction keeps the original problem and core idea while replacing brittle, hard-coded code with a small, testable pipeline.

## What it does

- Detects vehicles with YOLO
- Tracks vehicles across consecutive frames using ByteTrack
- Counts unique vehicles crossing a configurable virtual line
- Separates results by vehicle class
- Records individual crossing events
- Saves an annotated output video
- Writes machine-readable CSV and JSON results
- Supports video files and webcam input

Vehicle classes currently used from the COCO model:

- car
- motorcycle
- bus
- truck

## Problem

Traffic videos contain many moving vehicles, so manually counting vehicles and understanding directional flow is slow and inconsistent.

## Solution

The system combines object detection and multi-object tracking:

**Video → YOLO detection → ByteTrack IDs → line-crossing events → flow analytics**

The line-crossing approach is intentionally simple. It measures vehicle movement through a selected region instead of pretending that a comparison of two cumulative counts is full traffic-density estimation.

## Historical context

The original academic materials described:

- object detection from video
- vehicles such as cars, trucks and bikes
- real-time processing as a target
- YOLO-based detection
- data collection, annotation and preprocessing
- evaluation using accuracy, precision, recall and F1-score
- deployment through a backend/API

The preserved implementation later evolved into a YOLOv8 traffic-flow prototype with vehicle tracking, line crossing and exported analytics.

The source audit found that the older code mixed several experimental approaches and contained hard-coded paths, simulated web-dashboard values, and incomplete analytics. Those parts are **not** carried forward as if they were production functionality.

## Project chronology

- **2024:** Academic object-detection / vehicle-detection project chronology
- **October 2023:** Date found in a preserved report file, kept as source evidence rather than the public project year
- **November 2024:** YOLOv8 vehicle-flow implementation and local analytics artifacts
- **2026:** Reconstruction for a clean, public-safe GitHub repository

## Team

The original academic project was worked on by:

- Abdul Fadhil M
- Aswin Kumar A
- Bharathraj S

## Repository structure

```text
real-time-vehicle-detection-yolo/
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── run.py
├── docs/
│   ├── source_audit.md
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

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Model

The reconstruction uses Ultralytics YOLO for vehicle detection and ByteTrack for multi-object tracking.

The current locally validated configuration uses:

- YOLOv8n
- image size: 320
- confidence threshold: 0.35

Place the model here:

```text
models/yolov8n.pt
```

## Run

```bash
python run.py --source "path/to/video.mp4" --model "models/yolov8n.pt"
```

Useful options:

```bash
python run.py   --source "path/to/video.mp4"   --model "models/yolov8n.pt"   --output-dir outputs   --confidence 0.35   --line-position 0.50   --imgsz 320
```

Press `q` during display mode to stop early.

By default the run writes:

```text
outputs/
├── annotated.mp4
├── crossing_events.csv
└── summary.json
```

## Testing

The counting logic is dependency-light and can be tested separately:

```bash
python -m pytest -q
```

A video smoke test checks that the source can be opened and basic frame metadata can be read without running the model.

## Validation status

The current reconstruction has been validated end-to-end on a controlled 640x360, 10-second sample video using YOLOv8n with image size 320 and confidence 0.35.

Observed sample result:

- 300/300 frames processed
- 15 line-crossing events
- 13 cars
- 1 bus
- 1 truck
- annotated video generated
- crossing-events CSV generated
- summary JSON generated

These values are sample-run results for the current reconstruction, not model accuracy metrics.

The original 1920x1080 traffic video is approximately 5 minutes 6 seconds / 9,184 frames. Full-resolution processing was not completed end-to-end on the development laptop and is therefore not presented as a completed benchmark.

Real-time performance depends on hardware, input resolution, model size, confidence threshold, image size, and tracking configuration.

This repository does **not** claim:

- a newly trained custom YOLO model
- a verified new accuracy/precision/recall/F1 score
- a production traffic-management system
- traffic-light optimization
- true physical traffic-density measurement
- historical company/client data

The 2026 reconstruction is about making the real academic idea clean, reproducible, and maintainable.

## Next improvements

Possible future work, only when justified:

- custom training for a project-specific vehicle dataset
- stronger tracking configuration
- region-of-interest filtering
- speed estimation
- lane-level analysis
- calibrated traffic-density estimation
- benchmarked inference speed on local GPU/CPU

## License

This repository is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

Ultralytics YOLO is a third-party dependency and is subject to its applicable license terms. See the Ultralytics licensing documentation for details.
