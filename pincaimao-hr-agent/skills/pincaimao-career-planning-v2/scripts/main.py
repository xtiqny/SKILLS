#!/usr/bin/env python3
"""聘才猫 - 职业规划助手 V2 skill 真实现。
流程: 上传简历 -> cos_key -> chat-bot-messages(query 固定"分析简历，提出职业建议")
type 三选一: 初入职场 | 转型建议 | 晋升路径
用法:
  python3 main.py --resume /path/to/resume.pdf --type 晋升路径
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 121182005294690304
VALID_TYPES = ["初入职场", "转型建议", "晋升路径"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--resume", required=True)
    p.add_argument("--type", required=True, choices=VALID_TYPES)
    args = p.parse_args()

    cos_key, _ = pcm.upload_file(args.resume, ENV)
    inputs = {"type": args.type, "file_url": cos_key}
    resp = pcm.chat_bot_messages(ENV, "分析简历，提出职业建议",
                                 bot_id=BOT_ID, inputs=inputs)
    pcm.emit({"answer": pcm.get_answer(resp)})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
