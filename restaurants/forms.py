from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Restaurant


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'logo', 'phone', 'address', 'latitude', 'longitude']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            'logo',
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address',
            Row(
                Column('latitude', css_class='form-group col-md-6 mb-0'),
                Column('longitude', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Restaurant', css_class='btn btn-primary')
        )
