from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'phone', 'notes']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'delivery_address',
            'phone',
            'notes',
            Submit('submit', 'Place Order', css_class='btn btn-primary btn-lg w-100')
        )


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'status',
            Submit('submit', 'Update Status', css_class='btn btn-primary')
        )
