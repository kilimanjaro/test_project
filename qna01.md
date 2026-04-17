# 선택한 질문 목록

## Q1: 모델 변경은 어디서 하나요?

**A:** `/model` 명령어로 변경 가능합니다. 여기(채팅 인터페이스)에서도 가능합니다.

```
/model claude-sonnet-4-6
```

### CLI vs 채팅 인터페이스 역할 분담

| 영역 | CLI (터미널) | 채팅 (여기) |
|------|-------------|----------|
| 모델 선택 | `/model` | `/model` ✓ |
| 키바인딩 설정 | `~/.claude/keybindings.json` 편집 | ✗ |
| 훅(자동화) | `settings.json` 편집 | ✗ |
| 스킬 생성/수정 | CLI 제어 | ✗ |
| **코드 작업** | ✓ | **✓✓✓** |
| **파일 읽기/수정** | ✓ | **✓✓✓** |
| **Git 작업** | ✓ | **✓✓✓** |

**요점**: 환경 설정은 CLI에서, 코드 작업은 채팅 인터페이스에서 진행하는 것이 효율적입니다.

---

## Q2: 표 안의 체크 표시가 한 개인 것과 세 개인 것은 왜 다른가요?

**A:** 체크 표시의 개수는 **기능 추천 강도**를 나타냅니다.

| 표시 | 의미 |
|------|------|
| ✓ | 가능하지만 덜 추천 |
| ✓✓ | 권장 |
| ✓✓✓ | 매우 강력 추천 / 최적의 방식 |

**예시:**
- **코드 작업**: CLI에서도 `cat` / `sed` 명령어로 가능(✓)하지만, 채팅에서 **읽기/수정 도구로 훨씬 편함(✓✓✓)**
- **Git 작업**: CLI에서 `git` 명령어로 가능(✓)하지만, 채팅에서 **비주얼 피드백과 함께 진행 가능(✓✓✓)**

**결론**: 두 환경 모두 가능하지만, 코드 작업에는 여기(채팅)가 압도적으로 더 효율적입니다.

---

## Claude Code 기본 명령어

| 명령어 | 설명 |
|--------|------|
| `/help` | 도움말 |
| `/clear` | 대화 초기화 |
| `/compact` | 대화 압축 |
| `/cost` | 토큰 비용 확인 |
| `/doctor` | 환경 진단 |
| `/fast` | 빠른 모드 토글 |
| `/model` | 모델 변경 |

---

## 수정/삭제, 페이지네이션, 검색 등 을 하기 전에 /memory 기능에 대해서 설명해봐

**답변:**

## `/memory` 기능 설명

### 개요
`/memory`는 Claude Code에서 **Claude가 기억할 내용을 관리**하는 슬래시 커맨드입니다.

---

### 실행하면 보이는 것
```
/memory
```
- 현재 세션에 로드된 **CLAUDE.md 파일 목록** 표시
- **자동 메모리 ON/OFF 토글**
- 메모리 폴더 열기 링크

---

### CLAUDE.md vs 자동 메모리

| 구분 | CLAUDE.md | 자동 메모리 |
|------|-----------|------------|
| 작성자 | **사람** (직접 작성) | **Claude** (자동 저장) |
| 내용 | 코딩 규칙, 프로젝트 구조 | 대화 중 배운 것들 |
| 위치 | 프로젝트 루트 | `~/.claude/projects/.../memory/` |

---

### 이 프로젝트에서의 현황

현재 저는 이 대화에서 `MEMORY.md`를 아직 만들지 않은 상태입니다.  
예를 들어 "항상 pnpm 써", "테스트는 실제 DB로 해" 같은 걸 말하면 → 제가 메모리 파일에 저장해서 **다음 대화에서도 기억**하는 방식입니다.

---

### 실용적 활용

- **프로젝트 규칙 추가**: "앞으로 뷰는 항상 CBV로 작성해" → 메모리에 저장
- **잘못된 기억 삭제**: `/memory` 실행 후 파일 편집
- **현재 지시사항 확인**: 어떤 규칙이 로드됐는지 한눈에 보기

지금 수정/삭제, 페이지네이션, 검색 작업을 시작할까요?

---

## 따로 기능별로 md 파일을 작성하지 않고 memory.md에 저장하면 크기가 너무 커지지 않아? 따로 따로 조각내서 md 파일을 만들어야 하는 거 아니야?

**답변:**

좋은 질문입니다. 정확히 이해하고 계신 겁니다.

## MEMORY.md의 역할

`MEMORY.md`는 **목차(인덱스)** 역할만 합니다. 실제 내용은 저장하지 않아요.

```
memory/
├── MEMORY.md           ← 목차만 (200줄 제한, 항상 로드됨)
├── user_role.md        ← 실제 내용
├── feedback_testing.md ← 실제 내용
├── project_status.md   ← 실제 내용
└── ...
```

