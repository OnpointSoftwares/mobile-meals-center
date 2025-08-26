from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-payment-intent/', views.CreatePaymentIntentView.as_view(), name='create_payment_intent'),
    path('process-payment/<uuid:order_id>/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('payment-success/<uuid:payment_id>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment-failed/<uuid:payment_id>/', views.PaymentFailedView.as_view(), name='payment_failed'),
    path('webhook/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
]
