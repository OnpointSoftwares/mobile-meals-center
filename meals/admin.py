from django.contrib import admin
from .models import Meal, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'category', 'restaurant', 'created_at')
    search_fields = ('name', 'restaurant__name', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
