from vehicle_flow.counter import LineCrossingCounter


def test_counts_a_crossing_once():
    counter = LineCrossingCounter(line_y=100)

    assert counter.update(1, "car", 120, 1) is None
    event = counter.update(1, "car", 90, 2)

    assert event is not None
    assert event.direction == "A"
    assert event.vehicle_class == "car"
    assert counter.total_a == 1

    # Re-entering the same direction must not double count the same track.
    assert counter.update(1, "car", 80, 3) is None
    assert counter.total_a == 1


def test_counts_b_crossing_once():
    counter = LineCrossingCounter(line_y=100)

    assert counter.update(2, "bus", 80, 1) is None
    event = counter.update(2, "bus", 120, 2)

    assert event is not None
    assert event.direction == "B"
    assert counter.total_b == 1
    assert counter.class_counts_b["bus"] == 1


def test_same_track_cannot_be_counted_in_both_directions():
    counter = LineCrossingCounter(line_y=100)

    # First crossing: B.
    event = counter.update(3, "car", 80, 1)
    assert event is None

    event = counter.update(3, "car", 120, 2)
    assert event is not None
    assert event.direction == "B"

    # Tracking jitter moves the same vehicle back across the line.
    # It must not create a second event in direction A.
    event = counter.update(3, "car", 90, 3)

    assert event is None
    assert counter.total_a == 0
    assert counter.total_b == 1
    assert counter.class_counts_b["car"] == 1


def test_ignores_non_vehicle_classes():
    counter = LineCrossingCounter(line_y=100)

    assert counter.update(4, "person", 120, 1) is None
    assert counter.update(4, "person", 80, 2) is None
    assert counter.total_a == 0
    assert counter.total_b == 0


def test_two_vehicle_classes_are_tracked_independently():
    counter = LineCrossingCounter(line_y=100)

    counter.update(10, "car", 120, 1)
    counter.update(10, "car", 90, 2)

    counter.update(11, "truck", 80, 1)
    counter.update(11, "truck", 120, 2)

    assert counter.snapshot() == {
        "direction_a": 1,
        "direction_b": 1,
        "classes_a": {"car": 1},
        "classes_b": {"truck": 1},
    }