from pathlib import Path

import cv2
import pytest


VIDEO_CANDIDATES = [
    Path("tf.mp4"),
    Path("data/raw/tf.mp4"),
]


@pytest.mark.skipif(
    not any(path.exists() for path in VIDEO_CANDIDATES),
    reason="No local source video supplied",
)
def test_video_opens_and_has_metadata():
    path = next(path for path in VIDEO_CANDIDATES if path.exists())

    cap = cv2.VideoCapture(str(path))
    try:
        assert cap.isOpened()
        assert cap.get(cv2.CAP_PROP_FRAME_COUNT) > 0
        assert cap.get(cv2.CAP_PROP_FPS) > 0
    finally:
        cap.release()
