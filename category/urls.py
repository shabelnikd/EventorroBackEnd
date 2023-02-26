from django.urls import path
from category.views import (CategoryListView, CategoryDetailView)
urlpatterns = [
    path('', CategoryListView.as_view()),
    path('<str:slug>/', CategoryDetailView().as_view()),
]
