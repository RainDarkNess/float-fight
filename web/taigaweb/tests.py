import datetime

from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Article


class ArticleTests(APITestCase):
    def setUp(self):
        self.task = Article.objects.create(label="Тест статьи", body="Тестовое описание",
                                           datePublish=datetime.datetime.now(), author='test')

    def test_create_task(self):
        url = reverse('article-create')
        data = {
            'label': 'Тест статьи',
            'body': 'Тестовое описание',
            'datePublish': datetime.datetime.now(),
            'author': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Article.objects.count(), 2)
        self.assertEqual(Article.objects.get(id=response.data['id']).label, 'Тест статьи')

    def test_get_task_list(self):
        url = reverse('article-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_task_detail(self):
        url = reverse('article-list', args=[self.task.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], self.task.label)

    def test_update_task(self):
        url = reverse('article-list', args=[self.task.id])
        data = {'label': 'Updated Task', 'body': 'Updated Description', 'datePublish': datetime.datetime.now(),
                'author': 'test author'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.label, 'Updated Task')

    def test_delete_task(self):
        url = reverse('article-list', args=[self.task.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)
