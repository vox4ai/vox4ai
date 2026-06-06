# vox4ai

<p align="center">
  <img src="https://via.placeholder.com/1200x400/1a1a1a/ffffff?text=vox4ai" alt="vox4ai Banner" width="1200">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/pypi-latest-blue.svg" alt="PyPI version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.10%2B-yellow.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/maintained%3F-yes-brightgreen.svg" alt="Maintained">
</p>

<p align="center">
  <a href="https://github.com/vox4ai/vox4ai">Website</a> •
  <a href="https://github.com/vox4ai/vox4ai/issues">Report Bug</a> •
  <a href="https://github.com/vox4ai/vox4ai/contributing">Contributing</a>
</p>

---

## 🚀 Overview

TTS 音声合成 CLI。`tts-plugin-bridge` のプラグインシステムに対応した TTS Engine を
統一的に操作できます。`vox` と `vox4ai` 両方のコマンド名でインストールされます。

## 📦 Installation

```bash
uv add vox4ai
```

インストールするだけで `tts-plugin-bridge` + `tts-plugin-edgetts`（クラウドデフォルト）が
入り、追加のローカルサーバーなしで音声合成を試せます。

他の TTS エンジンを追加する場合：

```bash
uv add tts-plugin-aivisspeech   # AivisSpeech Engine
uv add tts-plugin-piperplus     # Piper Plus (HTTP server)
uv add tts-plugin-voisonatalk   # VoiSona Talk
uv add tts-plugin-kokoro        # Kokoro (local)
```

## 🛠 Usage

`vox` と `vox4ai` は同義。短い `vox` を推奨。

```bash
# テキストを読み上げる（デフォルト: edgetts）
vox "こんにちは"

# 音声ファイルに保存
vox save "こんにちは" -o output.wav

# engine を明示指定
vox "こんにちは" -e aivisspeech --style-id 888753760

# 利用可能な TTS エンジン一覧
vox list

# 接続テスト
vox test -e aivisspeech --server-url http://localhost:10101

# 環境診断
vox --doctor

# 現在の設定
vox config

# サブコマンド一覧
vox --commands
```

## ⚙️ Configuration

`vox4ai say "こんにちは"` のように engine を省略しても、設定ファイルからデフォルト値を読み込みます。

**場所**: `~/.config/vox4ai/config.yaml`（XDG_CONFIG_HOME 準拠）

**設定例**:

```yaml
# デフォルトの TTS Engine
engine: edgetts

# デフォルトの音声モデル
model: ja-JP-NanamiNeural

# TTS サーバーURL（aivisspeech などで必要）
server_url: http://localhost:10101

# デフォルトの話速（0.5 〜 2.0、デフォルト 1.0）
speed: 1.2

# 話者スタイル ID（aivisspeech など）
style_id: 888753760
```

**優先順位**: `CLI 引数 > config.yaml > デフォルト値`

## ⌨️ Subcommands

| Command | Description |
|---------|-------------|
| `say` | テキストを読み上げる（ffplay ストリーミング優先 → paplay/aplay） |
| `save` | テキストを音声ファイルに保存 |
| `list` | 利用可能なTTSプラグインを一覧表示 |
| `test` | TTSエンジンへの接続テスト |
| `config` | 現在の設定 (config.yaml) を表示 |

## 📦 Dependencies

- `tts-plugin-bridge` — コアフレームワーク
- `tts-plugin-edgetts` — Microsoft Edge TTS（クラウド、デフォルト）
- `vox4ai-skill-lib` — 内部ライブラリ
- 任意の TTS プラグイン (`tts-plugin-aivisspeech`, `tts-plugin-piperplus` など)

## 📜 License

MIT License