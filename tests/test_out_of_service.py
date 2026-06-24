import importlib
import sys
import types
import unittest
from unittest.mock import call, patch


detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

_original_detector = sys.modules.get("detector")
sys.modules["detector"] = detector_stub
out_of_service = importlib.import_module("features.out_of_service")

if _original_detector is None:
    sys.modules.pop("detector", None)
else:
    sys.modules["detector"] = _original_detector


class OutOfServiceTests(unittest.TestCase):
    @patch("features.out_of_service.find_image")
    def test_requires_title_and_icon(self, find_image_mock):
        find_image_mock.side_effect = [object(), object()]

        self.assertTrue(out_of_service.is_out_of_service_visible(timeout=3))
        self.assertEqual(
            find_image_mock.call_args_list,
            [
                call("pump_out_of_service_title.png", timeout=3),
                call("pump_out_of_service_icon.png", timeout=1),
            ],
        )

    @patch("features.out_of_service.find_image", return_value=None)
    def test_returns_false_without_title(self, find_image_mock):
        self.assertFalse(out_of_service.is_out_of_service_visible(timeout=3))

        find_image_mock.assert_called_once_with(
            "pump_out_of_service_title.png",
            timeout=3,
        )


if __name__ == "__main__":
    unittest.main()
