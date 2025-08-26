from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.MealListView.as_view(), name='list'),
    path('<int:pk>/', views.MealDetailView.as_view(), name='detail'),
    path('create/', views.MealCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.MealUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.MealDeleteView.as_view(), name='delete'),
]
