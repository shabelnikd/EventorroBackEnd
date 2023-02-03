from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from category.models import Category
from category.serializers import (CategoryListSerializer, )

class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryListSerializer

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    lookup_field = 'slug'



    
