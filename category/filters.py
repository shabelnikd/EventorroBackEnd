from django_filters import rest_framework as filters
from .models import Category

class CategoryFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['search']