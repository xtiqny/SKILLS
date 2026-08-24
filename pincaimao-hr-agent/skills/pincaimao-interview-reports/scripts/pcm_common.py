"""
聘才猫平台通用调用底座 (pcm_common)

封装聘才猫开放平台的两个核心动作：
  1. upload_file(): 上传文件，返回 (cos_key, filename)
  2. chat_bot_messages(): 调用 chat-bot-messages 接口（blocking / streaming）

所有上层 skill 的 scripts/main.py 复用本模块，避免重复实现。
凭证从环境变量读取，绝不硬编码。
仅依赖 Python 标准库（urllib），无第三方依赖。
"""
import json
import os
import urllib.request
import urllib.error
import mimetypes
import uuid

API_BASE = "https://api.pincaimao.com"
CHAT_URL = f"{API_BASE}/agents/v1/chat/chat-bot-messages"
UPLOAD_URL = f"{API_BASE}/agents/v1/files/upload"

DEFAULT_TIMEOUT = 120


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """
    禁止自动跟随 HTTP 重定向。

    默认的 urlopen 会自动跟随重定向，且在跨域重定向时不会剥离 Authorization 头，
    可能导致携带 API key 的请求被发往第三方域（重定向劫持 / 开放重定向攻击）。
    聘才猫正常 API 不应返回重定向；一旦出现重定向，直接报错而非携带凭证跟随。
    """
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(
            req.full_url, code,
            f"请求被重定向至 {newurl}，为防止凭证泄漏已拒绝跟随。",
            headers, fp
        )


# 全局使用禁止重定向的 opener
_OPENER = urllib.request.build_opener(_NoRedirect)


def _urlopen(req, timeout=DEFAULT_TIMEOUT):
    """统一的请求入口：使用禁止重定向的 opener。"""
    return _OPENER.open(req, timeout=timeout)


def _safe_resolve_path(file_path):
    """
    校验并解析用户传入的文件路径，防止路径遍历越权读取。

    规则：
      1. 解析为绝对真实路径（os.path.realpath 会将 ../ 与符号链接拆平）；
      2. 限制在允许的根目录范围内。默认允许根为当前工作目录；
         可通过环境变量 PCM_ALLOWED_FILE_ROOT 指定其它根目录（如需读取工作目录外的文件）；
      3. 必须是真实存在的普通文件（拒绝目录、设备、符号链接指向越界目标等）。

    返回解析后的安全绝对路径，校验不通过则抛出异常。
    """
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("文件路径不能为空")

    # 允许的根目录：默认当前工作目录，可由环境变量覆盖
    allowed_root = os.path.realpath(
        os.environ.get("PCM_ALLOWED_FILE_ROOT", os.getcwd())
    )
    resolved = os.path.realpath(os.path.abspath(file_path))

    # 范围校验：resolved 必须等于 allowed_root 或在其子目录下
    if resolved != allowed_root and not resolved.startswith(allowed_root + os.sep):
        raise PermissionError(
            "文件路径超出允许范围。如需读取其它目录的文件，"
            "请通过环境变量 PCM_ALLOWED_FILE_ROOT 配置允许的根目录。"
        )
    if not os.path.exists(resolved):
        raise FileNotFoundError("指定的文件不存在。")
    if not os.path.isfile(resolved):
        raise ValueError("指定的路径不是普通文件。")
    return resolved


def _get_key(env_name):
    """从环境变量读取统一 API key，缺失则抛出清晰错误。"""
    key = os.environ.get(env_name)
    if not key:
        raise RuntimeError(
            f"缺少环境变量 {env_name}。请在运行环境中配置 API key "
            f"（获取方式见 SKILL.md 中的注册链接）。"
        )
    return key


def upload_file(file_path, env_name):
    """
    上传文件到聘才猫平台。
    返回 (cos_key, filename)。后续接口使用 cos_key，不是 presigned_url。
    上传接口使用统一配置的 API key。
    """
    key = _get_key(env_name)
    safe_path = _safe_resolve_path(file_path)
    filename = os.path.basename(safe_path)
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    with open(safe_path, "rb") as f:
        file_data = f.read()

    # 构造 multipart/form-data
    boundary = f"----PCMBoundary{uuid.uuid4().hex}"

    body = b""
    body += f"--{boundary}\r\n".encode()
    body += (
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
    ).encode()
    body += f"Content-Type: {content_type}\r\n\r\n".encode()
    body += file_data
    body += f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        UPLOAD_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with _urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"文件上传失败（HTTP {e.code}）。请检查 key 与文件是否有效。")

    cos_key = data.get("cos_key")
    if not cos_key:
        raise RuntimeError("上传响应异常：未返回 cos_key。")
    return cos_key, data.get("filename", filename)


def chat_bot_messages(env_name, query, bot_id, inputs=None, conversation_id=None,
                  response_mode="blocking", user=None):
    """
    调用 chat-bot-messages 接口。
    chat-bot-messages 使用统一配置的 API key。

    blocking 模式：返回完整 JSON dict（含 answer / conversation_id）。
    streaming 模式：返回 dict，answer 为拼接后的完整文本，并尽力解析 conversation_id。
    """
    key = _get_key(env_name)
    payload = {
        "bot_id": bot_id,
        "query": query,
        "inputs": inputs or {},
        "response_mode": response_mode,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id
    if user:
        payload["user"] = user

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if response_mode == "streaming":
        headers["Accept"] = "text/event-stream"

    req = urllib.request.Request(
        CHAT_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with _urlopen(req) as resp:
            if response_mode == "streaming":
                return _parse_sse(resp)
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        # 仅消费响应体以释放连接，不回显服务器返回内容
        try:
            e.read()
        except Exception:
            pass
        if e.code == 401:
            raise RuntimeError(
                f"鉴权失败（401）。请检查环境变量 {env_name} 是否正确，"
                f"且该 API key 有权访问 chat-bot-messages。"
            )
        raise RuntimeError(f"chat-bot-messages 调用失败（HTTP {e.code}）。")


def _parse_sse(resp):
    """解析 SSE 流式响应，拼接 answer，提取 conversation_id 与任务结束标志。"""
    answer = ""
    conversation_id = None
    finished = False
    for raw_line in resp:
        line = raw_line.decode("utf-8", "ignore").strip()
        if not line.startswith("data: "):
            continue
        try:
            d = json.loads(line[6:])
        except json.JSONDecodeError:
            continue
        event = d.get("event", "")
        if d.get("conversation_id") and not conversation_id:
            conversation_id = d["conversation_id"]
        if event in ("message", "agent_message"):
            answer += d.get("answer", "")
        elif event == "node_finished":
            title = (d.get("data") or {}).get("title", "") or ""
            if "聘才猫任务结束" in title:
                finished = True
        elif event == "message_end":
            break
    return {
        "answer": answer,
        "conversation_id": conversation_id,
        "finished": finished,
        "event": "message",
    }


def get_answer(resp):
    """从 blocking/streaming 响应统一取出 answer 文本。"""
    return resp.get("answer", "")


def emit(obj):
    """统一以 JSON 输出到 stdout（ensure_ascii=False 保留中文）。"""
    print(json.dumps(obj, ensure_ascii=False, indent=2))
