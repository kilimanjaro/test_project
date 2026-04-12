# 선택한 질문 목록

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
