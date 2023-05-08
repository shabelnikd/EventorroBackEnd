from django.urls import path
from event import views

urlpatterns = [
    path('age_limits/', views.AgeLimitsListView.as_view()),
    path('audience/', views.AudienceListView.as_view()),
    path('locations/', views.LocationListView.as_view()),
]
