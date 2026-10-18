import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from core import schedule


class ScheduleCacheTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.assets = Path(self.directory.name)
        self.cache_file = self.assets / "schedule_cache.json"
        for name, value in (("ASSETS_DIR", self.assets), ("CACHE_FILE", self.cache_file)):
            patcher = patch.object(schedule, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.data = {"leagueSchedule": {"gameDates": []}}

    def write_cache(self, age=timedelta()):
        self.cache_file.write_text(json.dumps({
            "last_update": (datetime.utcnow() - age).isoformat(),
            "data": self.data,
        }), encoding="utf-8")

    def test_valid_cache_does_not_use_network(self):
        self.write_cache()
        with patch.object(schedule.requests, "get") as get:
            self.assertEqual(schedule.fetch_schedule(), self.data)
        get.assert_not_called()

    def test_invalid_cache_is_refreshed(self):
        for content in ('{"data":', '{}', '[]', '{"last_update": null}'):
            with self.subTest(content=content):
                self.cache_file.write_text(content, encoding="utf-8")
                response = Mock()
                response.json.return_value = self.data
                with patch.object(schedule.requests, "get", return_value=response):
                    self.assertEqual(schedule.fetch_schedule(), self.data)
                self.assertEqual(json.loads(self.cache_file.read_text())["data"], self.data)

    def test_expired_cache_is_used_when_offline(self):
        self.write_cache(age=timedelta(days=1))
        with patch.object(schedule.requests, "get", side_effect=requests.ConnectionError):
            self.assertEqual(schedule.fetch_schedule(), self.data)

    def test_invalid_or_missing_cache_when_offline_has_clear_error(self):
        for content in (None, '{"data":'):
            with self.subTest(content=content):
                if content is not None:
                    self.cache_file.write_text(content, encoding="utf-8")
                with patch.object(schedule.requests, "get", side_effect=requests.ConnectionError):
                    with self.assertRaises(schedule.ConnectionFailedError):
                        schedule.fetch_schedule()

    def test_interrupted_write_preserves_previous_cache(self):
        self.write_cache()
        original = self.cache_file.read_bytes()

        def interrupted_dump(data, stream, **kwargs):
            stream.write('{"data":')
            raise OSError("Interrupted write")

        with patch.object(schedule.json, "dump", side_effect=interrupted_dump):
            with self.assertRaises(OSError):
                schedule._save_cache(self.data)
        self.assertEqual(self.cache_file.read_bytes(), original)
        self.assertEqual(list(self.assets.iterdir()), [self.cache_file])


class StartupTests(unittest.TestCase):
    def test_unavailable_schedule_displays_error_without_traceback(self):
        code = """
import runpy
import sys
from unittest.mock import patch
from core.schedule import ConnectionFailedError
sys.argv = ['main.py', 'today']
with patch('core.schedule.fetch_schedule', side_effect=ConnectionFailedError('Données indisponibles')):
    runpy.run_module('main', run_name='__main__')
"""
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Données indisponibles", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_help_starts_without_loading_schedule_or_network(self):
        # A fresh process also exercises imports, where the original crash occurred.
        code = """
from unittest.mock import patch
from typer.testing import CliRunner
with patch('core.schedule.fetch_schedule', side_effect=AssertionError('Schedule loaded during startup')):
    from main import app
    for args in (['--help'], ['help'], ['team', '--help']):
        result = CliRunner().invoke(app, args)
        assert result.exit_code == 0, (result.output, result.exception)
"""
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
