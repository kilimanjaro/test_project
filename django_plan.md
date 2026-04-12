# Django 게시판 심화 Q&A 가이드

> Python · Django · 순수 CSS/JS
> 게시판 기본 CRUD 완성 후 수정/삭제·페이지네이션·검색 기능 구현 Q&A

---

## 목차

1. [게시글 수정 기능 — 설계](#1-게시글-수정-기능--설계)
2. [게시글 수정 기능 — 구현](#2-게시글-수정-기능--구현)
3. [게시글 삭제 기능 — 설계](#3-게시글-삭제-기능--설계)
4. [게시글 삭제 기능 — 구현](#4-게시글-삭제-기능--구현)
5. [댓글 삭제 기능](#5-댓글-삭제-기능)
6. [페이지네이션 — 개념](#6-페이지네이션--개념)
7. [페이지네이션 — 구현](#7-페이지네이션--구현)
8. [검색 기능 — 설계](#8-검색-기능--설계)
9. [검색 기능 — 구현](#9-검색-기능--구현)
10. [페이지네이션 + 검색 연동](#10-페이지네이션--검색-연동)
11. [순수 CSS로 UI 스타일링](#11-순수-css로-ui-스타일링)
12. [Claude Code /memory 활용](#12-claude-code-memory-활용)
13. [전체 프로젝트 구조 정리](#13-전체-프로젝트-구조-정리)

---

## 1. 게시글 수정 기능 — 설계

**Q. 게시글 수정 기능을 설계할 때 무엇을 고려해야 할까?**

### 함수형 뷰 vs CBV(UpdateView)

| 항목 | 함수형 뷰 | UpdateView (CBV) |
|------|-----------|-----------------|
| 코드량 | 많음 | 적음 |
| 유연성 | 높음 | 낮음 |
| 학습 난이도 | 낮음 | 높음 |
| 이 프로젝트 선택 | ✅ | |

이 프로젝트는 기존 뷰가 모두 함수형이므로 일관성을 위해 함수형 뷰 사용.

### URL 설계

```
/board/<pk>/edit/    →  게시글 수정 (GET: 폼 표시, POST: 저장)
```

### 핵심 고려사항

- GET 요청 시 기존 데이터로 폼을 미리 채워서 표시
- POST 요청 시 유효성 검사 후 저장 → 상세 페이지로 리다이렉트
- 작성자 본인만 수정 가능 여부 (현재는 로그인 없으므로 생략)

---

## 2. 게시글 수정 기능 — 구현

**Q. 게시글 수정 뷰·URL·템플릿을 어떻게 구현할까?**

### views.py

```python
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('board:detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/edit.html', {'form': form, 'post': post})
```

- `instance=post` — 기존 데이터를 폼에 바인딩하는 핵심 파라미터

### urls.py

```python
path('<int:pk>/edit/', views.post_edit, name='edit'),
```

### edit.html (핵심 부분)

```html
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">수정 완료</button>
  <a href="{% url 'board:detail' post.pk %}">취소</a>
</form>
```

---

## 3. 게시글 삭제 기능 — 설계

**Q. 게시글 삭제 기능을 설계할 때 주의할 점은?**

### GET 방식 삭제의 문제점

```html
<!-- 위험: 링크 클릭만으로 삭제됨 -->
<a href="/board/1/delete/">삭제</a>
```

- 브라우저 prefetch, 크롤러 등이 링크를 요청하면 데이터가 삭제될 수 있음
- **반드시 POST 방식**으로 처리해야 함

### 권장 방식

```html
<!-- 안전: form의 POST 요청으로만 삭제 -->
<form method="post" action="{% url 'board:delete' post.pk %}">
  {% csrf_token %}
  <button type="submit" onclick="return confirm('삭제하시겠습니까?')">삭제</button>
</form>
```

---

## 4. 게시글 삭제 기능 — 구현

**Q. 게시글 삭제 뷰와 URL을 어떻게 구현할까?**

### views.py

```python
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('board:list')
    return redirect('board:detail', pk=pk)
```

- GET 요청으로 접근하면 상세 페이지로 돌려보냄 (직접 URL 접근 방지)

### urls.py

```python
path('<int:pk>/delete/', views.post_delete, name='delete'),
```

### detail.html에 삭제 버튼 추가

```html
<form method="post" action="{% url 'board:delete' post.pk %}">
  {% csrf_token %}
  <button type="submit" onclick="return confirm('정말 삭제하시겠습니까?')">
    삭제
  </button>
</form>
```

---

## 5. 댓글 삭제 기능

**Q. 댓글 삭제는 어떻게 구현할까?**

### views.py

```python
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
    return redirect('board:detail', pk=post_pk)
```

- 댓글 삭제 후 원래 게시글 상세 페이지로 리다이렉트
- `post_pk`를 삭제 전에 미리 저장하는 것이 핵심

### urls.py

```python
path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
```

### detail.html에 댓글 삭제 버튼

```html
{% for comment in post.comments.all %}
  <div>
    <strong>{{ comment.author }}</strong>
    <p>{{ comment.content }}</p>
    <form method="post" action="{% url 'board:comment_delete' comment.pk %}">
      {% csrf_token %}
      <button type="submit" onclick="return confirm('삭제?')">삭제</button>
    </form>
  </div>
{% endfor %}
```

---

## 6. 페이지네이션 — 개념

**Q. Django의 페이지네이션은 어떻게 동작할까?**

### Paginator 클래스

```python
from django.core.paginator import Paginator

posts = Post.objects.all()       # 전체 쿼리셋
paginator = Paginator(posts, 10) # 페이지당 10개
page_obj = paginator.get_page(1) # 1페이지 데이터
```

### page_obj 주요 속성

| 속성 | 설명 |
|------|------|
| `page_obj.object_list` | 현재 페이지의 게시글 목록 |
| `page_obj.has_previous()` | 이전 페이지 존재 여부 |
| `page_obj.has_next()` | 다음 페이지 존재 여부 |
| `page_obj.previous_page_number()` | 이전 페이지 번호 |
| `page_obj.next_page_number()` | 다음 페이지 번호 |
| `page_obj.number` | 현재 페이지 번호 |
| `paginator.num_pages` | 전체 페이지 수 |

---

## 7. 페이지네이션 — 구현

**Q. 게시판 목록에 페이지네이션을 어떻게 적용할까?**

### views.py 수정

```python
def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'board/list.html', {'page_obj': page_obj})
```

### list.html 페이지 버튼

```html
<!-- 게시글 목록 -->
{% for post in page_obj %}
  <div>{{ post.title }}</div>
{% endfor %}

<!-- 페이지 버튼 -->
<div>
  {% if page_obj.has_previous %}
    <a href="?page={{ page_obj.previous_page_number }}">이전</a>
  {% endif %}

  <span>{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>

  {% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">다음</a>
  {% endif %}
</div>
```

---

## 8. 검색 기능 — 설계

**Q. 게시판 검색 기능을 어떻게 설계해야 할까?**

### GET 파라미터 방식

```
/board/?q=Django
```

- URL에 검색어가 포함되어 공유 가능
- 북마크, 뒤로가기 등 브라우저 기능과 호환됨
- POST 방식보다 검색에 적합

### Q 객체 OR 검색

```python
from django.db.models import Q

Post.objects.filter(
    Q(title__icontains=query) | Q(content__icontains=query)
)
```

- `icontains` — 대소문자 구분 없이 포함 여부 검색
- `Q` 객체의 `|` 연산자로 제목 또는 내용 중 하나라도 일치하면 반환

---

## 9. 검색 기능 — 구현

**Q. 검색 뷰와 템플릿을 어떻게 구현할까?**

### views.py 수정

```python
from django.db.models import Q

def post_list(request):
    query = request.GET.get('q', '')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'board/list.html', {
        'page_obj': page_obj,
        'query': query,
    })
```

### list.html 검색 폼

```html
<form method="get" action="{% url 'board:list' %}">
  <input type="text" name="q" value="{{ query }}" placeholder="검색어 입력">
  <button type="submit">검색</button>
</form>
```

---

## 10. 페이지네이션 + 검색 연동

**Q. 검색 결과에서 페이지를 이동하면 검색어가 사라지는 문제를 어떻게 해결할까?**

### 문제 상황

```html
<!-- 검색어 유지 안 됨 -->
<a href="?page={{ page_obj.next_page_number }}">다음</a>
```

페이지 이동 시 `q` 파라미터가 사라져 검색 결과가 초기화됨.

### 해결 방법 — 검색어를 URL에 함께 포함

```html
<!-- 검색어 유지됨 -->
{% if page_obj.has_previous %}
  <a href="?q={{ query }}&page={{ page_obj.previous_page_number }}">이전</a>
{% endif %}

{% if page_obj.has_next %}
  <a href="?q={{ query }}&page={{ page_obj.next_page_number }}">다음</a>
{% endif %}
```

---

## 11. 순수 CSS로 UI 스타일링

**Q. Bootstrap 없이 카드·버튼·폼을 어떻게 스타일링할까?**

### 기본 리셋 + 공통 스타일

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans KR', sans-serif; background: #f4f6fb; color: #333; }
```

### 카드 스타일

```css
.card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
```

### 버튼 스타일

```css
.btn {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}
.btn-primary { background: #1a6bc6; color: #fff; }
.btn-danger  { background: #e74c3c; color: #fff; }
```

### 폼 스타일

```css
input[type="text"], textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}
```

---

## 12. Claude Code /memory 활용

**Q. Claude Code의 /memory 기능은 어떻게 활용할까?**

### 구조

```
~/.claude/projects/{프로젝트경로}/memory/
├── MEMORY.md           ← 목차만 (200줄 제한, 항상 로드됨)
├── user_profile.md     ← 사용자 정보
├── project_status.md   ← 프로젝트 현황
├── feedback_memory.md  ← 작업 피드백
└── ...
```

### MEMORY.md 역할

- 항상 컨텍스트에 로드되는 **인덱스 파일**
- 실제 내용은 개별 파일에 저장
- 200줄 초과 시 잘림 → 간결하게 유지

### 실용적 활용

```
"앞으로 뷰는 항상 함수형으로 작성해"
→ Claude가 feedback_memory.md에 자동 저장
→ 다음 대화에서도 동일 규칙 적용
```

---

## 13. 전체 프로젝트 구조 정리

```
test_project/
├── CLAUDE.md                    # 프로젝트 Claude 설정
├── manage.py
├── requirements.txt
├── db.sqlite3
├── django_qa.md                 # 기초 Q&A 가이드
├── django_plan.md               # 심화 Q&A 가이드 (이 파일)
├── config/
│   ├── settings.py
│   └── urls.py
├── board/
│   ├── models.py                # Post, Comment 모델
│   ├── views.py                 # index, list, detail, write, edit, delete, comment
│   ├── forms.py                 # PostForm, CommentForm
│   └── urls.py
└── templates/
    ├── base.html
    ├── index.html
    └── board/
        ├── list.html            # 목록 + 검색 + 페이지네이션
        ├── detail.html          # 상세 + 댓글 + 수정/삭제 버튼
        ├── write.html
        └── edit.html            # 게시글 수정 폼
```

---

*Django 게시판 심화 Q&A 가이드 — 2026*