## MEMORY.md 내용 예시

```markdown
- [사용자 정보](user_role.md) — Django 백엔드 개발자, Python/Bootstrap 선호
- [작업 피드백](feedback_testing.md) — 테스트는 실제 DB 사용
- [프로젝트 현황](project_status.md) — 게시판 기본 구조 완성
```

## 동작 방식

1. 대화 시작 시 → `MEMORY.md` (목차) 먼저 로드
2. 특정 기억이 필요할 때 → 해당 `.md` 파일만 읽음
3. 불필요한 파일은 로드 안 함 → **컨텍스트 절약**

---

즉, 말씀하신 대로 **파일을 쪼개는 게 맞는 설계**이고, 저도 그렇게 구현되어 있습니다. `MEMORY.md`가 비대해지면 안 되는 구조입니다.

지금 이 프로젝트의 메모리를 정리해서 저장해 드릴까요?

---

## wsl을 사용하면 더 쉽나?

**답변:**

네, WSL이 훨씬 편합니다.

| 항목 | Windows (CMD/PowerShell) | WSL (Ubuntu 등) |
|------|--------------------------|-----------------|
| `python3` | 없음 → `python` 써야 함 | 기본 제공 |
| 인코딩 | cp949 기본 → 매번 `encoding='utf-8'` | UTF-8 기본 |
| 경로 | `C:\Users\...` 백슬래시 이슈 | `/home/...` 유닉스 경로 |
| bash 명령 | 제한적 | 완전 지원 |
| Claude Code 궁합 | 보통 | 좋음 (Linux 기반이라 자연스러움) |

아까 겪은 3가지 에러가 WSL에서는 **전부 발생하지 않았을** 겁니다.

단, WSL을 쓰면 **파일 경로가 달라지는** 점만 주의하면 됩니다.
- Windows 파일: `/mnt/c/Users/901-00/...` 로 접근
- WSL 내부 파일: `/home/<username>/...`

Django 개발도 WSL에서 하면 훨씬 편하게 됩니다.

---

## 장고 웹서버를 띄울 때, 가상환경에서 실행했나? 명령어를 무엇이라고 해서 실행했지?

**답변:**

네, 가상환경에서 실행했습니다. 아까 사용한 명령어는:

```bash
source venv/Scripts/activate && python manage.py runserver
```

- `source venv/Scripts/activate` — Windows 가상환경 활성화 (Mac/Linux는 `venv/bin/activate`)
- `python manage.py runserver` — Django 개발 서버 실행

---

## venv/Scripts/activate 부분은 파워셀에서 실행하니까 안되었던 거 같은데, 너는 되었어?

**답변:**

맞습니다. 사용자 PowerShell에서는 `source` 명령이 없어서 안 됩니다.

저는 되었던 이유는 — Claude Code가 내부적으로 **bash**를 사용해서 실행하기 때문입니다. 환경 설정에도 `Shell: bash`로 명시되어 있습니다.

| 환경 | 가상환경 활성화 명령 |
|------|------------------|
| **PowerShell** | `.\venv\Scripts\Activate.ps1` |
| **CMD** | `venv\Scripts\activate.bat` |
| **bash (Claude Code 내부)** | `source venv/Scripts/activate` |

그래서 사용자가 직접 PowerShell에서 서버를 띄우려면:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## 어떻게 윈도우에서도 bash 명령이 작동할 수 있지?

**답변:**

Claude Code가 Windows에서 **Git Bash**를 내장하고 있거나, 설치된 Git에 포함된 bash를 사용하기 때문입니다.

```
사용자 (PowerShell)
       ↓
  Claude Code
       ↓
  Git Bash (bash.exe)   ← 여기서 명령 실행
       ↓
  Windows OS
```

`x86_64-pc-msys` — **MSYS2** 기반 bash입니다. Git for Windows 설치 시 함께 따라오는 Unix 호환 환경입니다.

즉, 컴퓨터에 **Git for Windows**가 설치되어 있고, 그 안에 포함된 bash를 Claude Code가 사용하는 겁니다. WSL과는 별개로, 이미 bash가 동작하고 있는 셈입니다.

---

## 스킬이 `~\.claude\skills`와 `~\.claude\commands` 두 군데를 말하는데, 실제로는 어디에 있나?

**답변:**

두 디렉토리의 역할이 **다릅니다.**

