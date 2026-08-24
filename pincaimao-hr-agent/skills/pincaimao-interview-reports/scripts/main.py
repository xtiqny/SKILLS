#!/usr/bin/env python3
"""聘才猫 - 面试报告 skill 真实现。
注意差异: 文件字段名为 file_urls(复数)；query 传文件名(非 job_info 前20字符)
流程: 上传面试记录文件 -> cos_key + filename -> chat-bot-messages
用法:
  python3 main.py --file /path/to/interview_record.docx --job-info "<JD全文>"
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 3022316191018877

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    p.add_argument("--job-info", required=True)
    args = p.parse_args()

    cos_key, filename = pcm.upload_file(args.file, ENV)
    inputs = {"job_info": args.job_info, "file_urls": cos_key}  # 复数 file_urls
    resp = pcm.chat_bot_messages(ENV, filename, bot_id=BOT_ID,
                                 inputs=inputs)  # query = 文件名
    pcm.emit({"answer": pcm.get_answer(resp)})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
