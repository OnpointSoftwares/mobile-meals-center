from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_restaurant(self):
        return self.user_type == 'restaurant'
    
    @property
    def is_customer(self):
        return self.user_type == 'customer'
