from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.db.models.deletion import Collector
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

class DynamicListView(ListView):
    template_name = 'django_dynamic_views/dynamic_list_view.html'
    ajax_template_name = None
    field_names = None
    order_fields = None
    verbose_names = None
    convert_field_values = None
    search_fields = None
    filter_fields = None
    annotate_fields = None
    prefetch_related = []
    distinct = True

    def get_ajax_template_name(self):
        """
        Hook for returning the ajax template.

        Returns self.ajax_template_name if it exists, else the normal template.

        :return:
        """
        if self.ajax_template_name:
            return self.ajax_template_name

        return super(DynamicListView, self).get_template_names()

    def get_template_names(self):
        """
        When a request is made with AJAX, it returns the ajax_template_name
        Else the normal listview behaviour

        :return:
        """
        if self.request.is_ajax():
            return self.get_ajax_template_name()
        return super(DynamicListView, self).get_template_names()

    def get_field_names(self):
        """
        Return the field names defined in field_names attribute.
        If field_names does not exists, automatically get all the field names in the model

        :return: list of fieldnames
        """
        if self.field_names:
            return self.field_names
        return []

    def get_convert_field_values(self):
        """
        Dict with methods to be called on the view to convert a certain value

        :return: method name
        """
        if self.convert_field_values:
            return self.convert_field_values
        else:
            return {}

    def get_order_fields(self):
        """
        Return the field names defined in order_fields attribute.

        All the field that a user can order on. If not specified it returns all
         the fields that are defined in get_field_names that are present in
         the model.

        :return: list of field names
        """
        if self.order_fields:
            return self.order_fields
        return []

    def get_field_verbose_names(self):
        """
        Returns a dict with the verbose name of a field.
        E.g.:
        { 'name': _("Name"), 'max_value': _("Maximum value") }

        :return: dict with field -> verbose name mapping
        """
        if self.verbose_names:
            return self.verbose_names
        else:
            field_verbose_names = {}
            for name in self.get_field_names():
                field_verbose_names[name] = name

            return field_verbose_names

    def get_search_fields(self):
        """
        Hook to returns all the fields where can be searched in. The fields shall
        be suffixed with __icontains in the query

        :return: All the field where can be searched in
        """
        if self.search_fields:
            return self.search_fields
        else:
            return False

    @property
    def get_paginate_url(self):
        """
        The url it should paginate on. By default an empty string

        :return: string url
        """
        return ''

    def get_paginate_by(self, queryset):
        """
        Returns the numbers of pages per page in the list.
        First tries the GET parameter, then the session(userpreference), then the value defined
        in the class attribute

        :return:
        """

        return self.request.GET.get('paginate_by', self.request.session.get('paginate_by', self.paginate_by))

    @property
    def search_phrase(self):
        """
        Propery method to determine the search phrase.

        :return: string search phrase
        """
        if self.request.GET.get('search_phrase') or self.request.GET.get('search_phrase') == '':
            return self.request.GET.get('search_phrase')

        return ''

    def add_queryset_search(self, queryset):
        """
        Modifies the query set with the search parameter.
        Creates an OR filter argument for every self.search_fields with the searchphrase.

        :param queryset: current queryset
        :return: modified queryset
        """
        if self.search_phrase:
            queries = [Q(**{'{}__{}'.format(search_field, 'icontains'): self.search_phrase}) for search_field in
                       self.get_search_fields()]

            # Set up the query
            query = Q()

            # Or the Q object with the ones remaining in the list
            for item in queries:
                query |= item

            queryset = queryset.filter(query)

        return queryset

    @property
    def order_by(self):
        """
        Propery method to determine the order by.
        First check if it is used in the url, then retrieve the user setting and else it is an empty string

        :return: string order by
        """
        order_by = self.request.GET.get('order_by', None)
        if order_by in self.get_field_names():
            if order_by in self.get_order_fields():
                if self.request.GET.get('sort') == 'DESC':
                    return '-%s' % order_by
                else:
                    return order_by

        return ''

    def add_queryset_ordering(self, query_set):
        """
        Sets the ordering on a query.

        :param query_set:
        :return: modified queryset
        """
        if self.order_by:
            return query_set.order_by(self.order_by)
        else:
            return query_set

    def get_filter_fields(self):
        """
        Hook to determine the filter fields.  The format it expects
        is requires a tuple dict. The first argument is the key used in the database
        and to be used for grouping, the other is the name the user sees in the UI

        *Example*

        ::

            (
                ('category__pk', 'category__name'),
                ('author__pk', 'author__name'),
            )

        """
        return self.filter_fields or []

    def get_filter_values(self):
        """
        Queries the database for the values that shall be used in the filtering dropdowns

        :returns list with tuples with the first argument the filter key and the second the value used for
        displaying in the UI
        """
        filter_values = []

        for filter_key, filter_name in self.get_filter_fields():
            values = [(o[filter_key], o[filter_name]) for o in
                      self.get_queryset().values(filter_key, filter_name).distinct(filter_key).order_by(filter_key)]

            values.sort(key=lambda tup: tup[1])  # Sort on the filter_name

            filter_values.append(
                (filter_key, self.verbose_names.get(filter_name), values)
            )

        return filter_values

    @property
    def filter_kwargs(self):
        """
        Helper method to create the keyword arguments used in the queryset to actual filter the list
        """
        filter_kwargs = {}

        for filter_key, filter_name in self.get_filter_fields():
            filter_value = self.request.GET.get('filter-{}'.format(filter_key))
            if filter_value and filter_value != '---':
                filter_kwargs[filter_key] = str(filter_value)

        return filter_kwargs

    def add_queryset_filtering(self, queryset):
        """
        Modifies the queryset with the filtering of the queryset

        :param queryset:
        :returns modified queryset
        """

        if self.filter_kwargs:
            queryset = queryset.filter(**self.filter_kwargs)

        return queryset

    def add_queryset_annotating(self, queryset):
        if self.annotate_fields:
            queryset = queryset.annotate(**self.annotate_fields)

        return queryset

    def get_queryset(self):
        """
        Modifies the query set with all the magic this class contains
        We will add searching, ordering and filtering, as well add distinct and
        prefetch related to the queryset
        """
        queryset = super(DynamicListView, self).get_queryset()
        queryset = self.add_queryset_search(queryset)
        queryset = self.add_queryset_filtering(queryset)
        queryset = self.add_queryset_annotating(queryset)
        queryset = self.add_queryset_ordering(queryset)

        if self.distinct:
            queryset = queryset.distinct()

        if self.prefetch_related:
            queryset = queryset.prefetch_related(*self.prefetch_related)

        return queryset

    @staticmethod
    def nice_page_range(page_range, current_page):
        """
        Returns a page range

        :param page_range:
        :param current_page:
        :return:
        """
        display_around = 2
        if len(page_range) > display_around:
            start = 0 if current_page - display_around - 1 < 0 else current_page - display_around - 1
            end = None if current_page + display_around > len(page_range) else current_page + display_around
            page_range = page_range[start:end]

        return page_range

    def get_context_data(self, **kwargs):
        context = super(DynamicListView, self).get_context_data(**kwargs)
        context['field_names'] = self.get_field_names()
        context['field_verbose_names'] = self.get_field_verbose_names()
        context['order_fields'] = self.get_order_fields()
        context['convert_field_values'] = self.get_convert_field_values()
        context['filter_fields'] = self.get_filter_fields()
        context['filter_values'] = self.get_filter_values()
        context['filter_kwargs'] = self.filter_kwargs
        context['num_fields'] = len(self.get_field_names())
        context['paginate_url'] = self.get_paginate_url
        context['search'] = True if self.get_search_fields() else False
        context['search_phrase'] = self.search_phrase
        if context['paginator']:
            context['nice_page_range'] = self.nice_page_range(context['paginator'].page_range,
                                                              context['page_obj'].number)

        if self.order_by:
            context['order_by'] = self.order_by[1:] if self.order_by[0] == '-' else self.order_by
            context['sort'] = 'ASC' if self.order_by[0] == '-' else 'DESC'

        return context


