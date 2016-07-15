from django_dynamic_views.views import DynamicListView, DynamicCRUDView, DynamicUpdateView, DynamicCreateView
from .models import Book, Genre, Author


class BookCRUD(DynamicCRUDView):
    """
    Simple django admin like class
    """
    model = Book
    field_names = ['title', 'description', 'author', 'genre', 'pages']
    links = ['list', 'create', 'read', 'update']
    paginate_by = 5


class GenreCRUD(DynamicCRUDView):
    model = Genre
    field_names = ['name']


class AuthorCRUD(DynamicCRUDView):
    model = Author
    field_names = ['name']


class BookFilterList(DynamicListView):
    model = Book
    field_names = ['title', 'description', 'author', 'genre', 'pages']
    verbose_names = {'title': 'title',
                     'description': 'description',
                     'author': 'author',
                     'genre': 'genre',
                     'pages': 'pages',
                     'author__name': 'Author name',
                     'genre__name': 'Genre name'}
    filter_fields = (('author__pk', 'author__name'), ('genre__pk', 'genre__name'))
    search_fields = ['title', 'description', 'author__name']


class UpdateBookView(DynamicUpdateView):
    model = Book
    field_names = ['name', 'description']


class CreateBookView(DynamicCreateView):
    model = Book
    field_names = ['name', 'description']
