from django.test import TestCase
from django.urls import reverse
from board.models import Post


class PostEditTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='원본 제목',
            content='원본 내용',
            author='작성자',
        )

    def test_edit_get_prefills_form(self):
        """GET 요청 시 기존 데이터가 폼에 채워져 있는지 확인"""
        response = self.client.get(reverse('board:edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '원본 제목')
        self.assertContains(response, '원본 내용')

    def test_edit_post_saves_and_redirects(self):
        """POST 요청 시 저장 후 상세 페이지로 리다이렉트되는지 확인"""
        response = self.client.post(
            reverse('board:edit', args=[self.post.pk]),
            {'title': '수정된 제목', 'content': '수정된 내용', 'author': '작성자'},
        )
        self.assertRedirects(response, reverse('board:detail', args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, '수정된 제목')

    def test_edit_invalid_post_stays_on_page(self):
        """유효하지 않은 POST 요청 시 수정 페이지에 머무르는지 확인"""
        response = self.client.post(
            reverse('board:edit', args=[self.post.pk]),
            {'title': '', 'content': '', 'author': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/write.html')
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, '원본 제목')

    def test_edit_nonexistent_post_returns_404(self):
        """존재하지 않는 게시글 수정 시 404를 반환하는지 확인"""
        response = self.client.get(reverse('board:edit', args=[9999]))
        self.assertEqual(response.status_code, 404)
