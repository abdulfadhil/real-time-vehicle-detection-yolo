from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, Optional


VEHICLE_CLASSES = {"car", "motorcycle", "bus", "truck"}


@dataclass
class CrossingEvent:
    track_id: int
    vehicle_class: str
    direction: str
    frame_index: int


@dataclass
class LineCrossingCounter:
    line_y: int
    tracked_centers: Dict[int, int] = field(default_factory=dict)
    counted_track_ids: set[int] = field(default_factory=set)
    counted_a: set[int] = field(default_factory=set)
    counted_b: set[int] = field(default_factory=set)
    class_counts_a: Counter[str] = field(default_factory=Counter)
    class_counts_b: Counter[str] = field(default_factory=Counter)

    def update(
        self,
        track_id: int,
        vehicle_class: str,
        center_y: int,
        frame_index: int,
    ) -> Optional[CrossingEvent]:
        if vehicle_class not in VEHICLE_CLASSES:
            return None

        previous_y = self.tracked_centers.get(track_id)
        self.tracked_centers[track_id] = center_y

        if previous_y is None:
            return None

        # A vehicle should be counted only once during a run.
        # This prevents tracking jitter around the line from
        # generating opposite-direction duplicate events.
        if track_id in self.counted_track_ids:
            return None

        # A: object moves from below the line to above it.
        if previous_y > self.line_y >= center_y:
            self.counted_track_ids.add(track_id)
            self.counted_a.add(track_id)
            self.class_counts_a[vehicle_class] += 1

            return CrossingEvent(
                track_id,
                vehicle_class,
                "A",
                frame_index,
            )

        # B: object moves from above the line to below it.
        if previous_y < self.line_y <= center_y:
            self.counted_track_ids.add(track_id)
            self.counted_b.add(track_id)
            self.class_counts_b[vehicle_class] += 1

            return CrossingEvent(
                track_id,
                vehicle_class,
                "B",
                frame_index,
            )

        return None

    @property
    def total_a(self) -> int:
        return len(self.counted_a)

    @property
    def total_b(self) -> int:
        return len(self.counted_b)

    def snapshot(self) -> dict:
        return {
            "direction_a": self.total_a,
            "direction_b": self.total_b,
            "classes_a": dict(sorted(self.class_counts_a.items())),
            "classes_b": dict(sorted(self.class_counts_b.items())),
        }