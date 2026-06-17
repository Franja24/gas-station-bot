import json
import tempfile
import unittest
from pathlib import Path

from config.local_coordinates import (
    CoordinateConfigError,
    load_local_coordinates,
)


class LocalCoordinatesTests(unittest.TestCase):
    def test_returns_defaults_when_local_file_does_not_exist(self):
        missing_path = Path(tempfile.gettempdir()) / "missing_coordinates.json"

        coordinates = load_local_coordinates(
            "coordinates",
            {"premium.png": (640, 256)},
            path=missing_path,
        )

        self.assertEqual(coordinates, {"premium.png": (640, 256)})

    def test_merges_local_overrides(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = Path(temp_dir) / "coordinates.local.json"
            local_path.write_text(
                json.dumps(
                    {
                        "coordinates": {
                            "premium.png": [641, 257],
                            "new_button.png": [700, 300],
                        }
                    }
                ),
                encoding="utf-8",
            )

            coordinates = load_local_coordinates(
                "coordinates",
                {"premium.png": (640, 256)},
                path=local_path,
            )

        self.assertEqual(coordinates["premium.png"], (641, 257))
        self.assertEqual(coordinates["new_button.png"], (700, 300))

    def test_rejects_invalid_coordinate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = Path(temp_dir) / "coordinates.local.json"
            local_path.write_text(
                json.dumps({"coordinates": {"premium.png": ["641", 257]}}),
                encoding="utf-8",
            )

            with self.assertRaises(CoordinateConfigError):
                load_local_coordinates(
                    "coordinates",
                    {"premium.png": (640, 256)},
                    path=local_path,
                )


if __name__ == "__main__":
    unittest.main()
