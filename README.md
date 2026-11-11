# myharness-marketplace

practice-m3 하네스에서 프로젝트와 상관없는 부분만 뽑아 만든 로컬 플러그인 마켓플레이스다.

## 설치 (로컬)

```
/plugin marketplace add <이 폴더 경로>
/plugin install myharness@myharness-marketplace
```

## 들어 있는 것 (`plugins/myharness`)

| 종류 | 이름 | 하는 일 |
|---|---|---|
| agent | verifier | spec 기준 검증. 고치지 않고 보고만 한다 |
| agent | cleaner | 죽은 코드 · 중복 · 낡은 TODO · 문서 불일치 정리 |
| skill | round | spec → plan → 구현 → verifier → cleaner → review 라운드 절차와 종료 조건 |
| hook | guard.py (PreToolUse, Bash/PowerShell) | rm -rf, 재귀 강제 삭제, git push --force 차단 |
| hook | protect_env.py (PreToolUse, Read/Grep) | .env 읽기 차단 (`.env.example` 등은 허용) |
| hook | post_edit_lint.py (PostToolUse, Edit/Write) | 프로젝트에 `scripts/arch_lint.py`가 있으면 실행, 위반을 에이전트에게 돌려준다 |

## 프로젝트마다 둘 것 (플러그인에서 뺀 것)

- **CLAUDE.md**: 코드 규칙, 테스트 · 린트 명령, 패키지 관리 규칙(예: uv만 사용). 에이전트와 스킬은 여기에 적힌 명령을 쓴다.
- **scripts/arch_lint.py**: 그 프로젝트의 아키텍처 규칙. 위반 시 0 아닌 코드로 끝나고 수정 지침을 stderr에 쓴다.
- **pip 금지 같은 도구 규칙**: 필요하면 프로젝트 `.claude/settings.json`의 Hook이나 permissions로 둔다.

## 요구 사항

Hook은 `python`(3.8 이상, 표준 라이브러리만)으로 실행한다. PATH에 `python`이 없는 환경(일부 macOS/Linux)이라면
`hooks/hooks.json`의 `python`을 `python3`로 바꾼다.
