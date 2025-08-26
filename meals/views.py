from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Meal, Category
from .forms import MealForm
from restaurants.models import Restaurant


class MealListView(ListView):
    model = Meal
    template_name = 'meals/list.html'
    context_object_name = 'meals'
    paginate_by = 12
    
    def get_queryset(self):
        return Meal.objects.filter(is_available=True)


class MealDetailView(DetailView):
    model = Meal
    template_name = 'meals/detail.html'
    context_object_name = 'meal'


class MealCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Meal
    form_class = MealForm
    template_name = 'meals/create.html'
    success_url = reverse_lazy('restaurants:dashboard')
    
    def test_func(self):
        return self.request.user.is_restaurant and hasattr(self.request.user, 'restaurant')
    
    def form_valid(self, form):
        form.instance.restaurant = self.request.user.restaurant
        messages.success(self.request, 'Meal created successfully!')
        return super().form_valid(form)


class MealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meal
    form_class = MealForm
    template_name = 'meals/edit.html'
    success_url = reverse_lazy('restaurants:dashboard')
    
    def test_func(self):
        meal = self.get_object()
        return self.request.user == meal.restaurant.owner
    
    def form_valid(self, form):
        messages.success(self.request, 'Meal updated successfully!')
        return super().form_valid(form)


class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meal
    template_name = 'meals/delete.html'
    success_url = reverse_lazy('restaurants:dashboard')
    
    def test_func(self):
        meal = self.get_object()
        return self.request.user == meal.restaurant.owner
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Meal deleted successfully!')
        return super().delete(request, *args, **kwargs)
