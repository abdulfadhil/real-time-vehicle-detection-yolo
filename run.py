from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import cv2

# Keep the CLI importable even when the optional ML dependency is not installed.
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vehicle_flow.counter import LineCrossingCounter, VEHICLE_CLASSES


COCO_VEHICLE_IDS = {
    "car": 2,
    "motorcycle": 3,
    "bus": 5,
    "truck": 7,
}



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect, track and count vehicles crossing a virtual line."
    )
    parser.add_argument("--source", required=True, help="Video path or webcam index.")
    parser.add_argument("--model", required=True, help="YOLO model path, e.g. models/yolov8n.pt")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--confidence", type=float, default=0.35)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--line-position", type=float, default=0.50)
    parser.add_argument("--display", action="store_true")

    args = parser.parse_args()

    if not 0.0 < args.confidence <= 1.0:
        parser.error("--confidence must be greater than 0 and at most 1.")

    if args.imgsz <= 0:
        parser.error("--imgsz must be a positive integer.")

    if not 0.0 <= args.line_position <= 1.0:
        parser.error("--line-position must be between 0 and 1, inclusive.")

    return args





def as_capture_source(value: str):
    return int(value) if value.isdigit() else value


def main() -> int:
    args = parse_args()

    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit(
            "ultralytics is not installed. Run: python -m pip install -r requirements.txt"
        ) from exc

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    source = as_capture_source(args.source)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SystemExit(f"Could not open video source: {args.source}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    line_y = int(height * args.line_position)

    try:
        model = YOLO(args.model)
    except Exception:
        cap.release()
        raise

    counter = LineCrossingCounter(line_y=line_y)

    output_video = output_dir / "annotated.mp4"
    events_csv = output_dir / "crossing_events.csv"
    summary_json = output_dir / "summary.json"

    writer = cv2.VideoWriter(
        str(output_video),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        cap.release()
        raise SystemExit(f"Could not create output video: {output_video}")

    events = []
    frame_index = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame_index += 1

            result = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                classes=list(COCO_VEHICLE_IDS.values()),
                conf=args.confidence,
                imgsz=args.imgsz,
                verbose=False,
            )[0]

            annotated = frame.copy()
            cv2.line(
                annotated,
                (0, line_y),
                (width, line_y),
                (0, 220, 120),
                2,
            )
            cv2.putText(
                annotated,
                "COUNTING LINE",
                (20, max(30, line_y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 220, 120),
                2,
                cv2.LINE_AA,
            )

            boxes = result.boxes
            if boxes is not None and len(boxes) > 0:
                ids = boxes.id.int().tolist() if boxes.id is not None else [None] * len(boxes)
                xyxy = boxes.xyxy.int().tolist()
                classes = boxes.cls.int().tolist()
                confs = boxes.conf.float().tolist()

                names = result.names

                for track_id, box, class_id, confidence in zip(
                    ids, xyxy, classes, confs
                ):
                    label = str(names[class_id]).lower()
                    if label not in VEHICLE_CLASSES:
                        continue

                    x1, y1, x2, y2 = box
                    center_y = (y1 + y2) // 2

                    event = None
                    if track_id is not None:
                        event = counter.update(
                            int(track_id),
                            label,
                            center_y,
                            frame_index,
                        )

                    if event is not None:
                        events.append(
                            {
                                "frame": event.frame_index,
                                "track_id": event.track_id,
                                "vehicle_class": event.vehicle_class,
                                "direction": event.direction,
                                "time_seconds": round(event.frame_index / fps, 3),
                            }
                        )

                    text = f"{label} #{track_id}" if track_id is not None else label
                    text += f" {confidence:.2f}"
                    cv2.rectangle(
                        annotated,
                        (x1, y1),
                        (x2, y2),
                        (255, 180, 0),
                        2,
                    )
                    cv2.putText(
                        annotated,
                        text,
                        (x1, max(25, y1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 180, 0),
                        2,
                        cv2.LINE_AA,
                    )

            snapshot = counter.snapshot()
            cv2.putText(
                annotated,
                f"A: {snapshot['direction_a']}  B: {snapshot['direction_b']}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            writer.write(annotated)

            if args.display:
                cv2.imshow("Vehicle Detection", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        cap.release()
        writer.release()
        cv2.destroyAllWindows()

    with events_csv.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "frame",
            "track_id",
            "vehicle_class",
            "direction",
            "time_seconds",
        ]
        writer_csv = csv.DictWriter(handle, fieldnames=fieldnames)
        writer_csv.writeheader()
        writer_csv.writerows(events)

    snapshot = counter.snapshot()
    summary = {
        "source": str(args.source),
        "model": str(args.model),
        "frames_processed": frame_index,
        "fps": fps,
        "resolution": {"width": width, "height": height},
        "counting_line_y": line_y,
        "confidence_threshold": args.confidence,
        "image_size": args.imgsz,
        "vehicle_classes": sorted(VEHICLE_CLASSES),
        "direction_a_total": snapshot["direction_a"],
        "direction_b_total": snapshot["direction_b"],
        "direction_a_by_class": snapshot["classes_a"],
        "direction_b_by_class": snapshot["classes_b"],
        "events": len(events),
        "outputs": {
            "annotated_video": str(output_video),
            "crossing_events_csv": str(events_csv),
            "summary_json": str(summary_json),
        },
    }

    summary_json.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
