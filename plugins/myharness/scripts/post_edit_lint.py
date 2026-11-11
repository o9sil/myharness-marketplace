"""파일을 고친 뒤 프로젝트의 아키텍처 린터를 돌리는 PostToolUse Hook.

린트 규칙은 프로젝트마다 다르므로 플러그인에 넣지 않는다.
프로젝트에 scripts/arch_lint.py 가 있으면 그것을 실행하고, 없으면 아무것도 하지 않는다.

arch_lint.py 약속
  - 위반이 없으면 exit 0
  - 위반이 있으면 0 이 아닌 코드로 끝나고, 수정 지침을 stderr 에 쓴다.
이 Hook 은 그 stderr 를 그대로 전달하고 exit 2 로 끝나 에이전트가 고치게 한다.
"""
import os
import subprocess
import sys
from pathlib import Path

LINT = Path("scripts") / "arch_lint.py"


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    lint = project / LINT
    if not lint.is_file():
        return 0
    result = subprocess.run(
        [sys.executable, str(lint)],
        cwd=project,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout or f"[arch_lint] exit {result.returncode}\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
