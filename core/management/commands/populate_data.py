from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import User
from restaurants.models import Restaurant
from meals.models import Meal, Category
from orders.models import Order, OrderItem
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Pizza', 'description': 'Delicious pizzas with various toppings'},
            {'name': 'Burgers', 'description': 'Juicy burgers and sandwiches'},
            {'name': 'Asian', 'description': 'Asian cuisine including Chinese, Thai, Japanese'},
            {'name': 'Italian', 'description': 'Authentic Italian dishes'},
            {'name': 'Mexican', 'description': 'Spicy Mexican food and tacos'},
            {'name': 'Desserts', 'description': 'Sweet treats and desserts'},
            {'name': 'Beverages', 'description': 'Drinks and beverages'},
            {'name': 'Healthy', 'description': 'Healthy and organic options'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create restaurant owners
        restaurant_users_data = [
            {'username': 'pizzapalace', 'email': 'owner@pizzapalace.com', 'first_name': 'Mario', 'last_name': 'Rossi'},
            {'username': 'burgerking', 'email': 'owner@burgerking.com', 'first_name': 'John', 'last_name': 'Smith'},
            {'username': 'asiandelight', 'email': 'owner@asiandelight.com', 'first_name': 'Li', 'last_name': 'Chen'},
            {'username': 'italianroma', 'email': 'owner@italianroma.com', 'first_name': 'Giuseppe', 'last_name': 'Verdi'},
            {'username': 'mexicanfiesta', 'email': 'owner@mexicanfiesta.com', 'first_name': 'Carlos', 'last_name': 'Rodriguez'},
        ]
        
        restaurant_users = []
        for user_data in restaurant_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'user_type': 'restaurant',
                    'phone': f'+1555{random.randint(1000000, 9999999)}',
                    'address': f'{random.randint(100, 999)} Main St, City',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created restaurant user: {user.username}')
            restaurant_users.append(user)
        
        # Create restaurants
        restaurants_data = [
            {'name': 'Pizza Palace', 'description': 'Authentic Italian pizzas made with fresh ingredients', 'owner_idx': 0},
            {'name': 'Burger Kingdom', 'description': 'Gourmet burgers and fries', 'owner_idx': 1},
            {'name': 'Asian Delight', 'description': 'Traditional Asian cuisine with modern twist', 'owner_idx': 2},
            {'name': 'Roma Italian', 'description': 'Family-owned Italian restaurant since 1985', 'owner_idx': 3},
            {'name': 'Mexican Fiesta', 'description': 'Authentic Mexican food and margaritas', 'owner_idx': 4},
        ]
        
        restaurants = []
        for rest_data in restaurants_data:
            restaurant, created = Restaurant.objects.get_or_create(
                name=rest_data['name'],
                defaults={
                    'owner': restaurant_users[rest_data['owner_idx']],
                    'description': rest_data['description'],
                    'phone': f'+1555{random.randint(1000000, 9999999)}',
                    'address': f'{random.randint(100, 999)} Restaurant Ave, City',
                    'latitude': Decimal(str(40.7128 + random.uniform(-0.1, 0.1))),
                    'longitude': Decimal(str(-74.0060 + random.uniform(-0.1, 0.1))),
                }
            )
            restaurants.append(restaurant)
            if created:
                self.stdout.write(f'Created restaurant: {restaurant.name}')
        
        # Create meals
        meals_data = [
            # Pizza Palace
            {'name': 'Margherita Pizza', 'description': 'Classic pizza with tomato, mozzarella, and basil', 'price': '18.99', 'category': 'Pizza', 'restaurant_idx': 0},
            {'name': 'Pepperoni Pizza', 'description': 'Traditional pepperoni pizza with extra cheese', 'price': '21.99', 'category': 'Pizza', 'restaurant_idx': 0},
            {'name': 'Quattro Stagioni', 'description': 'Four seasons pizza with mushrooms, ham, artichokes, and olives', 'price': '24.99', 'category': 'Pizza', 'restaurant_idx': 0},
            
            # Burger Kingdom
            {'name': 'Classic Cheeseburger', 'description': 'Beef patty with cheese, lettuce, tomato, and pickles', 'price': '12.99', 'category': 'Burgers', 'restaurant_idx': 1},
            {'name': 'BBQ Bacon Burger', 'description': 'Beef patty with BBQ sauce, bacon, and onion rings', 'price': '15.99', 'category': 'Burgers', 'restaurant_idx': 1},
            {'name': 'Veggie Burger', 'description': 'Plant-based patty with avocado and sprouts', 'price': '13.99', 'category': 'Healthy', 'restaurant_idx': 1},
            
            # Asian Delight
            {'name': 'Pad Thai', 'description': 'Traditional Thai stir-fried noodles with shrimp', 'price': '16.99', 'category': 'Asian', 'restaurant_idx': 2},
            {'name': 'Chicken Teriyaki', 'description': 'Grilled chicken with teriyaki sauce and rice', 'price': '14.99', 'category': 'Asian', 'restaurant_idx': 2},
            {'name': 'Vegetable Spring Rolls', 'description': 'Fresh spring rolls with peanut dipping sauce', 'price': '8.99', 'category': 'Asian', 'restaurant_idx': 2},
            
            # Roma Italian
            {'name': 'Spaghetti Carbonara', 'description': 'Classic carbonara with eggs, cheese, and pancetta', 'price': '19.99', 'category': 'Italian', 'restaurant_idx': 3},
            {'name': 'Chicken Parmigiana', 'description': 'Breaded chicken with marinara sauce and mozzarella', 'price': '22.99', 'category': 'Italian', 'restaurant_idx': 3},
            {'name': 'Tiramisu', 'description': 'Traditional Italian dessert with coffee and mascarpone', 'price': '7.99', 'category': 'Desserts', 'restaurant_idx': 3},
            
            # Mexican Fiesta
            {'name': 'Chicken Tacos', 'description': 'Three soft tacos with grilled chicken and salsa', 'price': '11.99', 'category': 'Mexican', 'restaurant_idx': 4},
            {'name': 'Beef Burrito', 'description': 'Large burrito with seasoned beef, rice, and beans', 'price': '13.99', 'category': 'Mexican', 'restaurant_idx': 4},
            {'name': 'Guacamole & Chips', 'description': 'Fresh guacamole with tortilla chips', 'price': '6.99', 'category': 'Mexican', 'restaurant_idx': 4},
        ]
        
        meals = []
        for meal_data in meals_data:
            category = Category.objects.get(name=meal_data['category'])
            meal, created = Meal.objects.get_or_create(
                name=meal_data['name'],
                restaurant=restaurants[meal_data['restaurant_idx']],
                defaults={
                    'description': meal_data['description'],
                    'price': Decimal(meal_data['price']),
                    'category': category,
                    'preparation_time': random.randint(15, 45),
                }
            )
            meals.append(meal)
            if created:
                self.stdout.write(f'Created meal: {meal.name}')
        
        # Create customer users
        customer_users_data = [
            {'username': 'customer1', 'email': 'customer1@example.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
            {'username': 'customer2', 'email': 'customer2@example.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
            {'username': 'customer3', 'email': 'customer3@example.com', 'first_name': 'Carol', 'last_name': 'Davis'},
        ]
        
        customer_users = []
        for user_data in customer_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'user_type': 'customer',
                    'phone': f'+1555{random.randint(1000000, 9999999)}',
                    'address': f'{random.randint(100, 999)} Customer St, City',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created customer user: {user.username}')
            customer_users.append(user)
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@mobilemeals.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'user_type': 'customer',
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user: admin')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('- Admin: admin / admin123')
        self.stdout.write('- Restaurant users: pizzapalace, burgerking, etc. / password123')
        self.stdout.write('- Customer users: customer1, customer2, customer3 / password123')
