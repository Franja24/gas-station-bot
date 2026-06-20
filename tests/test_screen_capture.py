import unittest
from types import SimpleNamespace
from unittest.mock import patch

import screen_capture


class ScreenCaptureTests(unittest.TestCase):
    @patch(
        "screen_capture.get_target_monitor",
        return_value={"left": 1440, "top": -252, "width": 2048, "height": 1152},
    )
    def test_target_screen_size_uses_selected_monitor(self, _monitor_mock):
        self.assertEqual(screen_capture.get_target_screen_size(), (2048, 1152))

    @patch(
        "screen_capture.get_target_monitor",
        return_value={"left": 1440, "top": -252, "width": 2048, "height": 1152},
    )
    def test_target_coordinates_are_translated_to_global_screen(
        self,
        _monitor_mock,
    ):
        self.assertEqual(
            screen_capture.to_target_screen_coordinates(429, 19),
            (1869, -233),
        )

    @patch(
        "screen_capture.get_target_monitor",
        return_value={"left": 1440, "top": -252, "width": 2048, "height": 1152},
    )
    def test_global_coordinates_are_translated_to_target_local(
        self,
        _monitor_mock,
    ):
        self.assertEqual(
            screen_capture.from_target_screen_coordinates(1869, -233),
            (429, 19),
        )

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
