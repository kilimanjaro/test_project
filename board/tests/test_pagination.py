from django.test import TestCase
from django.urls import reverse
from board.models import Post


class PaginationTest(TestCase):
    def setUp(self):
        for i in range(1, 16):
            Post.objects.create(title=f'게시글 {i}', content='내용', author='작성자')

    def test_first_page_shows_10_posts(self):
        """1페이지에 게시글 10개가 표시되는지 확인"""
        response = self.client.get(reverse('board:list'))
        self.assertEqual(len(response.context['posts']), 10)

    def test_second_page_shows_remaining_posts(self):
        """2페이지에 나머지 게시글이 표시되는지 확인"""
        response = self.client.get(reverse('board:list') + '?page=2')
        self.assertEqual(len(response.context['posts']), 5)

    def test_page_navigation_visible(self):
        """페이지 버튼이 화면에 표시되는지 확인"""
        response = self.client.get(reverse('board:list'))
        self.assertContains(response, 'page=2')
