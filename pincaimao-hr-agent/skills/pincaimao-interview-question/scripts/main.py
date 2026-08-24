#!/usr/bin/env python3
"""聘才猫 - 面试出题大师 skill 真实现。
流程: 上传简历 -> cos_key -> chat-bot-messages
question_number 为数字(默认6)；can_outputAnalysis 为字符串 "true"/"false"(默认"false")
query = job_info 前20字符
用法:
  python3 main.py --resume /path/to/resume.docx --job-info "<JD全文>" [--job-title "<职位名>"] [--num 6] [--analysis false]
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 3022316191018876

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--resume", required=True)
    p.add_argument("--job-info", required=True)
    p.add_argument("--job-title", default="")
    p.add_argument("--num", type=int, default=6)
    p.add_argument("--analysis", choices=["true", "false"], default="false")
    args = p.parse_args()

    cos_key, _ = pcm.upload_file(args.resume, ENV)
    inputs = {
        "job_info": args.job_info,
        "file_url": cos_key,
        "question_number": args.num,            # 数字
        "can_outputAnalysis": args.analysis,    # 字符串
    }
    if args.job_title:
        inputs["job_title"] = args.job_title
    resp = pcm.chat_bot_messages(ENV, args.job_info[:20],
                                 bot_id=BOT_ID, inputs=inputs)
    pcm.emit({"answer": pcm.get_answer(resp)})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
