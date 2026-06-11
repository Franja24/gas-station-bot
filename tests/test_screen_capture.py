import unittest
from types import SimpleNamespace
from unittest.mock import patch

import screen_capture


class ScreenCaptureTests(unittest.TestCase):
    @patch("screen_capture.capture_screen", return_value="screenshot")
    def test_locate_center_on_monitor_returns_global_coordinates(
        self,
        _capture_screen_mock,
    ):
        monitor = {"left": 1440, "top": -252, "width": 2048, "height": 1152}
        box = SimpleNamespace(left=100, top=50, width=340, height=92)

        with patch.dict(
            "sys.modules",
            {"pyscreeze": SimpleNamespace(locate=lambda *args, **kwargs: box)},
        ):
            location = screen_capture.locate_center_on_monitor(
                "assets/premium.png",
                0.80,
                monitor,
            )

        self.assertEqual(location.x, 1710)
        self.assertEqual(location.y, -156)

    @patch("screen_capture.capture_screen", return_value="screenshot")
    def test_locate_center_on_monitor_returns_none_when_image_is_missing(
        self,
        _capture_screen_mock,
    ):
        class ImageNotFoundException(Exception):
            pass

        def locate_missing(*_args, **_kwargs):
            raise ImageNotFoundException("missing")

        pyscreeze = SimpleNamespace(
            ImageNotFoundException=ImageNotFoundException,
            locate=locate_missing,
        )

        with patch.dict("sys.modules", {"pyscreeze": pyscreeze}):
            location = screen_capture.locate_center_on_monitor(
                "assets/premium.png",
                0.80,
                {"left": 1440, "top": -252, "width": 2048, "height": 1152},
            )

        self.assertIsNone(location)


if __name__ == "__main__":
    unittest.main()
