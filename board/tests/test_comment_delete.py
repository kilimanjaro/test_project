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
