import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pos_log_collector


class PosLogCollectorTests(unittest.TestCase):
    def test_copies_latest_pos_log_to_latest_run_folder(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            temp_path = Path(temp_directory)
            source_dir = temp_path / "pos_build_petro"
            older_run = temp_path / "Evidencias" / "run_20260623_190243"
            latest_run = temp_path / "Evidencias" / "run_20260624_190257"
            source_dir.mkdir()
            older_run.mkdir(parents=True)
            latest_run.mkdir(parents=True)

            older_log = source_dir / "api_log_2026-06-23.txt"
            latest_log = source_dir / "api_log_2026-06-24.txt"
            older_log.write_text("older", encoding="utf-8")
            latest_log.write_text("latest", encoding="utf-8")
            os.utime(older_run, (1, 1))
            os.utime(latest_run, (2, 2))
            os.utime(older_log, (1, 1))
            os.utime(latest_log, (2, 2))

            with patch.object(
                pos_log_collector,
                "EVIDENCE_ROOT",
                temp_path / "Evidencias",
            ):
                copied_path = pos_log_collector.copy_latest_pos_log_to_run_folder(
                    source_dir=source_dir
                )

            self.assertEqual(copied_path, latest_run / latest_log.name)
            self.assertEqual(copied_path.read_text(encoding="utf-8"), "latest")

    def test_rejects_log_when_it_does_not_match_run_date(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            temp_path = Path(temp_directory)
            source_dir = temp_path / "pos_build_petro"
            run_folder = temp_path / "Evidencias" / "run_20260625_155518"
            source_dir.mkdir()
            run_folder.mkdir(parents=True)

            wrong_date_log = source_dir / "api_log_2026-06-24.txt"
            wrong_date_log.write_text("wrong date", encoding="utf-8")

            copied_path = pos_log_collector.copy_latest_pos_log_to_run_folder(
                source_dir=source_dir,
                run_folder=run_folder,
            )

            self.assertIsNone(copied_path)

    def test_missing_source_log_returns_none(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            source_dir = Path(temp_directory) / "pos_build_petro"
            run_folder = Path(temp_directory) / "Evidencias" / "run_1"
            source_dir.mkdir()
            run_folder.mkdir(parents=True)

            copied_path = pos_log_collector.copy_latest_pos_log_to_run_folder(
                source_dir=source_dir,
                run_folder=run_folder,
            )

        self.assertIsNone(copied_path)

    def test_after_run_is_enabled_by_env_flag_or_source_dir(self):
        with patch.dict(pos_log_collector.os.environ, {}, clear=True):
            self.assertFalse(pos_log_collector.is_pos_log_after_run_enabled())

        with patch.dict(
            pos_log_collector.os.environ,
            {pos_log_collector.POS_LOG_AFTER_RUN_ENV: "1"},
            clear=True,
        ):
            self.assertTrue(pos_log_collector.is_pos_log_after_run_enabled())

        with patch.dict(
            pos_log_collector.os.environ,
            {pos_log_collector.POS_LOG_SOURCE_DIR_ENV: "/tmp/pos_build_petro"},
            clear=True,
        ):
            self.assertTrue(pos_log_collector.is_pos_log_after_run_enabled())

    def test_rejects_unverified_source_folder_by_default(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            source_dir = Path(temp_directory) / "Downloads"
            run_folder = Path(temp_directory) / "Evidencias" / "run_1"
            source_dir.mkdir()
            run_folder.mkdir(parents=True)
            (source_dir / "api_log_2026-06-24.txt").write_text(
                "wrong source",
                encoding="utf-8",
            )

            copied_path = pos_log_collector.copy_latest_pos_log_to_run_folder(
                source_dir=source_dir,
                run_folder=run_folder,
            )

        self.assertIsNone(copied_path)

    def test_accepts_rustdesk_drop_folder_and_expected_run_date(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            temp_path = Path(temp_directory)
            source_dir = temp_path / "api_log_drop"
            run_folder = temp_path / "Evidencias" / "run_20260721_090000"
            source_dir.mkdir()
            run_folder.mkdir(parents=True)
            expected_log = source_dir / "api_log_2026-07-21.txt"
            expected_log.write_text("rustdesk log", encoding="utf-8")

            copied_path = pos_log_collector.copy_latest_pos_log_to_run_folder(
                source_dir=source_dir,
                run_folder=run_folder,
            )

            self.assertEqual(copied_path, run_folder / expected_log.name)
            self.assertEqual(copied_path.read_text(encoding="utf-8"), "rustdesk log")

    def test_allows_unverified_source_only_with_override(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            source_dir = Path(temp_directory) / "Downloads"
            run_folder = Path(temp_directory) / "Evidencias" / "run_1"
            source_dir.mkdir()
            run_folder.mkdir(parents=True)
            log_path = source_dir / "api_log_2026-06-24.txt"
            log_path.write_text("manual override", encoding="utf-8")

            with patch.dict(
                pos_log_collector.os.environ,
                {pos_log_collector.POS_LOG_ALLOW_UNVERIFIED_SOURCE_ENV: "1"},
                clear=True,
            ):
                copied_path = pos_log_collector.copy_latest_pos_log_to_run_folder(
                    source_dir=source_dir,
                    run_folder=run_folder,
                )

            self.assertEqual(copied_path, run_folder / log_path.name)
            self.assertEqual(
                copied_path.read_text(encoding="utf-8"),
                "manual override",
            )


if __name__ == "__main__":
    unittest.main()
