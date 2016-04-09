from django_dynamic_views.views import DynamicListView, DynamicCRUDView, DynamicUpdateView, DynamicCreateView
from models import Foo


class FooCRUD(DynamicCRUDView):
    """
    Simple django admin like class
    """
    model = Foo
    field_names = ['name', 'description']


class FooList(DynamicListView):
    model = Foo
    field_names = ['name', 'description']


class AdminFooList(FooList):
    update_link = 'foo-update'
    create_link = 'foo-create'
    delete_link = 'foo-delete'
    detail_link = 'foo-detail'


class UpdateFooView(DynamicUpdateView):
    model = Foo
    field_names = ['name', 'description']


class AdminFooListClass(FooList):
    update_class = UpdateFooView
    create_link = 'foo-create'
    delete_link = 'foo-delete'
    detail_link = 'foo-detail'


class CreateFooView(DynamicCreateView):
    model = Foo
    field_names = ['name', 'description']