| 디렉토리 | 종류 | 실행 방식 |
|---------|------|---------|
| `~\.claude\commands\` | **슬래시 커맨드** | 사용자가 `/git-push` 처럼 직접 입력 |
| `~\.claude\skills\` | **자동 트리거 스킬** | Claude가 문맥 보고 자동으로 판단해서 사용 |

`/skills` 다이얼로그가 두 곳을 함께 보여주는 이유는, 사용자 입장에서 만든 커스텀 도구들을 한 곳에서 확인할 수 있게 하기 위해서입니다.

- `commands/git-push.md` → `/git-push` 로 수동 호출
- `skills/presentation/SKILL.md` → "발표 자료 만들어" 같은 말을 하면 자동 실행

---

## `~/.claude/agents/`와 `.claude/agents/`의 차이 (`~` 물결표시 의미)

**답변:**

`~`는 **현재 사용자의 홈 디렉토리**를 의미하는 Unix/Linux 표기법입니다.

| 경로 | 실제 경로 | 범위 |
|------|-----------|------|
| `~/.claude/agents/` | `C:\Users\901-00\.claude\agents\` | **전역** — 모든 프로젝트에서 사용 가능 |
| `.claude/agents/` | `C:\Users\901-00\test_project\.claude\agents\` | **프로젝트 한정** — 이 프로젝트에서만 사용 가능 |

전역으로 쓰고 싶다면 `~/.claude/agents/`에 복사하면 됩니다.

---

## 추천 Agent는?

현재 에이전트: `korean-code-reviewer`, `unit-test-generator`

**답변:**

| 에이전트 | 설명 |
|---------|------|
| `git-commit-writer` | 변경된 코드를 분석해서 컨벤션에 맞는 커밋 메시지 자동 작성 |
| `django-migration-checker` | models.py 변경 시 마이그레이션 누락, N+1, 인덱스 문제 탐지 |
| `template-reviewer` | Django 템플릿 전용 리뷰 (XSS, CSRF 토큰 누락 등 체크) |
| `api-doc-generator` | 뷰/URL 코드를 읽고 API 문서(Markdown) 자동 생성 |
| `security-auditor` | 보안 취약점 전용 (SQL Injection, XSS, CSRF, 인증/권한 누락 등) |

우선순위: **`security-auditor`** (권한 문제 다수 발견) → **`git-commit-writer`** (실용성) → **`template-reviewer`** (CSRF 확인 필요)

---

## `⏵ accept edits on` 모드는 뭐지?

**답변:**

Claude Code의 **권한 모드(permission mode)** 중 하나입니다.

**Shift+Tab으로 순환되는 3가지 모드:**

| 모드 | 동작 |
|------|------|
| `default` | 읽기만 자동, 나머지는 모두 확인 필요 |
| `accept edits` | 파일 편집 자동 승인, Bash 등은 확인 |
| `plan` | 변경 제안만 하고 실제 편집 안 함 |

**Shift+Tab으로는 안 나오는 모드:**
- `auto` — 안전성 검사하며 전부 자동 (별도 옵션으로만 설정 가능)
- `bypassPermissions` — 모든 체크 스킵 (격리 환경 전용)

---

## `template-reviewer` 에이전트 만드는 순서는?

**답변:**

### 1. 파일 생성
`.claude/agents/template-reviewer.md` 파일 생성
(전역으로 쓰려면 `~/.claude/agents/template-reviewer.md`)

### 2. 파일 구조 작성
```markdown
---
name: "template-reviewer"
description: "언제 이 에이전트를 호출할지 설명 (Claude가 이걸 보고 자동 판단)"
model: haiku        # sonnet / haiku / opus
color: green        # 에이전트 색상
---

