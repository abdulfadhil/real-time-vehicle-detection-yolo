# Source Audit

This document records what was found in the preserved project material before the 2026 reconstruction.

## 1. Preserved academic material

The preserved academic material includes a project report dated **October 2023** and describes:

- detection of cars, trucks, bikes and people from video streams
- real-time processing as a goal
- accuracy and precision as important objectives
- image collection and manual bounding-box annotation
- resizing, normalization and augmentation
- YOLO as the selected architecture
- Keras/TensorFlow and Google Colab for training
- validation using accuracy, precision, recall and F1-score
- deployment through a backend/API

These statements are treated as project framing and planned/academic material. They are not automatically treated as measured results.

## 2. Early experimental code

An older `main.py` uses a small CNN classifier and a placeholder download URL. It is not a reliable implementation of object detection.

Another script creates random labels for video frames. That is not valid evidence of model performance.

These experimental files are therefore not carried into the reconstructed implementation.

## 3. Video-processing experiment

A separate script uses YOLOv5 and OpenCV to detect vehicle classes in a traffic video.

It counts detections frame-by-frame, but that is not the same as counting unique vehicles. It also uses machine-specific paths such as `D:/TrafficViolationDetection/traffic_video.mp4`.

## 4. YOLOv8 vehicle-flow implementation

A later implementation, committed in November 2024, contains the clearest evidence of the project's working direction.

It uses:

- `ultralytics.YOLO`
- `yolov8s.pt`
- OpenCV
- a simple center-distance tracker
- virtual horizontal counting lines
- car and bus tracking
- crossing counts
- CSV/Excel output
- a vehicle-count-over-time plot

The preserved repository history shows an initial commit on **7 November 2024** titled:

`Initial commit - uploading object detection project`

The later repository also contains commits dealing with the large `tf.mp4` video through Git LFS.

## 5. Problems found in the old implementation

The old implementation should not be reused unchanged because it contains several brittle areas:

- machine-specific absolute paths
- a fixed input filename
- model-dependent code mixed with UI/backend experiments
- a hand-written tracker rather than a maintained multi-object tracker
- truck tracking variables that were declared but not actually used in the counting loop
- CSV-writing logic placed after the main processing loop
- repeated/unfinished analytics logic
- a web page whose detection numbers are randomly generated rather than returned by the detector
- no automated tests
- visualization code tightly coupled to the processing loop
- terminology that calls directional imbalance "density"

## 6. Historical output

The preserved output artifacts include a CSV dated **2024-11-03** and an Excel workbook containing interval vehicle counts.

These artifacts establish that the earlier implementation produced local analytics output.

Their numerical results are historical project artifacts only. They are not presented as measurements from the 2026 reconstruction.

## 7. Reconstruction decision

The 2026 repository keeps the defensible core:

**vehicle detection + tracking + line crossing + flow analytics**

The implementation is intentionally smaller than the old collection of files. It removes UI simulation and hard-coded paths, isolates counting logic for tests, and leaves room for stronger tracking or custom training later.
