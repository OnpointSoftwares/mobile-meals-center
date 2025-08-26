from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Restaurant
from .forms import RestaurantForm
from meals.models import Meal
from orders.models import Order


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/list.html'
    context_object_name = 'restaurants'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Restaurant.objects.filter(is_active=True)
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            ).distinct()
        
        return queryset.order_by('-created_at')


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = self.object.meals.filter(is_available=True)
        return context


class RestaurantCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'restaurants/create.html'
    success_url = reverse_lazy('restaurants:dashboard')
    
    def test_func(self):
        return self.request.user.is_restaurant
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Restaurant profile created successfully!')
        return super().form_valid(form)


class RestaurantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'restaurants/edit.html'
    success_url = reverse_lazy('restaurants:dashboard')
    
    def test_func(self):
        restaurant = self.get_object()
        return self.request.user == restaurant.owner
    
    def form_valid(self, form):
        messages.success(self.request, 'Restaurant profile updated successfully!')
        return super().form_valid(form)


class RestaurantDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'restaurants/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_restaurant
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            restaurant = self.request.user.restaurant
            context['restaurant'] = restaurant
            context['meals'] = restaurant.meals.all()[:5]
            context['recent_orders'] = Order.objects.filter(restaurant=restaurant)[:10]
            context['total_orders'] = Order.objects.filter(restaurant=restaurant).count()
            context['pending_orders'] = Order.objects.filter(
                restaurant=restaurant, status='pending'
            ).count()
            context['total_meals'] = restaurant.meals.count()
        except Restaurant.DoesNotExist:
            context['needs_restaurant_profile'] = True
        return context
