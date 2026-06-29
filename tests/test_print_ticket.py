import sys
import types
import unittest
from unittest.mock import call, patch


clicker_stub = types.ModuleType("clicker")
clicker_stub.assert_image_visible = lambda *args, **kwargs: True
clicker_stub.click_image = lambda *args, **kwargs: True

detector_stub = types.ModuleType("detector")
detector_stub.find_image = lambda *args, **kwargs: None

applications_stub = types.ModuleType("features.applications")
applications_stub.open_anydesk = lambda: None

screenshot_stub = types.ModuleType("screenshot")
screenshot_stub.save_screenshot = lambda *args, **kwargs: None

sys.modules.setdefault("clicker", clicker_stub)
sys.modules.setdefault("detector", detector_stub)
sys.modules.setdefault("features.applications", applications_stub)
sys.modules.setdefault("screenshot", screenshot_stub)

from features import print_ticket


class PrintTicketTests(unittest.TestCase):
    @patch("features.print_ticket.save_screenshot")
    @patch("features.print_ticket.assert_image_visible")
    @patch("features.print_ticket.click_image")
    @patch("features.print_ticket.find_image")
    @patch("features.print_ticket.open_anydesk")
    def test_cancels_invoice_screen_before_printing_ticket(
        self,
        open_anydesk_mock,
        find_image_mock,
        click_image_mock,
        assert_image_visible_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [
            object(),  # cancel_invoice_button
            object(),  # print_ticket after cancel
            object(),  # print_ticket wait confirmation
            None,
            None,
            None,  # finished after print click
            object(),  # finalize_button
            None,
            None,
            None,  # finished after finalize
        ]

        print_ticket.run()

        open_anydesk_mock.assert_called_once_with()
        self.assertEqual(
            click_image_mock.call_args_list,
            [
                call(
                    "cancel_invoice_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
                call(
                    "print_ticket_button.png",
                    timeout=10,
                    use_coordinates=False,
                    use_region=False,
                ),
            ],
        )
        assert_image_visible_mock.assert_any_call(
            "print_ticket_button.png",
            confidence=0.80,
            timeout=10,
        )
        save_screenshot_mock.assert_any_call("invoice_cancelled_back_to_summary")

    @patch("features.print_ticket.save_screenshot")
    @patch("features.print_ticket.click_image")
    @patch("features.print_ticket.find_image")
    @patch("features.print_ticket.open_anydesk")
    def test_print_ticket_wins_over_false_finished_match(
        self,
        open_anydesk_mock,
        find_image_mock,
        click_image_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [
            None,  # cancel invoice
            object(),  # print ticket visible
            object(),  # false finished after print click
        ]

        print_ticket.run()

        open_anydesk_mock.assert_called_once_with()
        click_image_mock.assert_called_once_with(
            "print_ticket_button.png",
            timeout=10,
            use_coordinates=False,
            use_region=False,
        )
        save_screenshot_mock.assert_any_call("print_ticket_clicked")

    @patch("features.print_ticket.save_screenshot")
    @patch("features.print_ticket.click_image")
    @patch("features.print_ticket.find_image")
    @patch("features.print_ticket.open_anydesk")
    def test_accepts_already_finished_start_screen(
        self,
        open_anydesk_mock,
        find_image_mock,
        click_image_mock,
        save_screenshot_mock,
    ):
        find_image_mock.side_effect = [
            None,  # cancel invoice
            None,  # print ticket
            object(),  # start/iniciar/magna finished state
        ]

        print_ticket.run()

        open_anydesk_mock.assert_called_once_with()
        click_image_mock.assert_not_called()
        save_screenshot_mock.assert_called_once_with(
            "print_ticket_already_finished"
        )


if __name__ == "__main__":
    unittest.main()
