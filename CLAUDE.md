# 프로젝트 개요

- **목적**: 간단한 게시판 웹사이트
- **Python 버전**: 3.14
- **Django 버전**: 5.x
- **DB**: SQLite (개발용)

## 페이지 구성

| 페이지 | URL | 설명 |
|--------|-----|------|
| 랜딩페이지 | `/` | 사이트 소개 + 상단 메뉴 |
| 게시판 목록 | `/board/` | 글 목록 |
| 게시글 상세 | `/board/<id>/` | 글 상세 보기 |
| 글 작성 | `/board/write/` | 새 글 작성 |

## 프로젝트 구조

```
test_project/
├── CLAUDE.md
├── manage.py
├── requirements.txt
├── config/              # Django 설정 패키지
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── board/               # 게시판 앱
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
        ├── base.html        # 공통 레이아웃 (상단 메뉴 포함)
        ├── index.html       # 랜딩페이지
        └── board/
            ├── list.html    # 게시판 목록
            ├── detail.html  # 게시글 상세
            └── write.html   # 글 작성
```

## 자주 쓰는 명령어

```bash
# 가상환경 활성화
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 서버 실행
python manage.py runserver

# 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

## 코딩 컨벤션

- 변수/함수: `snake_case`
- 클래스: `PascalCase`
- 모델 필드에 `verbose_name` 추가
- 템플릿은 `board/templates/` 아래 위치
- URL 이름은 `board:list`, `board:detail` 형태로 네임스페이스 사용

## 기술 스택

- **Backend**: Django 5.x
- **Frontend**: Django 템플릿 + Bootstrap 5 (CDN)
- **DB**: SQLite