class AdminDynamicListView(DynamicListView):
    template_name = 'django_dynamic_views/admin_dynamic_list_view.html'
    title = None
    update_link = None
    read_link = None
    create_link = None
    create_text = None
    delete_link = None
    extra_links = None

    def get_update_link(self):
        if self.update_link:
            return self.update_link
        else:
            return False

    def get_read_link(self):
        if self.read_link:
            return self.read_link
        else:
            return False

    def get_create_link(self):
        if self.create_link:
            return self.create_link
        else:
            return False

    def get_delete_link(self):
        if self.delete_link:
            return self.delete_link
        else:
            return False

    def get_extra_links(self):
        if self.extra_links:
            return self.extra_links
        else:
            return {}

    def get_title(self):
        if self.title:
            return self.title
        else:
            return ''

    def get_create_text(self):
        if self.create_text:
            return self.create_text
        else:
            return 'New'

    def get_context_data(self, **kwargs):
        context = super(AdminDynamicListView, self).get_context_data(**kwargs)
        context['update_link'] = self.get_update_link()
        context['read_link'] = self.get_read_link()
        context['delete_link'] = self.get_delete_link()
        context['create_link'] = self.get_create_link()
        context['extra_links'] = self.get_extra_links()
        context['title'] = self.get_title()
        context['create_text'] = self.get_create_text()
        return context


