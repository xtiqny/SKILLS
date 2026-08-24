#!/usr/bin/env python3
"""聘才猫 - 简历诊断 skill 真实现。
流程: 上传简历 -> cos_key -> chat-bot-messages(job_info + file_url + query=job_info前20字符)
用法:
  python3 main.py --resume /path/to/resume.pdf --job-info "<JD全文>" [--job-title "<职位名>"]
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 3022316191018881

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--resume", required=True)
    p.add_argument("--job-info", required=True)
    p.add_argument("--job-title", default="")
    args = p.parse_args()

    cos_key, _ = pcm.upload_file(args.resume, ENV)
    inputs = {"job_info": args.job_info, "file_url": cos_key}
    if args.job_title:
        inputs["job_title"] = args.job_title
    query = args.job_info[:20]
    resp = pcm.chat_bot_messages(ENV, query, bot_id=BOT_ID, inputs=inputs)
    pcm.emit({"answer": pcm.get_answer(resp)})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