에이전트 역할 및 행동 지침...
```

### 3. description 핵심 요소
- **언제** 호출하는지 명확히
- **예시** 포함하면 자동 트리거 정확도 향상

### 4. 본문에 넣을 내용
- 에이전트 역할 정의
- 리뷰 항목 (XSS, CSRF, URL 네임스페이스 등)
- 출력 형식
- 체크리스트

### 5. 확인
`/agents` 명령으로 목록에 뜨는지 확인

---

## 지금 수행중인 프로젝트 이름은?

**답변:**

메모리에 저장된 프로젝트 정보가 없습니다.

현재 작업 디렉토리는 `C:\Users\901-00` (홈 디렉토리)이며, git 저장소도 아닙니다.

진행 중인 특정 프로젝트가 있다면 알려주시면 기억해 드리겠습니다.

---

## C:\Users\901-00\.claude\projects 를 참고해서 답하라

**답변:**

현재 진행 중인 프로젝트는 **`test_project`** 입니다.

- **내용**: Django 기반 간단한 게시판 웹사이트
- **기술 스택**: Python 3.14, Django 5.x, SQLite
- **경로**: `C:\Users\901-00\test-project`
- **상태**: 기본 CRUD 기능 완성 (게시글 목록/상세/작성 + 댓글)

---

## 왜 4개의 폴더가 있지?

**답변:**

각 폴더는 **Claude Code를 실행했던 작업 디렉토리**마다 하나씩 생성됩니다.

폴더명은 경로의 `\`를 `-`로 치환한 것입니다:

| 폴더 | 실제 경로 |
|------|-----------|
| `C--Users-901-00` | `C:\Users\901-00` (홈 디렉토리) |
| `C--Users-901-00-test-project` | `C:\Users\901-00\test-project` |
| `C--Users-901-00-test-test-project` | `C:\Users\901-00\test\test-project` |
| `C--Users-901-00-test-test-project--claude-worktrees-thirsty-franklin` | `...\test-project\.claude-worktrees\thirsty-franklin` (git worktree) |

즉, 과거에 4개의 서로 다른 경로에서 Claude Code를 실행한 이력이 있기 때문입니다. 마지막 폴더는 worktree 기능을 사용했을 때 자동 생성된 것으로 보입니다.

---

## 2, 3번은 어떻게 다르지?

**답변:**

경로 구조가 다릅니다:

| 폴더 | 실제 경로 |
|------|-----------|
| `C--Users-901-00-test-project` | `C:\Users\901-00\`**`test-project`** |
| `C--Users-901-00-test-test-project` | `C:\Users\901-00\`**`test\test-project`** |

- **2번**: 홈 디렉토리 바로 아래의 `test-project` 폴더
- **3번**: `test` 폴더 안에 있는 `test-project` 폴더 (`C:\Users\901-00\test\test-project`)

현재 실제로 존재하는 것은 **3번** (`C:\Users\901-00\test\test-project`)이고, 2번은 과거에 다른 경로에서 작업했던 이력으로 보입니다.

---

## 서로 다른 경로에서 Claude Code를 실행한 이력 이라고 하는 것은 claude code 에 접속하는 방법에 대한 건가?

**답변:**

아니요, **접속 방법**이 아니라 **작업 디렉토리(Working Directory)**에 관한 것입니다.

Claude Code를 실행할 때 어느 폴더에서 실행했느냐에 따라 프로젝트가 구분됩니다.

예를 들어:
```bash
# 홈에서 실행
cd C:\Users\901-00
claude   → C--Users-901-00 폴더 생성

