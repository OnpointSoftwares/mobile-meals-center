from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='list'),
    path('<int:pk>/', views.RestaurantDetailView.as_view(), name='detail'),
    path('create/', views.RestaurantCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.RestaurantUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.RestaurantDeleteView.as_view(), name='delete'),
    path('dashboard/', views.RestaurantDashboardView.as_view(), name='dashboard'),
]
