from django.test import TestCase
from board.models import Post, Comment


class PostModelTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='내용입니다',
            author='작성자',
        )

    def test_str(self):
        """__str__이 title을 반환하는지 확인"""
        self.assertEqual(str(self.post), '테스트 게시글')

    def test_default_views_is_zero(self):
        """views 기본값이 0인지 확인"""
        self.assertEqual(self.post.views, 0)

    def test_ordering_latest_first(self):
        """ordering이 -created_at 순인지 확인"""
        post2 = Post.objects.create(title='두번째 글', content='내용', author='작성자')
        posts = list(Post.objects.all())
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], self.post)

    def test_verbose_name(self):
        self.assertEqual(Post._meta.verbose_name, '게시글')
        self.assertEqual(Post._meta.verbose_name_plural, '게시글 목록')


class CommentModelTest(TestCase):
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

    def test_str(self):
        """__str__이 '게시글 제목 - 작성자' 형식인지 확인"""
        self.assertEqual(str(self.comment), '게시글 - 댓글작성자')

    def test_cascade_delete(self):
        """Post 삭제 시 관련 Comment도 삭제되는지 확인"""
        comment_pk = self.comment.pk
        self.post.delete()
        self.assertFalse(Comment.objects.filter(pk=comment_pk).exists())

    def test_ordering_oldest_first(self):
        """댓글 ordering이 created_at 오름차순인지 확인"""
        comment2 = Comment.objects.create(
            post=self.post,
            author='두번째댓글',
            content='두번째 내용',
        )
        comments = list(Comment.objects.filter(post=self.post))
        self.assertEqual(comments[0], self.comment)
        self.assertEqual(comments[1], comment2)

    def test_related_name(self):
        """post.comments로 역참조가 동작하는지 확인"""
        self.assertIn(self.comment, self.post.comments.all())

    def test_verbose_name(self):
        self.assertEqual(Comment._meta.verbose_name, '댓글')
        self.assertEqual(Comment._meta.verbose_name_plural, '댓글 목록')
