from django.test import TestCase
from board.forms import PostForm, CommentForm


class PostFormTest(TestCase):
    def test_valid_form(self):
        """필수 필드가 모두 있을 때 유효한 폼인지 확인"""
        form = PostForm(data={'title': '제목', 'content': '내용', 'author': '작성자'})
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        """제목 없으면 유효하지 않은지 확인"""
        form = PostForm(data={'title': '', 'content': '내용', 'author': '작성자'})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_missing_content(self):
        """내용 없으면 유효하지 않은지 확인"""
        form = PostForm(data={'title': '제목', 'content': '', 'author': '작성자'})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_missing_author(self):
        """작성자 없으면 유효하지 않은지 확인"""
        form = PostForm(data={'title': '제목', 'content': '내용', 'author': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('author', form.errors)

    def test_title_max_length(self):
        """제목이 200자 초과 시 유효하지 않은지 확인"""
        form = PostForm(data={'title': 'a' * 201, 'content': '내용', 'author': '작성자'})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_fields(self):
        """폼 필드가 title, author, content 세 개인지 확인"""
        form = PostForm()
        self.assertEqual(list(form.fields.keys()), ['title', 'author', 'content'])


class CommentFormTest(TestCase):
    def test_valid_form(self):
        """필수 필드가 모두 있을 때 유효한 폼인지 확인"""
        form = CommentForm(data={'author': '댓글작성자', 'content': '댓글 내용'})
        self.assertTrue(form.is_valid())

    def test_missing_author(self):
        """작성자 없으면 유효하지 않은지 확인"""
        form = CommentForm(data={'author': '', 'content': '댓글 내용'})
        self.assertFalse(form.is_valid())
        self.assertIn('author', form.errors)

    def test_missing_content(self):
        """내용 없으면 유효하지 않은지 확인"""
        form = CommentForm(data={'author': '댓글작성자', 'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_fields(self):
        """폼 필드가 author, content 두 개인지 확인"""
        form = CommentForm()
        self.assertEqual(list(form.fields.keys()), ['author', 'content'])
