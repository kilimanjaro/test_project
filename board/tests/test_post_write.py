from django.test import TestCase
from django.urls import reverse
from board.models import Post


class PostWriteTest(TestCase):
    def test_write_get_returns_200(self):
        """GET 요청 시 글 작성 페이지가 200을 반환하는지 확인"""
        response = self.client.get(reverse('board:write'))
        self.assertEqual(response.status_code, 200)

    def test_write_get_uses_correct_template(self):
        """GET 요청 시 write.html 템플릿을 사용하는지 확인"""
        response = self.client.get(reverse('board:write'))
        self.assertTemplateUsed(response, 'board/write.html')

    def test_write_post_creates_post_and_redirects(self):
        """유효한 POST 요청 시 게시글이 생성되고 목록으로 리다이렉트되는지 확인"""
        response = self.client.post(reverse('board:write'), {
            'title': '새 게시글',
            'content': '새 내용',
            'author': '작성자',
        })
        self.assertRedirects(response, reverse('board:list'))
        self.assertTrue(Post.objects.filter(title='새 게시글').exists())

    def test_write_post_invalid_form_stays_on_page(self):
        """유효하지 않은 POST 요청 시 작성 페이지에 머무르는지 확인"""
        response = self.client.post(reverse('board:write'), {
            'title': '',
            'content': '내용',
            'author': '작성자',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/write.html')
        self.assertEqual(Post.objects.count(), 0)

    def test_write_post_invalid_form_shows_errors(self):
        """유효하지 않은 POST 시 폼 에러가 컨텍스트에 포함되는지 확인"""
        response = self.client.post(reverse('board:write'), {
            'title': '',
            'content': '',
            'author': '',
        })
        self.assertFalse(response.context['form'].is_valid())
