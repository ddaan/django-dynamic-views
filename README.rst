=============================
django-dynamic-views
=============================

.. image:: https://badge.fury.io/py/django-dynamic-views.png
    :target: https://badge.fury.io/py/django-dynamic-views

.. image:: https://travis-ci.org/ddaan/django-dynamic-views.png?branch=master
    :target: https://travis-ci.org/ddaan/django-dynamic-views

Provides out of the box CRUD functionality including templates and gives you the ability to build your screen top-down.

Documentation
-------------

The full documentation is at https://django-dynamic-views.readthedocs.org.

Quickstart
----------

Install django-dynamic-views::

    pip install django-dynamic-views

Then use it in a project::

    import django_dynamic_views


```
pip install django-dynamic-views
```

Add django-dynamic-views to installed apps



Example
=====================

models.py
---------

::

    class Article(models.Model):
        name = models.Charfield(max_length=200)
        description = models.Charfield(max_length=200)

views.py
--------
::

    class ArticleCRUDView(dynamicviews.DynamicCRUDView):
        model = Article

urls.py
-------
::

    urlpatterns += ArticleCRUDView.urls()

You'll point your browser to /article/list/ and a basic list with Create / Read / Update and Delete
buttons will be displayed.

So on the background it will create the following urls::

    /article/list/
    /article/create/
    /article/(?P<pk>[-\w]+)/update/
    /article/(?P<pk>[-\w]+)/read/
    /article/(?P<pk>[-\w]+)/delete/

If you don't care for some of the urls you can modfiy the _links_ atribute on the CrudView::

    class ArticleCRUDView(dynamicviews.DynamicCRUDView):
        model = Article
        links = ['list', 'read']

This will result in the following urls::

    /article/list/
    /article/(?P<pk>[-\w]+)/read/

So this will give you a basic list with a Read button next to it.

## Override the default classes
You can define which class the CRUD uses, so you can easily modify it's appearance and behaviour

::

    class ArticleDetailView(DetailView):
        template_name = 'articles/article_detail.html'


    class ArticleCRUDView(dynamicviews.DynamicCRUDView):
        model = Article
        links = ['list', 'read']
        read_class = ArticleDetail



Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