class DynamicReadView(DetailView):
    template_name = 'django_dynamic_views/dynamic_read_view.html'
    field_names = None
    verbose_names = None

    def get_field_names(self):
        """
        Return the field names defined in field_names attribute.

        :return: list of fieldnames
        """
        if self.field_names:
            return self.field_names
        return []

    def get_field_verbose_names(self):
        """
        Returns a dict with the verbose name of a field.
        E.g.:
        { 'name': _("Name"), 'max_value': _("Maximum value") }

        :return: dict with field -> verbose name mapping
        """
        if self.verbose_names:
            return self.verbose_names
        else:
            field_verbose_names = {}
            for name in self.get_field_names():
                field_verbose_names[name] = name

            return field_verbose_names

    def get_context_data(self, **kwargs):
        context = super(DynamicReadView, self).get_context_data(**kwargs)
        context['field_names'] = self.get_field_names()
        context['field_verbose_names'] = self.get_field_verbose_names()
        return context


class DynamicDeleteView(DeleteView):
    template_name = 'django_dynamic_views/dynamic_delete_form.html'

    def get_context_data(self, **kwargs):
        context = super(DynamicDeleteView, self).get_context_data(**kwargs)

        collector = Collector(using='default') # or specific database
        collector.collect([self.object])
        to_delete = collector.instances_with_model()
        context['to_delete_list'] = []

        for x, y in to_delete:
            context['to_delete_list'].append((x.__name__, y,))

        return context

class DynamicUpdateView(UpdateView):
    template_name = 'django_dynamic_views/dynamic_form.html'
    field_names = None

    @property
    def fields(self):
        return self.field_names


class DynamicCreateView(CreateView):
    template_name = 'django_dynamic_views/dynamic_form.html'
    field_names = None

    @property
    def fields(self):
        return self.field_names


class DynamicCRUDView(object):
    model = None
    links = ['list', 'update', 'read', 'delete', 'create']

    field_names = ['pk']
    verbose_names = None

    update_kwargs = 'pk'
    update_kwargs_regexp = '(?P<pk>[-\w]+)'
    read_kwargs = 'pk'
    read_kwargs_regexp = '(?P<pk>[-\w]+)'
    delete_kwargs = 'pk'
    delete_kwargs_regexp = '(?P<pk>[-\w]+)'

    def get_view_kwargs(self):
        return {'model': self.model}

    def get_list_view_kwargs(self):
        kwargs = self.get_view_kwargs()
        kwargs['field_names'] = self.field_names
        kwargs['verbose_names'] = self.verbose_names
        kwargs['update_link'] = self.link_name('update')
        kwargs['read_link'] = self.link_name('read')
        kwargs['create_link'] = self.link_name('create')
        kwargs['create_text'] = self.link_name('create')
        kwargs['delete_link'] = self.link_name('delete')
        return kwargs

    def get_read_view_kwargs(self):
        kwargs = self.get_view_kwargs()
        kwargs['field_names'] = self.field_names
        return kwargs

    def get_update_view_kwargs(self):
        kwargs = self.get_view_kwargs()
        kwargs['field_names'] = self.field_names
        kwargs['success_url'] = reverse_lazy(self.link_name('list'))
        return kwargs

    def get_create_view_kwargs(self):
        kwargs = self.get_view_kwargs()
        kwargs['field_names'] = self.field_names
        kwargs['success_url'] = reverse_lazy(self.link_name('list'))
        return kwargs

    def get_delete_view_kwargs(self):
        kwargs = self.get_view_kwargs()
        kwargs['success_url'] = reverse_lazy(self.link_name('list'))
        return kwargs

    @property
    def list_class(self):
        return AdminDynamicListView.as_view(**self.get_list_view_kwargs())

    @property
    def update_class(self):
        return DynamicUpdateView.as_view(**self.get_update_view_kwargs())

    @property
    def read_class(self):
        return DynamicReadView.as_view(**self.get_read_view_kwargs())

    @property
    def delete_class(self):
        return DynamicDeleteView.as_view(**self.get_delete_view_kwargs())

    @property
    def create_class(self):
        return DynamicCreateView.as_view(**self.get_create_view_kwargs())

    @property
    def model_name(self):
        return slugify(self.model.__name__)

    def link_name(self, link_name):
        return '{}_{}'.format(self.model_name, link_name)

    def urls(self):
        urls = []
        for link in self.links:
            if hasattr(self, '{}_link'.format(link)):
                link_name = getattr(self, '{}_link'.format(link))
            else:
                link_name = link

            url_check = r'{}/{}/'.format(self.model_name, link_name)

            if hasattr(self, '{}_kwargs'.format(link)):
                link_kwargs = getattr(self, '{}_kwargs_regexp'.format(link))
                url_check += '{}/'.format(link_kwargs)

            action_cls = getattr(self, '{}_class'.format(link))
            urls.append(url(url_check, action_cls, name=self.link_name(link)))

        return urls
