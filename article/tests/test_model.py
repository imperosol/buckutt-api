from datetime import timedelta

from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.test import TestCase
from django.utils.timezone import now

from article.models import Article, Foundation, Period, Price


class ArticleTestCase(TestCase):
    def test_something(self):
        print(Article.objects.all())
        self.assertEqual(True, True)


class PriceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article = Article.objects.first()
        cls.group = Group.objects.first()
        cls.foundation = Foundation.objects.first()
        cls.period = Period.objects.create(start=now(), end=now() + timedelta(days=1))

    def test_cannot_duplicate(self):
        """
        Test qu'on ne peut pas avoir deux prix pour un même article,
        une même période, une même fondation et un même groupe
        :return:
        """
        Price.objects.create(
            article=self.article,
            group=self.group,
            foundation=self.foundation,
            amount=1,
            period=self.period,
        )
        with self.assertRaises(IntegrityError):
            Price.objects.create(
                article=self.article,
                group=self.group,
                foundation=self.foundation,
                amount=2,
                period=self.period,
            )
