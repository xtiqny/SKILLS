#!/usr/bin/env python3
"""聘才猫 - 平台基础能力 skill 真实现。

提供平台通用接口的命令行调用（文件上传、临时链接、会话列表、历史消息、音视频转文字）。
这些接口统一读取 PCM_API_KEY，也可用 --env 指定其他环境变量名。

用法:
  python3 main.py upload --file /path/to/file.pdf
  python3 main.py presigned --cos-key "/resources/file/xxx/abc.jpg" [--expired 600]
  python3 main.py conversations [--user user_001] [--limit 20] [--last-id <id>]
  python3 main.py messages --conversation-id <id> [--limit 20] [--first-id <id>]
  python3 main.py audio2text --cos-key "/resources/file/xxx/audio.mp3"
"""
import sys
import os
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

API_BASE = pcm.API_BASE


def _get(path, env, params=None):
    key = pcm._get_key(env)
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"}, method="GET")
    try:
        with pcm._urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            e.read()
        except Exception:
            pass
        raise RuntimeError(f"接口请求失败（HTTP {e.code}）。")


def _post_json(path, env, body):
    key = pcm._get_key(env)
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with pcm._urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            e.read()
        except Exception:
            pass
        raise RuntimeError(f"接口请求失败（HTTP {e.code}）。")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--env", default="PCM_API_KEY",
                   help="使用的环境变量名，默认 PCM_API_KEY")
    sub = p.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("upload"); u.add_argument("--file", required=True)
    pre = sub.add_parser("presigned"); pre.add_argument("--cos-key", required=True); pre.add_argument("--expired", type=int)
    c = sub.add_parser("conversations"); c.add_argument("--user"); c.add_argument("--limit", type=int, default=20); c.add_argument("--last-id")
    m = sub.add_parser("messages"); m.add_argument("--conversation-id", required=True); m.add_argument("--limit", type=int, default=20); m.add_argument("--first-id")
    a = sub.add_parser("audio2text"); a.add_argument("--cos-key", required=True)

    args = p.parse_args()

    if args.cmd == "upload":
        cos_key, filename = pcm.upload_file(args.file, args.env)
        pcm.emit({"cos_key": cos_key, "filename": filename})
    elif args.cmd == "presigned":
        params = {"cos_key": args.cos_key, "expired": args.expired}
        pcm.emit(_get("/agents/v1/files/presigned-url", args.env, params))
    elif args.cmd == "conversations":
        params = {"user": args.user, "limit": args.limit, "last_id": args.last_id}
        pcm.emit(_get("/agents/v1/chat/conversations", args.env, params))
    elif args.cmd == "messages":
        params = {"conversation_id": args.conversation_id, "limit": args.limit, "first_id": args.first_id}
        pcm.emit(_get("/agents/v1/chat/messages", args.env, params))
    elif args.cmd == "audio2text":
        pcm.emit(_post_json("/agents/v1/tts/audio_to_text", args.env, {"cos_key": args.cos_key}))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)})
        sys.exit(1)
