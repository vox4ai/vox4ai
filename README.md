# vox4ai

TTS 音声合成 CLI。`tts-plugin-bridge` のプラグインシステムに対応した TTS Engine を
統一的に操作できます。

## インストール

```bash
uv add vox4ai
```

## 使い方

```bash
# テキストを読み上げる（設定ファイルの engine が使われる）
vox4ai say "こんにちは"

# engine を明示指定（CLI 引数は設定より優先）
vox4ai say "こんにちは" -e edgetts

# 音声ファイルに保存
vox4ai save "こんにちは" -o output.wav

# 利用可能なTTS Engine 一覧
vox4ai list

# 接続テスト
vox4ai test -e aivisspeech --server-url http://localhost:10101 --style-id 888753760

# 環境診断
vox4ai --doctor

# 現在の設定を表示
vox4ai config

# サブコマンド一覧
vox4ai --commands
```

## 設定ファイル

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

## サブコマンド

| コマンド | 説明 |
|----------|------|
| `say` | テキストを読み上げる（ffplay ストリーミング優先 → paplay/aplay） |
| `save` | テキストを音声ファイルに保存 |
| `list` | 利用可能なTTSプラグインを一覧表示 |
| `test` | TTSエンジンへの接続をテスト |
| `config` | 現在の設定（config.yaml）を表示 |

## 依存

- `tts-plugin-bridge` — コアフレームワーク
- 任意の TTS プラグイン（`tts-plugin-edgetts`, `tts-plugin-aivisspeech` など）

## ライセンス

MIT License