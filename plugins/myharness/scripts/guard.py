"""위험한 명령을 실행 전에 막는 PreToolUse Hook.

막는 것
  - rm -rf, PowerShell Remove-Item -Recurse -Force, rmdir /s
  - git push --force / -f

Bash와 PowerShell 도구 모두에 건다(matcher "Bash|PowerShell").
Hook 입력(JSON, stdin)의 tool_input.command 를 검사하고,
막을 때는 exit 2 와 함께 이유를 stderr 로 돌려준다.
패키지 관리자 규칙(예: pip 금지, uv만 사용)처럼 프로젝트마다 다른 규칙은
여기 넣지 않고 각 프로젝트의 CLAUDE.md 나 .claude/settings.json 에 둔다.
"""
import json
import re
import sys

RULES = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r",
     "rm -rf 는 막혀 있습니다. 지울 파일을 사람에게 확인받으세요."),
    (r"(?i)\bRemove-Item\b(?=.*-Recurse)(?=.*-Force)|\brmdir\s+/s\b",
     "재귀 강제 삭제는 막혀 있습니다. 지울 파일을 사람에게 확인받으세요."),
    (r"\bgit\s+push\b.*(--force\b|\s-f\b)",
     "git push --force 는 막혀 있습니다. 일반 push 를 쓰세요."),
]


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    command = (data.get("tool_input") or {}).get("command", "")
    for pattern, reason in RULES:
        if re.search(pattern, command):
            print(f"[guard] 차단: {command}\n이유: {reason}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
