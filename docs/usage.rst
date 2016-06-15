========
Usage
========

To use django-dynamic-views in a project::

    import django_dynamic_views

As it's possibe to override a lot of the standard behviour on a view and template level we start with an easy example.
It will use the easiest template and view code possible:

**Models**

We assume the following models:

.. code-block:: python

    class Category(models.Model):
        name = models.CharField(max_length=200)

    class Blog(models.Model):
        category = models.ForeignKey(Category, related_name='blog_items')
        author = models.CharField(max_length=200)
        title = models.TextField()
        body = models.TextField()
        date_published = models.DateTimeField()

**Views**

The easiest view without create, edit and delete links would be:

.. code-block:: python

    class BlogList(LoginRequiredMixin, DynamicListView):
        model = Blog

        title = 'Blog items'
        field_names = ['title', 'body', 'author', 'category', 'date_published']
        order_fields = ['title', 'body', 'author', 'category', 'date_published']
        search_fields = ['title', 'body', 'author', 'category', 'date_published']

This would be sufficient for a 5 column ListView with searchable and orderable data. If you need translation or you want
better column names you can add them with:

.. code-block:: python

    verbose_names = {
        'title': 'Blog post title',
        'body': 'Blog post content',
        'author': 'Author',
        'category': 'Category',
        'date_published': 'Published on'
    }

Often it's handy to have a filter, in this case a filter on author and category would be easy, then the user can easily
show only blog posts of a certain author and/or category:

.. code-block:: python

    filter_fields = (
        ('author', 'author'),
        ('category__pk', 'category__name'),
    )

If you want to use the extra functionality as available in in the DynamicAdminListView you only have to provide the
extra attributes for building the links to detail, delete and edit functionality. An complete example with al prior code
in one block and some extra code showing how to set context_object_name, call extra methods on each field before
displaying and set an icon:

.. code-block:: python

    from django.contrib.humanize.templatetags.humanize import naturalday

    class BlogList(LoginRequiredMixin, DynamicAdminListView):
        model = Blog
        title = 'Blog items'
        icon = 'newspaper'  # use name that exists in font awesome icon set

        field_names = ['title', 'body', 'author', 'category', 'date_published']
        order_fields = ['title', 'body', 'author', 'category', 'date_published']
        search_fields = ['title', 'body', 'author', 'category', 'date_published']

        verbose_names = {
            'title': 'Blog post title',
            'body': 'Blog post content',
            'author': 'Author',
            'category': 'Category',
            'date_published': 'Published on'
        }

        filter_fields = (
            ('author', 'author'),
            ('category__pk', 'category__name'),
        )

        context_object_name = 'blog_items'

        detail_link = 'blogs:blog-detail'
        edit_link = 'blogs:blog-edit'
        delete_link = 'blogs:blog-delete'

        def convert_to_human_datetime_format(self, date):
            value = None
            if isinstance(date, datetime):
                value = formats.date_format(date, settings.DATETIME_FORMAT)

            return value

**Templates**

The most simple use cases will be handled for you by the default list templates: 'base_list.html' and
'base_admin_list.html'.


However, if you want or need to change the visual representation of a field, row or other aspects of
the list are rendered you can override on a couple of places.

To override a complete row you can use the folowwing example. First add this to the view:

.. code-block:: python

    template_name = 'blogs/blog_list.html'

Now define youw own template with:

.. code-block:: django

    {% extends "base.html" %}

    {% block list-row %}
        <td>
            <a href="{% url "blogs:blog-detail" object.id %}">{{ object.title }}</a>
        </td>
        <td>
            {{ object.body|safe }}
        </td>
        <td>
            {{ object.author }}
        </td>
        <td>
            {% if object.category %}
                {{ object.category }}
            {% else %}
                No category selected
            {% endif %}
        </td>
        <td>
            {{ object.date_published }}
        </td>
    {% endblock %}

