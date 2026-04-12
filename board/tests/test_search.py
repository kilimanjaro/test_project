from django.test import TestCase
from django.urls import reverse
from board.models import Post


class SearchTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Django 튜토리얼', content='파이썬 웹 프레임워크', author='작성자')
        Post.objects.create(title='파이썬 기초', content='Django로 게시판 만들기', author='작성자')
        Post.objects.create(title='무관한 글', content='전혀 다른 내용', author='작성자')

    def test_search_by_title(self):
        """제목 키워드로 검색 시 결과가 반환되는지 확인 (제목+내용 OR 검색)"""
        response = self.client.get(reverse('board:list') + '?q=Django')
        # 'Django 튜토리얼'(제목) + '파이썬 기초'(내용에 'Django로' 포함) = 2개
        self.assertEqual(len(response.context['posts']), 2)
        self.assertContains(response, 'Django 튜토리얼')

    def test_search_by_content(self):
        """내용 키워드로 검색 시 결과가 반환되는지 확인"""
        response = self.client.get(reverse('board:list') + '?q=Django로')
        self.assertContains(response, '파이썬 기초')

    def test_search_no_result(self):
        """검색 결과 없을 때 빈 목록이 표시되는지 확인"""
        response = self.client.get(reverse('board:list') + '?q=없는키워드xyz')
        self.assertEqual(len(response.context['posts']), 0)

    def test_search_preserves_query_in_pagination(self):
        """검색 결과가 2페이지 이상일 때 페이지 URL에 검색어가 유지되는지 확인"""
        # 'keyword' 가 제목에 포함된 게시글 15개 추가
        for i in range(15):
            Post.objects.create(title=f'keyword 게시글 {i}', content='내용', author='작성자')
        response = self.client.get(reverse('board:list') + '?q=keyword')
        self.assertContains(response, 'q=keyword')
