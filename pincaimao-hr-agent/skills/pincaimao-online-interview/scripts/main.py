#!/usr/bin/env python3
"""聘才猫 - 在线面试 skill 真实现（多轮对话，企业招聘用）。
question_number 为字符串；无 interview_role / reference_answer。
第一轮不传 conversation_id；后续轮次必须带同一 conversation_id。
可选 url_callback：报告生成后回调。
用法:
  首轮:  python3 main.py start --job-info "<JD>" [--resume <file>] [--job-title <名>] [--num 5] [--callback <url>]
  后续:  python3 main.py reply --conversation-id <id> --answer "<回答或视频转写文字>"
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 3022316191018907

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)

    s = sub.add_parser("start")
    s.add_argument("--job-info", required=True)
    s.add_argument("--resume", default="")
    s.add_argument("--job-title", default="")
    s.add_argument("--num", default="5")        # 字符串
    s.add_argument("--callback", default="")

    r = sub.add_parser("reply")
    r.add_argument("--conversation-id", required=True)
    r.add_argument("--answer", required=True)

    args = p.parse_args()

    if args.mode == "start":
        inputs = {"job_info": args.job_info, "question_number": str(args.num)}
        if args.job_title:
            inputs["job_title"] = args.job_title
        if args.callback:
            inputs["url_callback"] = args.callback
        if args.resume:
            cos_key, filename = pcm.upload_file(args.resume, ENV)
            inputs["file_url"] = cos_key
            inputs["file_name"] = filename
        resp = pcm.chat_bot_messages(ENV, args.job_info[:20],
                                     bot_id=BOT_ID, inputs=inputs)
        pcm.emit({"answer": pcm.get_answer(resp),
                  "conversation_id": resp.get("conversation_id")})
    else:
        resp = pcm.chat_bot_messages(ENV, args.answer, bot_id=BOT_ID, inputs={},
                                 conversation_id=args.conversation_id)
        pcm.emit({"answer": pcm.get_answer(resp),
                  "conversation_id": resp.get("conversation_id") or args.conversation_id})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
