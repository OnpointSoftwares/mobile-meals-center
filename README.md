# Mobile Meals Center 🍕🍔🥘

A comprehensive food delivery platform built with Django and Bootstrap, featuring secure payment processing through Stripe.

## Features

### 🔐 **Authentication & User Management**
- Custom User model with restaurant/customer roles
- Secure registration and login system
- Role-based dashboards and permissions
- User profiles with location data

### 🏪 **Restaurant Management**
- Restaurant profile creation and management
- Menu management with full CRUD operations
- Image uploads for restaurant logos and meal photos
- Location-based restaurant discovery

### 🍽️ **Meal & Order System**
- Category-based meal organization
- Shopping cart functionality
- Order tracking and status updates
- Order history for customers and restaurants

### 💳 **Secure Payment Processing**
- **Stripe Integration** for secure payments
- Support for credit/debit cards
- Real-time payment processing
- Webhook handling for payment confirmations
- Payment failure handling and retry options

### 🎨 **Modern UI/UX**
- Bootstrap 5 responsive design
- Mobile-friendly interface
- Interactive animations and hover effects
- Clean, modern design with food-themed colors

## Tech Stack

- **Backend:** Django 5.0, Python 3.13
- **Frontend:** Bootstrap 5, JavaScript, HTML5/CSS3
- **Database:** SQLite (development), PostgreSQL ready
- **Payment:** Stripe Payment Processing
- **Forms:** Django Crispy Forms with Bootstrap 5
- **Media:** Django file handling for images

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd mobile_meals_center
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py migrate
python manage.py populate_data  # Creates sample data
```

### 3. Stripe Configuration

#### Get Your Stripe Keys
1. Sign up at [stripe.com](https://stripe.com)
2. Get your API keys from the Stripe Dashboard
3. For testing, use the test keys (they start with `pk_test_` and `sk_test_`)

#### Update Settings
Edit `config/settings.py` and replace the placeholder keys:

```python
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY = 'pk_test_your_actual_publishable_key_here'
STRIPE_SECRET_KEY = 'sk_test_your_actual_secret_key_here'
STRIPE_WEBHOOK_SECRET = 'whsec_your_webhook_secret_here'  # Optional for development
```

#### Environment Variables (Recommended)
For production, use environment variables:

```bash
export STRIPE_PUBLISHABLE_KEY='pk_live_your_live_publishable_key'
export STRIPE_SECRET_KEY='sk_live_your_live_secret_key'
export STRIPE_WEBHOOK_SECRET='whsec_your_webhook_secret'
```

Then update settings.py:
```python
import os
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_default')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_default')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_default')
```

### 4. Run the Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Test Accounts

The `populate_data` command creates these test accounts:

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full admin panel access

### Restaurant Accounts
- **Usernames:** `pizzapalace`, `burgerking`, `asiandelight`, `italianroma`, `mexicanfiesta`
- **Password:** `password123`
- **Features:** Can manage restaurant profiles and menus

### Customer Accounts
- **Usernames:** `customer1`, `customer2`, `customer3`
- **Password:** `password123`
- **Features:** Can browse meals, place orders, and make payments

## Stripe Testing

### Test Card Numbers
Use these test card numbers for development:

- **Successful Payment:** `4242424242424242`
- **Declined Payment:** `4000000000000002`
- **Insufficient Funds:** `4000000000009995`
- **Expired Card:** `4000000000000069`

**Test Details:**
- **Expiry:** Any future date (e.g., 12/25)
- **CVC:** Any 3 digits (e.g., 123)
- **ZIP:** Any 5 digits (e.g., 12345)

### Webhook Setup (Production)
1. In Stripe Dashboard, go to Webhooks
2. Add endpoint: `https://yourdomain.com/payments/webhook/`
3. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`
4. Copy the webhook secret to your settings

## Project Structure

```
mobile_meals_center/
├── accounts/          # User authentication and profiles
├── restaurants/       # Restaurant management
├── meals/            # Menu and meal management
├── orders/           # Order processing and cart
├── payments/         # Stripe payment integration
├── core/             # Homepage and search functionality
├── templates/        # HTML templates
├── static/           # CSS, JS, and images
├── media/            # User uploaded files
└── config/           # Django settings and main URLs
```

## Key Features Walkthrough

### 1. **Customer Journey**
1. Browse restaurants and meals on homepage
2. Search/filter meals by category, price, location
3. Add meals to shopping cart
4. Proceed to secure checkout
5. Complete payment with Stripe
6. Track order status in dashboard

### 2. **Restaurant Journey**
1. Register as restaurant owner
2. Create restaurant profile with logo and details
3. Add meals to menu with photos and pricing
4. Receive and manage incoming orders
5. Update order status (preparing, ready, delivered)
6. View sales analytics in dashboard

### 3. **Payment Flow**
1. Customer adds items to cart
2. Proceeds to checkout → creates order
3. Redirected to secure Stripe payment form
4. Payment processed in real-time
5. Success/failure handling with appropriate messaging
6. Order status updated automatically via webhooks

## Security Features

- **CSRF Protection:** All forms protected against CSRF attacks
- **User Authentication:** Secure login/logout with session management
- **Payment Security:** PCI-compliant payment processing via Stripe
- **Data Validation:** Server-side validation for all user inputs
- **SQL Injection Protection:** Django ORM prevents SQL injection
- **XSS Protection:** Template auto-escaping prevents XSS attacks

## Production Deployment

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
STRIPE_PUBLISHABLE_KEY=pk_live_your_key
STRIPE_SECRET_KEY=sk_live_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
```

### Static Files
```bash
python manage.py collectstatic
```

### Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

## API Endpoints

### Payment API
- `POST /payments/create-payment-intent/` - Create Stripe payment intent
- `GET /payments/process-payment/<order_id>/` - Payment form
- `GET /payments/payment-success/<payment_id>/` - Success page
- `GET /payments/payment-failed/<payment_id>/` - Failure page
- `POST /payments/webhook/` - Stripe webhook handler

### Order API
- `GET /orders/` - List user orders
- `POST /orders/add-to-cart/<meal_id>/` - Add item to cart
- `GET /orders/cart/` - View shopping cart
- `POST /orders/create/` - Create new order

## Support

For issues with:
- **Payment Processing:** Check Stripe Dashboard for transaction details
- **Order Issues:** Use Django admin panel to view order status
- **Technical Issues:** Check Django logs and error messages

## License

This project is built for educational and commercial use. Stripe integration requires a valid Stripe account and adherence to Stripe's terms of service.

---

**🚀 Your Mobile Meals Center is ready to serve delicious food with secure payments!**
