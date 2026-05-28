# vox4ai

TTS 音声合成 CLI。`tts-plugin-bridge` のプラグインシステムに対応した TTS Engine を統一的に操作できます。

## 🛠 概要
- **役割**: 統一されたインターフェース（CLI）を通じて、様々な TTS プラグインを操作する。
- **主要機能**:
    - `say`, `save`, `list`, `test`, `config` などのサブコマンド。
    - 環境診断機能 (`--doctor`)。
    - 設定ファイル (`~/.config/vox4ai/config.yaml`) によるデフォルト設定の管理。

## 🚀 開発・実行
- **パッケージ管理**: `uv`

## 🔗 関連リポジトリ
- `repos/tts-plugin-bridge`: コアフレームワーク
- 各種 `tts-plugin-*`: 各種TTSエンジンプラグイン
