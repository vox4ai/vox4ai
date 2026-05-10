# vox4ai

TTS 音声合成 CLI。`tts-plugin-bridge` のプラグインシステムに対応した TTS Engine を
統一的に操作できます。

## インストール

```bash
uv add vox4ai
```

## 使い方

```bash
# テキストを読み上げる（ストリーミング優先）
vox4ai say "こんにちは" -e edgetts

# 音声ファイルに保存
vox4ai save "こんにちは" -o output.wav

# 利用可能なTTS Engine 一覧
vox4ai list

# 接続テスト
vox4ai test -e aivisspeech --server-url http://localhost:10101 --style-id 888753760

# 環境診断
vox4ai --doctor

# サブコマンド一覧
vox4ai --commands
```

## サブコマンド

| コマンド | 説明 |
|----------|------|
| `say` | テキストを読み上げる（ffplay ストリーミング優先 → paplay/aplay） |
| `save` | テキストを音声ファイルに保存 |
| `list` | 利用可能なTTSプラグインを一覧表示 |
| `test` | TTSエンジンへの接続をテスト |

## 依存

- `tts-plugin-bridge` — コアフレームワーク
- 任意の TTS プラグイン（`tts-plugin-edgetts`, `tts-plugin-aivisspeech` など）

## ライセンス

MIT License