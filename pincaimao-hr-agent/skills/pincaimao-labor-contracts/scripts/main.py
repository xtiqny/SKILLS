#!/usr/bin/env python3
"""聘才猫 - 劳动合同卫士 skill 真实现。
合同来源二选一: 文件(上传得 cos_key 传 file_url) 或 文本(传 input)。
另一个字段传空字符串。query 固定 "请对劳动合同进行分析"。
用法:
  文件: python3 main.py --file /path/to/contract.docx
  文本: python3 main.py --text "劳动合同 甲方..."
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcm_common as pcm

ENV = "PCM_API_KEY"
BOT_ID = 3022316191018882

def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--file")
    g.add_argument("--text")
    args = p.parse_args()

    if args.file:
        cos_key, _ = pcm.upload_file(args.file, ENV)
        inputs = {"file_url": cos_key, "input": ""}
    else:
        inputs = {"file_url": "", "input": args.text}
    resp = pcm.chat_bot_messages(ENV, "请对劳动合同进行分析",
                                 bot_id=BOT_ID, inputs=inputs)
    pcm.emit({"answer": pcm.get_answer(resp)})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pcm.emit({"error": str(e)}); sys.exit(1)
