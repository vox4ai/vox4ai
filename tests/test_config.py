"""Tests for vox4ai.config — config loading, YAML parsing, CLI merge."""

import argparse
from pathlib import Path

import pytest

from vox4ai.config import defaults, load, merge_cli, show


class TestDefaults:
    def test_all_keys_present(self):
        d = defaults()
        assert set(d) == {
            "engine",
            "model",
            "server_url",
            "style_id",
            "speed",
            "volume",
            "pitch",
        }

    def test_default_values(self):
        d = defaults()
        assert d["engine"] == ""
        assert d["speed"] == 1.0
        assert d["model"] == ""
        assert d["server_url"] == ""
        assert d["style_id"] is None
        assert d["volume"] is None
        assert d["pitch"] is None

    def test_defaults_returns_copy(self):
        d1 = defaults()
        d2 = defaults()
        assert d1 is not d2


class TestLoad:
    def test_no_file_returns_defaults(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        cfg = load()
        assert cfg["engine"] == ""
        assert cfg["speed"] == 1.0

    def test_load_from_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config_dir = tmp_path / "vox4ai"
        config_dir.mkdir()
        (config_dir / "config.yaml").write_text("engine: edgetts\nspeed: 1.5\n")

        cfg = load()
        assert cfg["engine"] == "edgetts"
        assert cfg["speed"] == 1.5
        assert cfg["model"] == ""

    def test_load_partial_config(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config_dir = tmp_path / "vox4ai"
        config_dir.mkdir()
        (config_dir / "config.yaml").write_text("engine: piperplus\n")

        cfg = load()
        assert cfg["engine"] == "piperplus"
        assert cfg["speed"] == 1.0  # should keep default

    def test_load_malformed_yaml(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config_dir = tmp_path / "vox4ai"
        config_dir.mkdir()
        (config_dir / "config.yaml").write_text("{{invalid: yaml::\nbroken")

        # Should not raise
        cfg = load()
        # malformed YAML silently returns defaults via bare except
        assert cfg == defaults()


class TestMergeCLI:
    @staticmethod
    def _make_args(**overrides) -> argparse.Namespace:
        base = dict.fromkeys(
            ["engine", "model", "server_url", "style_id", "speed", "volume", "pitch"]
        )
        base.update(overrides)
        return argparse.Namespace(**base)

    def test_cli_overrides_config(self):
        cfg = {
            "engine": "aivisspeech",
            "speed": 1.0,
            "model": "",
            "server_url": "",
            "style_id": None,
            "volume": None,
            "pitch": None,
        }
        args = self._make_args(engine="edgetts")
        merged = merge_cli(cfg, args)
        assert merged["engine"] == "edgetts"

    def test_cli_speed_overrides(self):
        cfg = {
            "engine": "",
            "speed": 1.0,
            "model": "",
            "server_url": "",
            "style_id": None,
            "volume": None,
            "pitch": None,
        }
        args = self._make_args(speed=2.0)
        merged = merge_cli(cfg, args)
        assert merged["speed"] == 2.0

    def test_cli_preserves_config_when_unset(self):
        cfg = {
            "engine": "aivisspeech",
            "speed": 1.0,
            "model": "",
            "server_url": "",
            "style_id": None,
            "volume": None,
            "pitch": None,
        }
        args = self._make_args()
        merged = merge_cli(cfg, args)
        assert merged["engine"] == "aivisspeech"
        assert merged["speed"] == 1.0

    def test_string_does_not_override(self):
        cfg = {
            "engine": "aivisspeech",
            "speed": 1.0,
            "model": "",
            "server_url": "",
            "style_id": None,
            "volume": None,
            "pitch": None,
        }
        args = self._make_args(engine="")
        merged = merge_cli(cfg, args)
        assert merged["engine"] == "aivisspeech"

    def test_none_does_not_override(self):
        cfg = {
            "engine": "aivisspeech",
            "speed": 1.0,
            "model": "",
            "server_url": "",
            "style_id": None,
            "volume": None,
            "pitch": None,
        }
        args = self._make_args(engine=None)
        merged = merge_cli(cfg, args)
        assert merged["engine"] == "aivisspeech"

    def test_merge_returns_copy(self):
        cfg = {
            "engine": "aivisspeech",
            "speed": 1.0,
            "model": "",
            "server_url": "",
            "style_id": None,
            "volume": None,
            "pitch": None,
        }
        args = self._make_args()
        merged = merge_cli(cfg, args)
        assert merged is not cfg


class TestShow:
    def test_no_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        assert show() == "(no config file)"

    def test_with_content(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config_dir = tmp_path / "vox4ai"
        config_dir.mkdir()
        (config_dir / "config.yaml").write_text("engine: edgetts\n")
        assert show() == "engine: edgetts"

    def test_empty_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config_dir = tmp_path / "vox4ai"
        config_dir.mkdir()
        (config_dir / "config.yaml").write_text("")
        assert show() == "(empty)"
