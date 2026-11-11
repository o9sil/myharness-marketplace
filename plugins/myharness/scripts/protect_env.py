""".env 파일 읽기를 막는 PreToolUse Hook.

원래 하네스의 permissions.deny "Read(./.env)" 를 대신한다.
플러그인은 permissions 를 실을 수 없어서 Hook 으로 막는다.

Read 와 Grep 도구에 건다(matcher "Read|Grep").
tool_input 의 file_path 나 path 가 .env 또는 .env.* 이면 exit 2 로 막는다.
.env.example 처럼 값이 없는 견본 파일은 허용한다.
"""
import json
import re
import sys
from pathlib import PurePath

ENV_FILE = re.compile(r"^\.env(\..+)?$")
ALLOWED = {".env.example", ".env.sample", ".env.template"}


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = data.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("path") or ""
    name = PurePath(target.replace("\\", "/")).name
    if ENV_FILE.match(name) and name not in ALLOWED:
        print(f"[protect_env] 차단: {target}\n이유: .env 파일은 읽지 않습니다. 필요한 값은 사람에게 물어보세요.",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
