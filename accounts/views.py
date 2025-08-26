from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
from .forms import UserRegistrationForm, UserProfileForm
from restaurants.models import Restaurant
from orders.models import Order


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Registration successful!')
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_restaurant:
            try:
                restaurant = user.restaurant
                context['restaurant'] = restaurant
                context['recent_orders'] = Order.objects.filter(restaurant=restaurant)[:5]
                context['total_orders'] = Order.objects.filter(restaurant=restaurant).count()
                context['pending_orders'] = Order.objects.filter(
                    restaurant=restaurant, status='pending'
                ).count()
            except Restaurant.DoesNotExist:
                context['needs_restaurant_profile'] = True
        else:
            context['recent_orders'] = Order.objects.filter(customer=user)[:5]
            context['total_orders'] = Order.objects.filter(customer=user).count()
        
        return context
