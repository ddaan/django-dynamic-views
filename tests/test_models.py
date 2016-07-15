#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-dynamic-views
------------

Tests for `django-dynamic-views` models module.
"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from example.simple_django_app.models import Author, Genre, Book


class TestDjango_dynamic_views(TestCase):

    def setUp(self):
        self.author_a = Author.objects.create(name='Joe')
        self.author_b = Author.objects.create(name='Joe')
        self.genre_a = Genre.objects.create(name='SciFy')
        self.genre_b = Genre.objects.create(name='SciFy')
        self.book_a = Book.objects.create(author=self.author_a, genre=self.genre_a, title='Book 1', pages=100)
        self.book_b = Book.objects.create(author=self.author_a, genre=self.genre_a, title='Book 2', pages=200)
        self.book_c = Book.objects.create(author=self.author_b, genre=self.genre_a, title='Book 3', pages=300)
        self.book_d = Book.objects.create(author=self.author_b, genre=self.genre_b, title='Book 4', pages=100)

    def test_book_list(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def test_book_create(self):
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)

    def test_book_read(self):
        response = self.client.get(reverse('book_read', kwargs={'pk': self.book_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_book_update(self):
        response = self.client.get(reverse('book_update', kwargs={'pk': self.book_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_author_list(self):
        response = self.client.get(reverse('author_list'))
        self.assertEqual(response.status_code, 200)

    def test_author_update(self):
        response = self.client.get(reverse('author_update', kwargs={'pk': self.author_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_author_read(self):
        response = self.client.get(reverse('author_read', kwargs={'pk': self.author_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_author_delete(self):
        response = self.client.get(reverse('author_delete', kwargs={'pk': self.author_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_author_create(self):
        response = self.client.get(reverse('author_create'))
        self.assertEqual(response.status_code, 200)

    def test_genre_list(self):
        response = self.client.get(reverse('genre_list'))
        self.assertEqual(response.status_code, 200)

    def test_genre_update(self):
        response = self.client.get(reverse('genre_update', kwargs={'pk': self.genre_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_genre_read(self):
        response = self.client.get(reverse('genre_read', kwargs={'pk': self.genre_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_genre_delete(self):
        response = self.client.get(reverse('genre_delete', kwargs={'pk': self.genre_a.pk}))
        self.assertEqual(response.status_code, 200)

    def test_genre_create(self):
        response = self.client.get(reverse('genre_create'))
        self.assertEqual(response.status_code, 200)

    def test_book_urls(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
