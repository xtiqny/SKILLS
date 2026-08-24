#!/usr/bin/env python3
"""聘才猫 - JD 助手 skill 真实现。
两个功能共用 chat-bot-messages：
  1) 生成招聘 JD：inputs.job_info
  2) 生成职位标签：inputs.job_title + function_type(数字1)，answer 需二次 json.loads
用法:
  python3 main.py jd  --job-info "<职位信息>"
  python3 main.py tags --job-title "<职位名称>"
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 3022316191018873

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    a = sub.add_parser("jd"); a.add_argument("--job-info", required=True)
    b = sub.add_parser("tags"); b.add_argument("--job-title", required=True)
    args = p.parse_args()

    if args.mode == "jd":
        resp = pcm.chat_bot_messages(ENV, "请帮我生成这个职位的招聘信息：",
                                 bot_id=BOT_ID, inputs={"job_info": args.job_info})
        pcm.emit({"answer": pcm.get_answer(resp)})
    else:
        resp = pcm.chat_bot_messages(ENV, "请帮我生成职位标签",
                                 bot_id=BOT_ID,
                                 inputs={"job_title": args.job_title, "function_type": 1})
        answer = pcm.get_answer(resp)
        try:
            tags = json.loads(answer)  # answer 是 JSON 字符串，需二次解析
            pcm.emit({"tags": tags})
        except json.JSONDecodeError:
            pcm.emit({"answer": answer})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
