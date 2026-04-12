from django.test import TestCase
from django.urls import reverse
from board.models import Post, Comment


class CommentWriteTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='게시글',
            content='내용',
            author='작성자',
        )
        self.url = reverse('board:comment_write', args=[self.post.pk])

    def test_comment_write_creates_and_redirects(self):
        """유효한 POST 요청 시 댓글이 생성되고 상세 페이지로 리다이렉트되는지 확인"""
        response = self.client.post(self.url, {
            'author': '댓글작성자',
            'content': '댓글 내용',
        })
        self.assertRedirects(response, reverse('board:detail', args=[self.post.pk]))
        self.assertEqual(Comment.objects.filter(post=self.post).count(), 1)

    def test_comment_write_links_to_correct_post(self):
        """생성된 댓글이 올바른 게시글에 연결되는지 확인"""
        self.client.post(self.url, {'author': '댓글작성자', 'content': '댓글 내용'})
        comment = Comment.objects.get(post=self.post)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, '댓글작성자')

    def test_comment_write_invalid_form_does_not_save(self):
        """유효하지 않은 POST 요청 시 댓글이 저장되지 않는지 확인"""
        self.client.post(self.url, {'author': '', 'content': ''})
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_write_invalid_still_redirects(self):
        """유효하지 않은 POST여도 상세 페이지로 리다이렉트되는지 확인"""
        response = self.client.post(self.url, {'author': '', 'content': ''})
        self.assertRedirects(response, reverse('board:detail', args=[self.post.pk]))

    def test_comment_write_on_nonexistent_post_returns_404(self):
        """존재하지 않는 게시글에 댓글 작성 시 404를 반환하는지 확인"""
        response = self.client.post(
            reverse('board:comment_write', args=[9999]),
            {'author': '댓글작성자', 'content': '댓글 내용'},
        )
        self.assertEqual(response.status_code, 404)
