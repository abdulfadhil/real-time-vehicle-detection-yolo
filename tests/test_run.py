import sys
import types

import cv2
import pytest

import run


def test_capture_released_when_model_loading_fails(monkeypatch, tmp_path):
    class FakeCapture:
        def __init__(self):
            self.released = False

        def isOpened(self):
            return True

        def get(self, property_id):
            values = {
                cv2.CAP_PROP_FRAME_WIDTH: 640,
                cv2.CAP_PROP_FRAME_HEIGHT: 360,
                cv2.CAP_PROP_FPS: 30,
            }
            return values.get(property_id, 0)

        def release(self):
            self.released = True

    capture = FakeCapture()
    monkeypatch.setattr(cv2, "VideoCapture", lambda source: capture)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run.py",
            "--source", "sample.mp4",
            "--model", "missing-model.pt",
            "--output-dir", str(tmp_path),
        ],
    )

    fake_ultralytics = types.ModuleType("ultralytics")

    def fail_to_load_model(model_path):
        raise RuntimeError("Model loading failed")

    fake_ultralytics.YOLO = fail_to_load_model
    monkeypatch.setitem(sys.modules, "ultralytics", fake_ultralytics)

    with pytest.raises(RuntimeError, match="Model loading failed"):
        run.main()

    assert capture.released is True