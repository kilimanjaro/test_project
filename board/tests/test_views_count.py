from django.test import TestCase
from django.urls import reverse
from board.models import Post


class ViewsCountTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='조회수 테스트 글',
            content='내용',
            author='작성자',
        )

    def test_initial_views_is_zero(self):
        """게시글 생성 시 조회수 초기값이 0인지 확인"""
        self.assertEqual(self.post.views, 0)

    def test_views_increase_on_detail(self):
        """상세 페이지 접근 시 조회수가 1 증가하는지 확인"""
        self.client.get(reverse('board:detail', args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

    def test_views_increase_multiple(self):
        """여러 번 접근 시 조회수가 누적되는지 확인"""
        for _ in range(5):
            self.client.get(reverse('board:detail', args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 5)
