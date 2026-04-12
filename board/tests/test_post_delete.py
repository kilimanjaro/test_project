from django.test import TestCase
from django.urls import reverse
from board.models import Post


class PostDeleteTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='삭제할 게시글',
            content='내용',
            author='작성자',
        )

    def test_delete_get_shows_confirm(self):
        """GET 요청 시 삭제 확인 페이지가 표시되는지 확인"""
        response = self.client.get(reverse('board:delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_removes_and_redirects(self):
        """POST 요청 시 게시글 삭제 후 목록으로 리다이렉트되는지 확인"""
        response = self.client.post(reverse('board:delete', args=[self.post.pk]))
        self.assertRedirects(response, reverse('board:list'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_delete_get_does_not_delete(self):
        """GET 요청으로는 실제 삭제가 일어나지 않는지 확인"""
        self.client.get(reverse('board:delete', args=[self.post.pk]))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_delete_nonexistent_post_returns_404(self):
        """존재하지 않는 게시글 삭제 시 404를 반환하는지 확인"""
        response = self.client.post(reverse('board:delete', args=[9999]))
        self.assertEqual(response.status_code, 404)
