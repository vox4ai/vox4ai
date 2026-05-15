"""Tests for vox4ai.cli — CLI entry points (--commands, --doctor, config subcommand)."""

import sys
from unittest.mock import patch

import pytest

from vox4ai.cli import main


@pytest.fixture(autouse=True)
def reset_argv():
    original = sys.argv[:]
    yield
    sys.argv[:] = original


class TestCommandsFlag:
    @patch("vox4ai.cli.ConnectorFactory.list_available")
    def test_prints_all_subcommands_and_engines(self, mock_list, capsys):
        mock_list.return_value = ["edgetts", "aivisspeech"]
        sys.argv = ["vox4ai", "--commands"]
        assert main() == 0
        captured = capsys.readouterr()
        for cmd in ("say", "save", "list", "test", "config"):
            assert cmd in captured.out
        assert "edgetts" in captured.out
        assert "aivisspeech" in captured.out

    @patch("vox4ai.cli.ConnectorFactory.list_available")
    def test_commands_no_engines(self, mock_list, capsys):
        mock_list.return_value = []
        sys.argv = ["vox4ai", "--commands"]
        assert main() == 0
        captured = capsys.readouterr()
        assert "none found" in captured.out


class TestHelpFlag:
    def test_help_flag_returns_zero(self, capsys):
        sys.argv = ["vox4ai", "-h"]
        assert main() == 0
        captured = capsys.readouterr()
        assert "vox4ai" in captured.out


class TestEmptyCommand:
    def test_no_subcommand_returns_one(self, capsys):
        sys.argv = ["vox4ai"]
        assert main() == 1


class TestDoctor:
    @patch("vox4ai.cli.shutil.which")
    @patch("vox4ai.cli.ConnectorFactory.list_available")
    def test_doctor_ok(self, mock_list, mock_which):
        mock_which.side_effect = lambda cmd: (
            f"/usr/bin/{cmd}" if cmd in ("ffplay", "paplay", "aplay") else None
        )
        mock_list.return_value = ["edgetts"]
        sys.argv = ["vox4ai", "--doctor"]
        assert main() == 0

    @patch("vox4ai.cli.shutil.which")
    @patch("vox4ai.cli.ConnectorFactory.list_available")
    def test_doctor_no_plugins(self, mock_list, mock_which):
        mock_which.return_value = None
        mock_list.return_value = []
        sys.argv = ["vox4ai", "--doctor"]
        assert main() == 0


class TestConfigSubcommand:
    def test_config_shows_settings(self, capsys, tmp_path, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config_dir = tmp_path / "vox4ai"
        config_dir.mkdir()
        (config_dir / "config.yaml").write_text("engine: edgetts\n")

        sys.argv = ["vox4ai", "config"]
        assert main() == 0
        captured = capsys.readouterr()
        assert "engine: edgetts" in captured.out

    def test_config_no_file(self, capsys, tmp_path, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        sys.argv = ["vox4ai", "config"]
        assert main() == 0
        captured = capsys.readouterr()
        assert "no config file" in captured.out


class TestTTSPluginList:
    @patch("vox4ai.cli.list_engines")
    def test_calls_list_engines(self, mock_list):
        mock_list.return_value = 0
        sys.argv = ["vox4ai", "--tts-plugin-list"]
        assert main() == 0
        mock_list.assert_called_once()