# test-project에서 실행
cd C:\Users\901-00\test\test-project
claude   → C--Users-901-00-test-test-project 폴더 생성
```

즉, **같은 Claude Code**를 사용하더라도 실행 위치(디렉토리)가 다르면 별도의 프로젝트로 인식해서 대화 이력과 메모리를 따로 저장합니다.

---

## 맞다. 사용중에 폴더 변경이 있었다. 그것이 3번이다. 그럼 과거의 2번 내용은, 메모리라든가, 전혀 로드되지 않는 건가?

**답변:**

네, **맞습니다. 완전히 별개**입니다.

Claude Code는 현재 실행 중인 디렉토리의 메모리만 로드합니다. 2번 폴더의 메모리는 3번에서 작업할 때 **자동으로 로드되지 않습니다.**

현재 상황:
- **2번** (`test-project`): 메모리 7개 (게시판 프로젝트 관련 내용 풍부)
- **3번** (`test\test-project`): 메모리 2개 (거의 비어있음)

폴더를 이동하면서 2번에 쌓인 메모리(게시판 진행 상황, 피드백 등)가 현재 세션에서는 로드되지 않고 있었던 상태입니다.

**해결 방법**: 2번의 메모리 파일들을 3번 폴더로 복사하면 됩니다. 복사할까요?

---

## 복사했으면 2번 폴더는 모두 지워도 되겠네?

**답변:**

두 가지 확인사항이 있습니다:

1. **MEMORY.md 업데이트가 아직 안 됐습니다** - 방금 Write가 취소됐습니다. 이것도 처리해야 합니다.
2. **2번 폴더에는 대화 이력(.jsonl 파일)도 있습니다** - 메모리 외에 과거 대화 기록인데, 지워도 괜찮으신가요?

---

## MEMORY.md 업데이트가 아직 안 되었다면 그냥 기다리면 되나? 내가 무언가 해야하나?

**답변:**

제가 해야 합니다. 방금 제가 MEMORY.md를 업데이트하려다가 사용자분께서 취소하셨기 때문에 아직 미완료 상태입니다.

지금 바로 업데이트할까요?

---

## 대화이력 파일은 왜 필요한가?

**답변:**

주로 두 가지 용도입니다:

1. **대화 재개** — Claude Code에서 `claude --continue` 또는 `/resume` 으로 이전 대화를 이어갈 때 사용
2. **감사/복기** — 과거에 어떤 작업을 했는지 기록으로 남기고 싶을 때

하지만 실질적으로는:
- 메모리 파일로 중요한 내용은 이미 옮겼고
- 2번 폴더는 **현재 경로가 아니라** 어차피 로드되지 않는 상태

특별히 과거 대화를 다시 볼 일이 없다면 **지워도 무방**합니다.

---

## No 1 — 모든 답변의 시작 줄에 이모지를 붙인후 No 답변번호 를 한줄로 표시한 후 답변하여라. 메모리에 기억

**답변:**

메모리에 저장했습니다. 앞으로 모든 답변은 첫 줄에 이모지 + `No 답변번호`를 표시하겠습니다.

❤️ 🧡 💛 💚 💙

---

## No 2 — 메모리에 "모든 답변의 첫 줄에 이모지와 함께 `No 답변번호`를 한 줄로 표시한 후 답변한다. 모든 답변의 마지막에 줄바꿈 후 새로운 줄에 `❤️ 🧡 💛 💚 💙`를 출력한다." 이 문장은 필요 없지 않나?

**답변:**

맞습니다. 메모리 파일에 규칙이 저장되어 있으니 그 설명 문장은 중복입니다. 삭제하겠습니다.

완료됐습니다.

❤️ 🧡 💛 💚 💙

---

## No 3 — 메모리 파일은 자동으로 네가 작성하는 건가?

**답변:**

네, 맞습니다. 제가 대화 중에 기억할 필요가 있다고 판단하면 자동으로 작성합니다.

구체적으로는:
- **사용자가 명시적으로 "기억해"라고 요청**할 때
- **피드백/수정 지시**를 받았을 때 (예: "Bootstrap 쓰지 마")
- **사용자 성향이나 선호**를 파악했을 때

다만 자동으로 쓰되, 파일 저장 시 사용자 승인(도구 실행 허가)이 필요하기 때문에 완전히 몰래 저장되지는 않습니다.

❤️ 🧡 💛 💚 💙

---

## No 4 — 만약 No 3 을 저장해라고 하면 어떤 파일에 추가하나?

**답변:**

"No 3을 저장해"는 **대화 내용(이력)** 이므로, 메모리 시스템에는 적합하지 않습니다.

메모리 시스템의 원칙상:
- **저장 대상**: 미래 대화에서도 유용한 규칙, 선호도, 프로젝트 상태
- **저장 안 함**: 현재 대화의 특정 내용, 일시적인 상태

따라서 "No 3을 저장해"라고 하시면 저는 **어떤 점이 기억할 만한지 여쭤볼 것**입니다. 단순히 대화 번호를 저장하는 것은 의미가 없기 때문입니다.

❤️ 🧡 💛 💚 💙

---

## No 6 — 요약하지 말고 원문 그대로를 저장하는것이다. 메모리에 기억

**답변:**

메모리에 저장했습니다. 앞으로 "N번을 저장" 시 요약 없이 원문 그대로 기록합니다.

다시 저장 진행할까요?

❤️ 🧡 💛 💚 💙

---

## No 10 — User memory vs Project memory 차이는?

**답변:**

| 구분 | User Memory | Project Memory |
|------|-------------|----------------|
| **저장 위치** | `~/.claude/projects/C--Users-901-00/memory/` | `~/.claude/projects/C--Users-901-00-test-test-project/memory/` |
| **적용 범위** | 모든 프로젝트에서 공통 적용 | 해당 프로젝트에서만 적용 |
| **내용** | 사용자 성향, 선호도, 작업 방식 | 특정 프로젝트의 상태, 규칙, 결정사항 |
| **예시** | "Django 개발자", "snake_case 선호" | "Bootstrap 사용 금지", "게시판 CRUD 완성" |

현재 이 프로젝트의 메모리는 모두 **Project Memory**(`C--Users-901-00-test-test-project`)에 저장되어 있습니다.

`C--Users-901-00` (홈 디렉토리)에는 별도의 메모리가 없는 상태입니다.

❤️ 🧡 💛 💚 💙

---

## No 12 — User Memory는 문답을 할 때마다, 계속 토큰에 넣어서 너에게 전달되는 건가?

**답변:**

네, 맞습니다. `MEMORY.md` (인덱스)는 **매 대화마다 자동으로 컨텍스트에 포함**됩니다.

다만 개별 메모리 파일(예: `user_profile.md`)은 필요할 때만 읽습니다.

```
매 턴마다 자동 로드:
  MEMORY.md (인덱스, 항상)
  CLAUDE.md (항상)

필요시에만 로드:
  user_profile.md
  feedback_no_bootstrap.md
  ...
