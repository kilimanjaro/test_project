# Django 프로젝트 Q&A 가이드북

> Python · Django · Bootstrap 5 · GitHub Actions · Claude Code
> 게시판 웹사이트를 처음부터 완성까지 만들어 가는 과정의 핵심 Q&A 정리

---

## 목차

1. [Python 웹 개발 프레임워크 선택](#1-python-웹-개발-프레임워크-선택)
2. [Django 프로젝트 초기 세팅 절차](#2-django-프로젝트-초기-세팅-절차)
3. [CLAUDE.md 개념과 활용](#3-claudemd-개념과-활용)
4. [프로젝트 & 글로벌 CLAUDE.md 비교](#4-프로젝트--글로벌-claudemd-비교)
5. [Django 프로젝트 구조 설계](#5-django-프로젝트-구조-설계)
6. [게시판 앱 구현 (모델·뷰·URL·템플릿)](#6-게시판-앱-구현)
7. [답글 기능 — 모델 & 폼 설계](#7-답글-기능--모델--폼-설계)
8. [답글 기능 — 뷰 & URL 연결](#8-답글-기능--뷰--url-연결)
9. [게시판 목록에 답글 수 표시](#9-게시판-목록에-답글-수-표시)
10. [답글 배지 스타일 개선](#10-답글-배지-스타일-개선)
11. [UI 모던화 — 설계 원칙](#11-ui-모던화--설계-원칙)
12. [UI 모던화 — 적용 기술 상세](#12-ui-모던화--적용-기술-상세)
13. [GitHub Actions CI 트리거](#13-github-actions-ci-트리거)
14. [GitHub 브랜치 전략](#14-github-브랜치-전략)
15. [글로벌 CLAUDE.md 생성](#15-글로벌-claudemd-생성)
16. [주석 처리 vs 삭제 — 토큰 차이](#16-주석-처리-vs-삭제--토큰-차이)
17. [전체 프로젝트 구조 정리](#17-전체-프로젝트-구조-정리)

---

## 1. Python 웹 개발 프레임워크 선택

**Q. Python으로 웹사이트를 만드는 절차는?**

### Flask vs Django 비교

| 항목 | Flask | Django |
|------|-------|--------|
| 성격 | 마이크로 프레임워크 | 풀스택 프레임워크 |
| 자유도 | 높음 | 낮음 (규칙이 많음) |
| 적합한 경우 | 소규모, API 서버 | 게시판, 커머스, 관리자 화면 |
| 내장 기능 | 최소한 | ORM, 관리자, 인증 내장 |

### Django 선택 근거

- ORM으로 SQL 없이 모델 클래스만으로 DB 조작 가능
- `/admin` 경로에서 데이터 즉시 확인·수정 가능
- 마이그레이션 시스템으로 DB 스키마 변경 이력 관리
- Bootstrap 5 CDN과 조합해 프론트엔드 별도 설치 불필요

---

## 2. Django 프로젝트 초기 세팅 절차

**Q. Django 프로젝트 초기 세팅, 어떤 순서로 진행하나?**

### 1단계 — 가상환경 & 패키지

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install django
pip freeze > requirements.txt
```

### 2단계 — 프로젝트·앱 생성

```bash
django-admin startproject config .
python manage.py startapp board
```

### 3단계 — settings.py 필수 수정

```python
INSTALLED_APPS = [
    ...
    'board',          # 앱 등록
]

TEMPLATES = [{'DIRS': [BASE_DIR / 'templates'], ...}]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
```

### 4단계 — DB 초기화

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver     # http://127.0.0.1:8000
```

---

## 3. CLAUDE.md 개념과 활용

**Q. CLAUDE.md란 무엇이고 왜 만들어야 할까?**

### 개념

- Claude Code가 대화 시작 시 **자동으로 읽는** 프로젝트 컨텍스트 파일
- 매 대화마다 "이 프로젝트는 Django입니다" 같은 반복 설명이 불필요해짐
- 팀원과 공유하면 누구나 동일한 컨텍스트로 Claude를 활용 가능

### 포함할 내용

- 프로젝트 목적 및 기술 스택 (Python 버전, Django 버전, DB 종류)
- 페이지 구성표 (URL, 설명)
- 프로젝트 디렉토리 구조
- 자주 쓰는 명령어 (서버 실행, 마이그레이션, 슈퍼유저 생성)
- 코딩 컨벤션 (snake_case, PascalCase, verbose_name 등)

---

## 4. 프로젝트 & 글로벌 CLAUDE.md 비교

**Q. 프로젝트 CLAUDE.md와 글로벌 CLAUDE.md의 차이는?**

| 항목 | 프로젝트 | 글로벌 |
|------|---------|--------|
| 위치 | `test_project/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| 적용 범위 | 해당 프로젝트에서만 | 모든 프로젝트에서 항상 |
| 내용 | 프로젝트 구조, 명령어, 스택 | 개인 작업 스타일, 선호도 |
| 공유 여부 | 팀원과 공유 가능 | 개인 전용 |

### 글로벌 CLAUDE.md에 넣을 내용

```markdown
## 언어
- 항상 한국어로 답변 (기술 용어는 영어 유지)

## 작업 방식
- 파일 수정 전 반드시 먼저 읽기
- 요청한 것만 변경, 불필요한 리팩토링 금지

## 선호 스택
- Django / Bootstrap 5 / SQLite(개발) / PostgreSQL(운영)
```

> **Windows 경로:** `C:\Users\{사용자명}\.claude\CLAUDE.md`

---

## 5. Django 프로젝트 구조 설계

**Q. Django 게시판 앱의 구조를 어떻게 설계해야 할까?**

### 앱 구성 요소

| 파일 | 역할 |
|------|------|
| `models.py` | Post 모델 (title, content, author, created_at) |
| `forms.py` | PostForm, CommentForm (ModelForm 상속) |
| `views.py` | index, post_list, post_detail, post_write, comment_write |
| `urls.py` | app_name='board', 네임스페이스 기반 URL 설계 |

### URL 구조

```
/                      →  랜딩페이지        (index)
/board/                →  게시글 목록       (board:list)
/board/<pk>/           →  게시글 상세       (board:detail)
/board/write/          →  글 작성           (board:write)
/board/<pk>/comment/   →  답글 작성         (board:comment_write)
```

---

## 6. 게시판 앱 구현

**Q. 게시판 앱의 모델과 폼을 어떻게 구현할까?**

### Post 모델

```python
class Post(models.Model):
    title      = models.CharField(verbose_name='제목', max_length=200)
    content    = models.TextField(verbose_name='내용')
    author     = models.CharField(verbose_name='작성자', max_length=50)
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
```

### PostForm

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content']
        widgets = {
            'title':   forms.TextInput(attrs={'class': 'form-control'}),
            'author':  forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }
```

---

## 7. 답글 기능 — 모델 & 폼 설계

**Q. 답글(댓글) 기능을 추가하려면 무엇이 필요할까?**

### Comment 모델

```python
class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE,
                                   related_name='comments')
    author     = models.CharField(verbose_name='작성자', max_length=50)
    content    = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
```

### 핵심 설계 포인트

- `ForeignKey` → Post 1 : Comment N 관계 (게시글 삭제 시 댓글도 삭제)
- `related_name='comments'` → `post.comments.all()` 역참조 가능
- `ordering=['created_at']` → 오래된 답글이 위에 표시

### 마이그레이션

```bash
python manage.py makemigrations   # 0002_comment.py 생성
python manage.py migrate           # DB에 comments 테이블 생성
```

---

## 8. 답글 기능 — 뷰 & URL 연결

**Q. 답글 뷰와 URL은 어떻게 연결할까?**

### comment_write 뷰

```python
def comment_write(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post   # 외래키 직접 지정
            comment.save()
    return redirect('board:detail', pk=pk)
```

### URL 등록

```python
# board/urls.py
path('<int:pk>/comment/', views.comment_write, name='comment_write'),
```

### 템플릿에서 답글 목록 출력

```html
{% for comment in post.comments.all %}
  <div class="card mb-2">
    <strong>{{ comment.author }}</strong>
    <p>{{ comment.content }}</p>
  </div>
{% empty %}
  <p>아직 답글이 없습니다.</p>
{% endfor %}
```

---

## 9. 게시판 목록에 답글 수 표시

**Q. 게시판 목록에서 답글 수를 어떻게 표시할까?**

### 기본 배지 (처음 구현)

```html
{% if post.comments.count > 0 %}
  <span class="badge bg-primary ms-1">{{ post.comments.count }}</span>
{% endif %}
```

> **문제점:** 배지가 너무 크고 튀어 보임

### 개선된 오른쪽 어깨 배지

```html
{% if post.comments.count > 0 %}
  <sup style="font-size:0.65em; color:#fff; background:#e74c3c;
              border-radius:50%; padding:1px 5px; font-weight:bold;">
    {{ post.comments.count }}
  </sup>
{% endif %}
```

- `sup` 태그로 오른쪽 어깨 위에 소형 원형 배치
- 답글이 0인 경우 배지 미표시 (조건부 렌더링)

---

## 10. 답글 배지 스타일 개선

**Q. 배지 모양이 너무 크다. 어떻게 작고 예쁘게 만들까?**

### 변경 전 vs 변경 후

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 태그 | `<span class="badge">` | `<sup>` |
| 크기 | Bootstrap 기본 배지 크기 | `font-size: 0.65em` |
| 위치 | 제목 옆 (같은 라인) | 오른쪽 어깨 위 |
| 모양 | 둥근 사각형 | 원형 (`border-radius: 50%`) |
| 색상 | Bootstrap primary (파랑) | 빨강 (`#e74c3c`) |

---

## 11. UI 모던화 — 설계 원칙

**Q. 게시판 UI를 어떻게 모던하게 개선할까?**

### 디자인 원칙

- **색상:** 딥 네이비(`#1a1a2e`) 기반 그라데이션 네비바
- **레이아웃:** 테이블 → 카드형 `list-group` (시각적 분리감)
- **타이포그래피:** Google Fonts Noto Sans KR (한글 가독성 향상)
- **아이콘:** Bootstrap Icons CDN (`bi-person`, `bi-clock`, `bi-chat-dots`)
- **버튼:** `border-radius: 50px` 둥근 그라데이션 스타일

### 적용 위치별 변경

| 파일 | 변경 내용 |
|------|-----------|
| `base.html` | 다크 그라데이션 네비바, active 페이지 하이라이트 |
| `index.html` | 히어로 섹션 + 이모지 특징 카드 3개 |
| `list.html` | 카드형 목록, 번호·작성자·시간 한 줄 표시 |
| `detail.html` | 왼쪽 파란 `border-left` 답글 카드 |
| `write.html` | 폼 중앙 정렬, 둥근 등록/취소 버튼 |

---

## 12. UI 모던화 — 적용 기술 상세

**Q. Bootstrap 외에 어떤 기술을 추가로 적용했나?**

### CDN 추가 목록

```html
<!-- Bootstrap 5 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap Icons -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">

<!-- Google Fonts (Noto Sans KR) -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
```

### 핵심 CSS

```css
* { font-family: 'Noto Sans KR', sans-serif; }
body { background: #f4f6fb; }

.navbar {
  background: linear-gradient(135deg, #1a1a2e, #0f3460) !important;
}
.btn-primary {
  background: linear-gradient(135deg, #0f3460, #1a6bc6);
  border-radius: 50px;
  border: none;
}
```

---

## 13. GitHub Actions CI 트리거

**Q. GitHub Actions CI 트리거를 어떻게 설정할까?**

### 워크플로우 파일 위치

```
.github/workflows/ci.yml
```

### 트리거 조건

```yaml
on:
  push:
    branches: [ "main", "develop" ]   # push 시 자동 실행
  pull_request:
    branches: [ "main" ]              # PR 시 자동 실행
```

### 자동화 5단계

```yaml
steps:
  - uses: actions/checkout@v4               # 1. 코드 체크아웃
  - uses: actions/setup-python@v5           # 2. Python 환경 구성
    with: { python-version: "3.14" }
  - run: pip install -r requirements.txt    # 3. 패키지 설치
  - run: python manage.py check             # 4. Django 설정 검사
  - run: python manage.py test              # 5. 테스트 실행
```

---

## 14. GitHub 브랜치 전략

**Q. GitHub 브랜치 전략은 어떻게 구성해야 할까?**

### 권장 브랜치 구조

```
main        ← 배포용. PR만 허용, 직접 push 금지 권장
develop     ← 개발 통합 브랜치
feature/*   ← 기능 단위 브랜치 (예: feature/comment-reply)
```

### 작업 흐름

```bash
git checkout -b feature/새기능     # 기능 브랜치 생성
# ... 개발 ...
git push origin feature/새기능
# GitHub에서 develop으로 PR → CI 통과 → merge
# develop → main PR → CI 통과 → 배포
```

### GitHub 연동 초기 설정

```bash
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/{username}/{repo}.git
git branch -M main
git push -u origin main
```

---

## 15. 글로벌 CLAUDE.md 생성

**Q. 글로벌 CLAUDE.md를 만들고 관리하는 방법은?**

### 파일 위치

```
C:\Users\{사용자명}\.claude\CLAUDE.md   (Windows)
~/.claude/CLAUDE.md                      (Mac/Linux)
```

- 메모장·VS Code 등 텍스트 편집기로 직접 수정 가능
- 다음 대화 시작 시 자동 적용됨

### 이 프로젝트에서 설정한 내용

```markdown
## 언어
- 항상 한국어로 답변 (기술 용어는 영어 유지)

## 작업 방식
- 파일 수정 전 반드시 먼저 읽기
- 요청한 것만 변경, 불필요한 리팩토링 금지
- 꼭 필요한 경우가 아니면 새 파일 생성 금지

## 코딩 스타일
- 변수/함수: snake_case  /  클래스: PascalCase
- 불필요한 주석 금지

## 선호 기술 스택
- Django / Bootstrap 5 / SQLite(개발) / PostgreSQL(운영)

## 응답 스타일
- 간결하게, 변경 이유 한 줄, 불필요한 칭찬 생략
```

---

## 16. 주석 처리 vs 삭제 — 토큰 차이

**Q. CLAUDE.md에서 주석(#) 처리와 삭제, 토큰 차이가 있을까?**

### 핵심 결론

> CLAUDE.md는 마크다운 문서 → `#`은 **주석이 아니라 제목(Heading)**
> 주석 처리를 해도 Claude는 그 줄을 **그대로 읽는다**

### 비교표

| 방법 | 토큰 | Claude 읽음 여부 |
|------|------|-----------------|
| 주석 처리 (`# ...`) | 동일 | ✅ 읽음 |
| 완전 삭제 | 감소 | ❌ 읽지 않음 |

### 실무 팁

- CLAUDE.md는 매 대화마다 컨텍스트에 **자동 포함**됨
- 내용이 짧을수록 매 대화 토큰 비용 절감 효과
- 불필요한 내용은 주석 처리 말고 **완전 삭제** 권장

---

## 17. 전체 프로젝트 구조 정리

```
test_project/
├── CLAUDE.md                    # 프로젝트 Claude 설정
├── manage.py
├── requirements.txt
├── db.sqlite3                   # SQLite 데이터베이스
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI
├── config/                      # Django 설정 패키지
│   ├── settings.py
│   └── urls.py
├── board/                       # 게시판 앱
│   ├── models.py                # Post, Comment 모델
│   ├── views.py                 # index, list, detail, write, comment
│   ├── forms.py                 # PostForm, CommentForm
│   └── urls.py
└── templates/
    ├── base.html                # 공통 레이아웃
    ├── index.html               # 랜딩페이지
    └── board/
        ├── list.html            # 게시판 목록
        ├── detail.html          # 게시글 + 답글
        └── write.html           # 글 작성
```

---

*Django 게시판 프로젝트 Q&A 가이드북 — 2026*
