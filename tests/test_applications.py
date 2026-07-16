import unittest
from unittest.mock import patch
from types import SimpleNamespace

from features import applications


class OpenAnyDeskTests(unittest.TestCase):
    @patch("features.applications.save_screenshot")
    @patch("features.applications._frontmost_app_name", return_value="AnyDesk")
    @patch("features.applications._activate_app")
    def test_open_anydesk_verifies_frontmost_app(
        self,
        activate_app_mock,
        _frontmost_app_name_mock,
        save_screenshot_mock,
    ):
        applications.open_anydesk()

        activate_app_mock.assert_called_once_with(
            applications.ANYDESK_BUNDLE_ID,
            "AnyDesk",
        )
        save_screenshot_mock.assert_called_once_with("anydesk_opened")

    @patch("features.applications.time.sleep")
    @patch("features.applications.time.monotonic", side_effect=[0, 1, 11])
    @patch("features.applications.save_screenshot")
    @patch("features.applications._frontmost_app_name", return_value="Codex")
    @patch("features.applications._activate_app")
    def test_open_anydesk_stops_when_app_is_not_frontmost(
        self,
        _activate_app_mock,
        _frontmost_app_name_mock,
        save_screenshot_mock,
        _monotonic_mock,
        _sleep_mock,
    ):
        with self.assertRaisesRegex(RuntimeError, "app al frente: Codex"):
            applications.open_anydesk()

        save_screenshot_mock.assert_called_once_with("anydesk_not_frontmost")

    @patch("features.applications.save_screenshot")
    @patch("features.applications.time.sleep")
    @patch("features.applications._select_rustdesk_kiosco_tab")
    @patch("features.applications._raise_rustdesk_window")
    @patch(
        "features.applications._rustdesk_window_names",
        return_value=["RustDesk", "KIOSCO@tpv02-6588 - Remote Desktop - RustDesk"],
    )
    @patch("features.applications._activate_app")
    def test_open_rustdesk_prefers_existing_kiosco_window(
        self,
        activate_app_mock,
        _window_names_mock,
        raise_window_mock,
        select_tab_mock,
        _sleep_mock,
        save_screenshot_mock,
    ):
        applications.use_remote_desktop("rustdesk")

        applications.open_anydesk()

        activate_app_mock.assert_called_once_with(
            applications.RUSTDESK_BUNDLE_ID,
            "RustDesk",
        )
        raise_window_mock.assert_called_once_with(
            "KIOSCO@tpv02-6588 - Remote Desktop - RustDesk"
        )
        select_tab_mock.assert_called_once_with()
        save_screenshot_mock.assert_called_once_with("rustdesk_remote_window_opened")

    @patch("features.applications.save_screenshot")
    @patch("features.applications.time.sleep")
    @patch("features.applications._select_rustdesk_kiosco_tab")
    @patch("features.applications._raise_rustdesk_window")
    @patch(
        "features.applications._rustdesk_window_names",
        side_effect=[
            ["RustDesk"],
            ["RustDesk", "KIOSCO@tpv02-6588 - Remote Desktop - RustDesk"],
        ],
    )
    @patch(
        "features.applications._front_rustdesk_window_details",
        return_value={"name": "RustDesk", "x": 15, "y": 38, "width": 1014, "height": 709},
    )
    @patch("features.applications.double_click_coordinates")
    @patch("features.applications._activate_app")
    def test_open_rustdesk_connects_first_kiosco_from_home(
        self,
        _activate_app_mock,
        double_click_coordinates_mock,
        _front_window_mock,
        _window_names_mock,
        raise_window_mock,
        select_tab_mock,
        _sleep_mock,
        _save_screenshot_mock,
    ):
        applications.use_remote_desktop("rustdesk")

        applications.open_anydesk()

        double_click_coordinates_mock.assert_called_once_with(390, 468)
        raise_window_mock.assert_called_once_with(
            "KIOSCO@tpv02-6588 - Remote Desktop - RustDesk"
        )
        select_tab_mock.assert_called_once_with()

    @patch("features.applications.save_screenshot")
    @patch("features.applications.time.sleep")
    @patch("features.applications._select_rustdesk_kiosco_tab")
    @patch("features.applications._raise_rustdesk_window")
    @patch(
        "features.applications._rustdesk_window_names",
        return_value=["370897792@tpv02-6588 - Remote Desktop - RustDesk", "RustDesk"],
    )
    @patch("features.applications._activate_app")
    def test_open_rustdesk_selects_kiosco_tab_from_other_remote_tab(
        self,
        _activate_app_mock,
        _window_names_mock,
        raise_window_mock,
        select_tab_mock,
        _sleep_mock,
        _save_screenshot_mock,
    ):
        applications.use_remote_desktop("rustdesk")

        applications.open_anydesk()

        raise_window_mock.assert_called_once_with(
            "370897792@tpv02-6588 - Remote Desktop - RustDesk"
        )
        select_tab_mock.assert_called_once_with()

    @patch("features.applications.open_anydesk")
    @patch("features.applications.use_remote_desktop")
    def test_open_rustdesk_sets_selection_and_opens(
        self,
        use_remote_desktop_mock,
        open_anydesk_mock,
    ):
        applications.open_rustdesk()

        use_remote_desktop_mock.assert_called_once_with("rustdesk")
        open_anydesk_mock.assert_called_once_with()

    @patch("features.applications.use_windows_path", return_value=True)
    @patch("features.applications.save_screenshot")
    @patch("features.applications.time.sleep")
    @patch("features.applications.pygetwindow", create=True)
    def test_windows_rustdesk_prefers_existing_remote_window(
        self,
        pygetwindow_mock,
        _sleep_mock,
        save_screenshot_mock,
        _use_windows_path_mock,
    ):
        remote_window = SimpleNamespace(
            title="370945606@tpv02-6588",
            isMinimized=False,
            restore=lambda: None,
            activate=unittest.mock.Mock(),
        )
        pygetwindow_mock.getAllWindows.return_value = [
            SimpleNamespace(title="RustDesk"),
            remote_window,
        ]
        applications.use_remote_desktop("rustdesk")

        applications.open_anydesk()

        remote_window.activate.assert_called_once_with()
        save_screenshot_mock.assert_called_once_with("rustdesk_remote_window_opened")

    @patch("features.applications.subprocess.Popen")
    @patch("features.applications.os.path.isfile", return_value=True)
    @patch.dict(
        "features.applications.os.environ",
        {applications.RUSTDESK_COMMAND_ENV: r"C:\Program Files\RustDesk\RustDesk.exe"},
        clear=False,
    )
    def test_windows_command_runs_exe_paths_with_spaces(
        self,
        _isfile_mock,
        popen_mock,
    ):
        applications._run_windows_command(
            applications.RUSTDESK_COMMAND_ENV,
            "RustDesk",
        )

        popen_mock.assert_called_once_with(
            [r"C:\Program Files\RustDesk\RustDesk.exe"]
        )


if __name__ == "__main__":
    unittest.main()
