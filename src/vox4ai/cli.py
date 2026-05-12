import argparse
import asyncio
import shutil

from tts_plugin_bridge import ConnectorFactory
from vox4ai_skill.api import (
    list_engines,
    synthesize_text,
    play_text,
    test_connection,
)

from vox4ai.config import load as load_config, merge_cli, show as show_config

_EPILOG = """
使用例:
  vox4ai say "こんにちは"                  # テキストを読む（ストリーミング優先）
  vox4ai say "Hello" -e edgetts           # Edge TTS で読む
  vox4ai save "こんにちは" -o output.wav   # WAV ファイルに保存
  vox4ai list                              # 利用可能エンジン一覧
  vox4ai test -e aivisspeech              # 接続テスト
  vox4ai --commands                        # 使用可能なサブコマンド一覧
  vox4ai --doctor                         # 環境診断
  vox4ai --tts-plugin-list                # TTS Engine 一覧
"""

_COMMANDS = {
    "say": "テキストを読み上げる（ストリーミング優先、ffplay/paplay/aplay）",
    "save": "テキストを音声ファイルに保存",
    "list": "利用可能なTTSプラグインを一覧表示",
    "test": "TTSエンジンへの接続をテスト",
    "config": "現在の設定（config.yaml）を表示",
}


def main():
    return asyncio.run(_async_main())


async def _async_main():
    parser = argparse.ArgumentParser(
        description="vox4ai - 音声合成 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_EPILOG,
        add_help=False,
    )
    parser.add_argument(
        "--commands", action="store_true",
        help="利用可能なサブコマンド一覧を表示",
    )
    parser.add_argument(
        "--doctor", action="store_true",
        help="環境の動作確認（依存コマンド・プラグイン）",
    )
    parser.add_argument(
        "--tts-plugin-list", action="store_true",
        help="利用可能なTTS Engine 一覧",
    )
    parser.add_argument("-h", "--help", action="store_true", help="ヘルプを表示")

    known, remaining = parser.parse_known_args()

    if known.help:
        parser.print_help()
        return 0

    if known.commands:
        print("利用可能なサブコマンド:")
        for name, desc in _COMMANDS.items():
            print(f"  {name:8s}  {desc}")
        print()
        print("詳細: vox4ai <コマンド> --help")
        return 0

    if known.doctor:
        return await _doctor()

    if known.tts_plugin_list:
        return await list_engines()

    sub = parser.add_subparsers(dest="command", help="利用可能なコマンド")
    sub.add_parser("list", help="利用可能なTTSプラグインを一覧表示")
    sub.add_parser("config", help="現在の設定表示")

    say_parser = sub.add_parser("say", help="テキストを読み上げる（ストリーミング優先）")
    say_parser.add_argument("text", help="読み上げるテキスト")
    say_parser.add_argument("--engine", "-e", help="TTSエンジン名")
    say_parser.add_argument("--speed", "-s", type=float, default=1.0, help="話速")
    say_parser.add_argument("--volume", "-v", type=float, help="音量")
    say_parser.add_argument("--pitch", "-p", type=float, help="ピッチ補正")
    say_parser.add_argument("--server-url", help="TTSサーバーURL")
    say_parser.add_argument("--style-id", type=int, help="話者スタイルID")
    say_parser.add_argument("--model", help="音声モデル名")

    save_parser = sub.add_parser("save", help="テキストを音声ファイルに保存")
    save_parser.add_argument("text", help="合成するテキスト")
    save_parser.add_argument("--engine", "-e", help="TTSエンジン名")
    save_parser.add_argument("--speed", "-s", type=float, default=1.0, help="話速")
    save_parser.add_argument("--volume", "-v", type=float, help="音量")
    save_parser.add_argument("--pitch", "-p", type=float, help="ピッチ補正")
    save_parser.add_argument("--server-url", help="TTSサーバーURL")
    save_parser.add_argument("--style-id", type=int, help="話者スタイルID")
    save_parser.add_argument("--output", "-o", help="出力ファイルパス（省略時はBase64表示）")
    save_parser.add_argument("--play", action="store_true", help="保存後に再生")

    test_parser = sub.add_parser("test", help="TTS接続をテスト")
    test_parser.add_argument("--engine", "-e", help="TTSエンジン名")
    test_parser.add_argument("--server-url", help="TTSサーバーURL")
    test_parser.add_argument("--style-id", type=int, help="話者スタイルID")

    args = parser.parse_args(remaining)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "config":
        print(show_config())
        return 0

    cfg = load_config()
    if args.command in ("say", "save", "test"):
        merged = merge_cli(cfg, args)

    engine_kwargs = {}
    if merged.get("server_url"):
        engine_kwargs["server_url"] = merged["server_url"]

    engine = merged.get("engine") or None
    model = merged.get("model") or None
    speed = merged.get("speed", 1.0)
    volume = merged.get("volume")
    pitch = merged.get("pitch")
    style_id = merged.get("style_id")

    if args.command == "list":
        return await list_engines()
    elif args.command == "say":
        return await play_text(
            args.text, engine, speed, volume, pitch,
            style_id, model, engine_kwargs,
        )
    elif args.command == "save":
        return await synthesize_text(
            args.text, engine, speed, volume, pitch,
            style_id, getattr(args, "output", None),
            engine_kwargs, False, getattr(args, "play", False),
        )
    elif args.command == "test":
        return await test_connection(
            engine, style_id, engine_kwargs,
        )
    else:
        parser.print_help()
        return 1


async def _doctor():
    print("vox4ai 環境診断")
    print("=" * 40)

    print("\n[再生コマンド]")
    for cmd in ("ffplay", "paplay", "aplay"):
        found = shutil.which(cmd) is not None
        print(f"  {cmd:12s} {'found' if found else 'not found'}")

    print("\n[TTS プラグイン]")
    try:
        engines = ConnectorFactory.list_available()
        if engines:
            for eng in engines:
                print(f"  {eng:15s} registered")
        else:
            print("  (none found)")
    except Exception as e:
        print(f"  error: {e}")

    print("\n[Python パッケージ]")
    for pkg in ("tts-plugin-bridge", "edge-tts", "aiohttp", "pydantic"):
        try:
            __import__(pkg.replace("-", "_"))
            print(f"  {pkg:20s} installed")
        except ImportError:
            print(f"  {pkg:20s} not installed")

    print()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())