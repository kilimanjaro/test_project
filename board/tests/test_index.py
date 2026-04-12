from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_index_returns_200(self):
        """랜딩페이지가 200 응답을 반환하는지 확인"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        """랜딩페이지가 index.html 템플릿을 사용하는지 확인"""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')
