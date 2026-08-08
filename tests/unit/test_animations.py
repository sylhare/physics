from physics_explorations.visualization import create_play_pause_buttons


def _labels(buttons):
    return [b["label"] for b in buttons]


def test_play_pause_buttons_default():
    buttons = create_play_pause_buttons()
    assert _labels(buttons) == ["▶ Play", "⏸ Pause"]
    assert all(b["method"] == "animate" for b in buttons)


def test_play_pause_buttons_custom_labels():
    buttons = create_play_pause_buttons(play_label="Go", pause_label="Stop")
    assert _labels(buttons) == ["▶ Go", "⏸ Stop"]


def test_play_pause_buttons_with_reset():
    buttons = create_play_pause_buttons(include_reset=True)
    assert _labels(buttons) == ["▶ Play", "⏸ Pause", "↺ Reset"]
    # Reset jumps to the first frame ("0").
    assert buttons[-1]["args"][0] == ["0"]
