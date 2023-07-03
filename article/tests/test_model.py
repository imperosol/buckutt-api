from django.test import TestCase

from article.models import Article


class ArticleTestCase(TestCase):
    def test_something(self):
        print(Article.objects.all())
        self.assertEqual(True, True)
