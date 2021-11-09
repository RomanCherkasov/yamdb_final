import django_filters
from django_filters.filters import CharFilter, NumberFilter
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')
    name = CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