```

그래서 `MEMORY.md`를 200줄 이하로 유지하는 게 중요한 이유가 여기 있습니다. User Memory의 `MEMORY.md`는 **모든 프로젝트**에서 매 턴 로드되니 더 부담이 큽니다.

❤️ 🧡 💛 💚 💙

---

## No 13 — user memory에 적용되는 내용은 claude.md 와 겹치는 것 같은데, 어떻게 구분하지?

**답변:**

좋은 질문입니다. 실제로 내용이 겹칠 수 있습니다. 구분 기준은 **작성자와 목적**입니다.

| 구분 | CLAUDE.md | User Memory |
|------|-----------|-------------|
| **작성자** | 사람이 직접 작성 | Claude가 자동 저장 |
| **내용** | 명시적 규칙, 프로젝트 구조 | 대화 중 파악한 사용자 성향 |
| **예시** | "Bootstrap 사용금지" | "이 사람은 Django 백엔드 개발자" |
| **수정** | 사람이 직접 편집 | Claude가 갱신 |

**실용적 기준:**
- 내가 **의도적으로 지시한 규칙** → `CLAUDE.md`
- Claude가 **대화를 통해 파악한 것** → User/Project Memory

현재 `CLAUDE.md`에 코딩 스타일, 기술 스택 등이 이미 잘 정리되어 있으므로, User Memory에 중복 저장할 필요는 없습니다.

❤️ 🧡 💛 💚 💙

---

## No 16 — user memory 의 저장위치는?

**답변:**

`C:\Users\901-00\.claude\projects\C--Users-901-00\memory\`

홈 디렉토리(`C:\Users\901-00`)에서 실행한 Claude Code 세션의 프로젝트 폴더가 User Memory 역할을 합니다.

❤️ 🧡 💛 💚 💙

---

## No 17 — User Memory는 md 파일로 있지 않나?

**답변:**

네, 방금 만든 파일들이 있습니다:

```
C:\Users\901-00\.claude\projects\C--Users-901-00\memory\
├── MEMORY.md                  ← 인덱스
├── user_profile.md            ← 사용자 프로필
├── feedback_memory.md         ← 메모리 관리 방식
├── feedback_response_style.md ← 응답 스타일
├── feedback_ppt_style.md      ← PPT 스타일
└── feedback_qna_save.md       ← QnA 저장 규칙
```

❤️ 🧡 💛 💚 💙

---

## No 23 — 왜 프로젝트는 한개인데 폴더가 2개가 되어야 하지?

**답변:**

맞는 지적입니다.

현재 Claude Code를 **홈 디렉토리**(`C:\Users\901-00`)에서 실행하고 있기 때문입니다. 프로젝트는 `test_project`인데, Claude Code 실행 위치가 다른 것입니다.

**해결 방법**: Claude Code를 항상 프로젝트 폴더에서 실행하면 됩니다.

```powershell
cd C:\Users\901-00\test\test_project
claude
```

그러면 `C--Users-901-00` 폴더는 더 이상 생성되지 않고 `C--Users-901-00-test-test-project` 하나만 사용하게 됩니다.

❤️ 🧡 💛 💚 💙

---

## No 14 — 좋아. User Memory를 사용하겠다. 깔끔하게 해라.

**답변:**

정리 계획:
- **User Memory**: 사용자 프로필, 응답 스타일, 메모리 관리 방식, PPT 스타일, QnA 저장 규칙
- **Project Memory**: 게시판 프로젝트 현황, Bootstrap 금지 (프로젝트 특유 이유)
- `claude_code_faq.md`: `qna.md`에 이미 저장됐으므로 삭제

**User Memory** (모든 프로젝트 공통):
- 사용자 프로필
- 메모리 관리 방식
- 응답 스타일 (No 번호 + 무지개 하트)
- PPT 스타일 기준
- QnA 저장 규칙

**Project Memory** (test_project 전용):
- 게시판 프로젝트 현황
- Bootstrap 사용 금지

❤️ 🧡 💛 💚 💙

---

## No 1

**Q: 전역 claude.md와 User memory 는 무슨 차이가 있지?**

이전 질문과 동일한 내용이네요. 이미 이 대화에서 설명드렸지만 다시 정리합니다.

## 전역 CLAUDE.md vs User Memory

| 구분 | 전역 CLAUDE.md | User Memory |
|------|---------------|-------------|
| **위치** | `~/.claude/CLAUDE.md` | `~/.claude/projects/.../memory/` |
| **작성자** | 사용자가 직접 편집 | Claude가 대화 중 자동 저장 |
| **목적** | **규칙/지시사항** — "이렇게 행동해라" | **관찰/학습** — "이 사용자는 이런 사람이다" |
| **Claude 인식** | 강한 지시 (반드시 따름) | 참고 맥락 (놓칠 수 있음) |
| **변경 방법** | 직접 파일 편집 | Claude에게 "기억해줘" 또는 자동 감지 |

## 한 문장으로

- **CLAUDE.md** = "항상 이렇게 해" (규칙서)
- **User Memory** = "이 사람은 이런 특징이 있어" (노트)

방금 ✅/❤️ 규칙을 User Memory → CLAUDE.md로 옮긴 것도 이 이유입니다. 규칙은 CLAUDE.md가 더 확실하게 적용됩니다.

❤️ 🧡 💛 💚 💙

---

## No 1 (재저장 - feedback_response_style.md 삭제 관련)

**Q: feedback_response_style.md 파일은 그럼 지워도 되지?**

네, 지워도 됩니다. CLAUDE.md로 옮겼으니 중복이라 삭제하는 게 깔끔합니다.

파일 삭제 및 MEMORY.md 인덱스 정리 완료했습니다.

❤️ 🧡 💛 💚 💙

---

## 프로젝트 메모리는 어느 위치에 있지?

`C:\Users\901-00\.claude\projects\C--Users-901-00-test-test-project\memory\`

현재 파일 목록:
- `MEMORY.md` — 인덱스
- `user_profile.md` — 사용자 프로필
- `project_status.md` — 프로젝트 현황
- `feedback_memory.md` — 메모리 관리 방식
- `feedback_qna_save.md` — QnA 저장 규칙

---

## User memory는 어느 위치에 있지?

User Memory와 프로젝트 메모리는 **같은 위치**입니다.

`C:\Users\901-00\.claude\projects\C--Users-901-00-test-test-project\memory\`

Claude Code에서 "User Memory"는 별도의 전역 위치가 아니라, **프로젝트별 디렉토리** 안에 저장됩니다. 프로젝트 경로가 폴더명으로 인코딩되어 구분됩니다.

- `~/.claude/` — 전역 설정 (CLAUDE.md 등)
- `~/.claude/projects/C--Users-901-00-test-test-project/memory/` — 이 프로젝트의 메모리

---

## 그럼 user memory와 프로젝트 memory는 어떻게 구별되?

실제로 **파일 시스템상 구별이 없습니다.**

둘 다 같은 폴더에 `.md` 파일로 저장되고, 구별은 파일 내부의 `type` 프론트매터로만 합니다:

```markdown
---
type: user      # 사용자 프로필/특성
type: feedback  # 행동 지침/피드백
type: project   # 프로젝트 현황/맥락
type: reference # 외부 리소스 포인터
---
```

즉, "User Memory" / "Project Memory"는 **파일 위치가 아니라 type 값**으로 구분되는 논리적 분류입니다. Claude가 이 type을 보고 어떤 맥락으로 활용할지 판단합니다.

---

## " 모두 매 대화 시작 시 MEMORY.md 인덱스를 통해 로드됩니다" 라는 건 , 5개의 md 파일이 모두 로드 된다는 건가, 필요할 때 일부만 로드 된다는 건가?

정확히는 **MEMORY.md 인덱스만 항상 로드**되고, 개별 파일은 필요할 때 읽습니다.

```
MEMORY.md (항상 로드 — 대화 컨텍스트에 포함)
├── user_profile.md        ┐
├── project_status.md      │ 필요할 때 Read 도구로
├── feedback_memory.md     │ 개별 접근
├── feedback_qna_save.md   ┘
```

**동작 방식:**
1. 대화 시작 시 MEMORY.md 인덱스가 컨텍스트에 자동 포함
2. Claude가 인덱스를 보고 관련 파일이 있다고 판단하면 Read로 해당 파일만 읽음
3. 무관하다고 판단하면 읽지 않음

실제로 이 대화에서도 "프로젝트 현황은?" 질문에 `project_status.md`만 Read했고, "QnA 저장" 시에는 `feedback_qna_save.md`만 Read한 것이 그 증거입니다.

---

## 그렇다면 ~/.claude/projects/C--Users-901-00-test-test-project/memory/ 안의 md 파일들은 개수가 아무리 많아도, 한개의 파일이 크기가 커도 큰 상관은 없겠네?

**반은 맞고 반은 틀립니다.**

### 개수가 많아도 괜찮은 이유
MEMORY.md 인덱스만 항상 로드되니, 개별 파일이 100개여도 인덱스 크기만 영향을 줍니다.

### 하지만 주의할 점

**MEMORY.md 인덱스 크기 제한이 있습니다:**
- 시스템 설명에 명시: **200줄 초과 시 잘림**
- 인덱스가 잘리면 Claude가 해당 파일의 존재를 모름 → 로드 안 됨

**개별 파일 크기도 영향 있습니다:**
- 파일을 Read할 때 컨텍스트 토큰을 소비
- 이 대화에서 `qna.md`가 10,000 토큰 초과로 Read 실패한 것이 실제 사례

### 결론
- 개별 파일 수 → 크게 상관 없음 ✅
- MEMORY.md 인덱스 → 200줄 이내로 관리 필요 ⚠️
- 개별 파일 크기 → 너무 크면 Read 실패 가능 ⚠️

---

## 프로젝트가 여려개 있을 때 각각의 프로젝트에서 사용하는 skill은 어디에 저장되나?

Skill은 **전역 위치**에 저장됩니다. 프로젝트별로 분리되지 않습니다.

```
~/.claude/
├── CLAUDE.md              # 전역 지시사항
├── settings.json          # 전역 설정
└── skills/                # 모든 프로젝트 공통
    ├── backend.md
    ├── frontend.md
    ├── presentation.md
    └── git-push.md
