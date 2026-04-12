from django.test import TestCase
from django.urls import reverse
from board.models import Post, Comment


class CommentDeleteTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='게시글',
            content='내용',
            author='작성자',
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author='댓글작성자',
            content='댓글 내용',
        )

    def test_comment_delete_removes_and_redirects(self):
        """댓글 삭제 후 해당 게시글 상세 페이지로 리다이렉트되는지 확인"""
        response = self.client.post(
            reverse('board:comment_delete', args=[self.comment.pk])
        )
        self.assertRedirects(response, reverse('board:detail', args=[self.post.pk]))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_comment_delete_get_does_not_delete(self):
        """GET 요청으로는 댓글이 삭제되지 않는지 확인"""
        self.client.get(reverse('board:comment_delete', args=[self.comment.pk]))
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_comment_delete_nonexistent_returns_404(self):
        """존재하지 않는 댓글 삭제 시 404를 반환하는지 확인"""
        response = self.client.post(reverse('board:comment_delete', args=[9999]))
        self.assertEqual(response.status_code, 404)
