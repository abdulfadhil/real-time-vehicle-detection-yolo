# Real-Time Vehicle Detection & Traffic Flow Analytics

An academic computer-vision project that detects vehicles in traffic video, tracks them across frames, counts line crossings, and produces simple traffic-flow analytics.

> **Project history:** Original academic work from **2024**. This repository is a **2026 reconstruction/publication** based on the preserved project materials and earlier implementation artifacts. The reconstruction keeps the original problem and core idea while replacing brittle, hard-coded code with a small, testable pipeline.

## What it does

- Detects vehicles with YOLO
- Tracks vehicles across consecutive frames using ByteTrack
- Counts unique vehicles crossing a configurable virtual line
- Separates results by vehicle class
- Records crossing events and interval analytics
- Saves an annotated output video
- Writes machine-readable CSV and JSON results
- Works with a video file and can be adapted to a webcam/stream

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

- **2024:** Original academic project and experiments
- **November 2024:** YOLOv8 vehicle-flow implementation produced local analytics artifacts
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
├── requirements.txt
├── run.py
├── docs/
│   └── source_audit.md
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

The project uses a YOLOv8 small detection model for continuity with the earlier implementation.

Place the model here:

```text
models/yolov8s.pt
```

The model file is intentionally ignored by Git. Keep downloaded/model artifacts out of the repository unless licensing and repository-size requirements have been reviewed.

See `models/README.md`.

## Run

```bash
python run.py --source "path/to/video.mp4" --model "models/yolov8s.pt"
```

Useful options:

```bash
python run.py   --source "path/to/video.mp4"   --model "models/yolov8s.pt"   --output-dir outputs   --confidence 0.35   --line-position 0.50   --imgsz 640
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

## Important boundary

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