```

즉, 어떤 프로젝트에서 작업하든 동일한 skill 세트를 사용합니다.

**프로젝트별로 다른 skill을 쓰고 싶다면?**
- 프로젝트 `CLAUDE.md`에 직접 규칙을 작성하는 방법이 현실적입니다.
- 또는 skill 내부에서 프로젝트 감지 로직을 넣는 방식도 가능합니다.

---

## 프로젝트에 적용되는 스킬은 ~\.claude\projects\C--Users-901-00-test-test-project\memory 에서 사용하는 게 맞지?

아닙니다. 스킬과 메모리는 **저장 위치가 다릅니다**.

| 항목 | 위치 | 역할 |
|------|------|------|
| **Memory** | `~\.claude\projects\...\memory\` | 사용자/프로젝트 관련 정보를 대화 간 기억 |
| **Skills** | `~\.claude\` (전역) 또는 프로젝트 내 | 특정 작업 패턴을 정의한 프롬프트 템플릿 |

스킬은 보통 아래 경로에 `.md` 파일로 저장됩니다:

```
~\.claude\skills\          ← 전역 스킬
test_project\.claude\skills\   ← 프로젝트 스킬 (있을 경우)
```

- `memory/` 폴더 = **기억** (누가, 뭘 좋아하고, 어떤 규칙으로 일하는지 등)
- 스킬 = **작업 패턴 정의** (명령어처럼 불러서 쓰는 프롬프트 조각)

두 개는 독립적으로 동작하며, 현재 대화에서 사용 중인 스킬 목록은 system-reminder에서 확인할 수 있습니다.

❤️ 🧡 💛 💚 💙

---
## No 1 — 메모리에서 "Open auto-memory folder"를 하면 어떤 파일을 Open하나?

**답변:**

**"Open auto-memory folder"** 를 선택하면 아래 경로의 **폴더**가 열립니다:

```
C:\Users\901-00\.claude\projects\C--Users-901-00-test-test-project\memory\
```

이 폴더 안에는 다음 파일들이 있습니다:

| 파일 | 내용 |
|------|------|
| `MEMORY.md` | 메모리 인덱스 (목차 역할) |
| `user_profile.md` | 사용자 프로필 |
| `feedback_memory.md` | 메모리 관리 방식 |
| `feedback_qna_save.md` | QnA 저장 규칙 |
| `project_status.md` | 프로젝트 현황 |

특정 파일 하나를 여는 게 아니라 **폴더 자체**를 파일 탐색기(또는 IDE)로 열어서, 안에 있는 메모리 파일들을 직접 확인·편집할 수 있게 해줍니다.

❤️ 🧡 💛 💚 💙

---

## No 2 — 이 메모리는 스킬과 달리 항상 로드되나?

**답변:**

**부분적으로만** 항상 로드됩니다.

| 구분 | 로드 방식 |
|------|----------|
| **MEMORY.md** (인덱스) | ✅ 항상 자동 로드 — 매 대화 시작 시 context에 포함 |
| **개별 메모리 파일** (`.md`) | ⚠️ 필요할 때만 읽음 — Claude가 판단해서 Read |
| **스킬** | ❌ 트리거 조건 충족 시에만 로드 |

즉, `MEMORY.md`의 인덱스 한 줄짜리 요약들은 항상 보이지만, `user_profile.md` 같은 개별 파일의 **상세 내용**은 Claude가 관련있다고 판단할 때 직접 읽어야 합니다.

실제로 이 대화 상단 system-reminder에도 `MEMORY.md` 내용이 자동으로 들어와 있는 걸 확인할 수 있습니다.

❤️ 🧡 💛 💚 💙

---

## 그럼 아까 User memory도 필요할 때만 호출해서 로드한다고 했지?
● ✅ No 8

  네, 맞습니다. 구조가 스킬과 유사합니다.

  ┌────────┬────────────────────────────────────┬────────────────────────────┐
  │  항목  │             항상 로드              │      필요할 때만 로드      │
  ├────────┼────────────────────────────────────┼────────────────────────────┤
  │ 스킬   │ system-reminder의 description 목록 │ Skill 도구로 SKILL.md 내용 │
  ├────────┼────────────────────────────────────┼────────────────────────────┤
  │ 메모리 │ MEMORY.md 인덱스                   │ Read 도구로 개별 .md 파일  │
  └────────┴────────────────────────────────────┴────────────────────────────┘

  동작 방식 비교:

  - 스킬: description 보고 판단 → Skill 도구로 본문 로드
  - 메모리: MEMORY.md 인덱스 보고 판단 → Read 도구로 개별 파일 로드

  둘 다 인덱스/목록은 항상 컨텍스트에 있고, 실제 내용은 필요할 때만 가져오는 동일한 패턴입니다.
