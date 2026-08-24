#!/usr/bin/env python3
"""聘才猫 - 简历优化 skill 真实现。
流程: 上传简历 -> cos_key -> chat-bot-messages(query 固定"生成简历格式数据")
mode_type 为数字，默认 0。
用法:
  python3 main.py --resume /path/to/resume.pdf --job-info "<JD全文>" [--job-title "<职位名>"] [--mode-type 0]
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 45444431062634496

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--resume", required=True)
    p.add_argument("--job-info", required=True)
    p.add_argument("--job-title", default="")
    p.add_argument("--mode-type", type=int, default=0)
    args = p.parse_args()

    cos_key, _ = pcm.upload_file(args.resume, ENV)
    inputs = {"job_info": args.job_info, "file_url": cos_key, "mode_type": args.mode_type}
    if args.job_title:
        inputs["job_title"] = args.job_title
    resp = pcm.chat_bot_messages(ENV, "生成简历格式数据",
                                 bot_id=BOT_ID, inputs=inputs)
    pcm.emit({"answer": pcm.get_answer(resp)})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
