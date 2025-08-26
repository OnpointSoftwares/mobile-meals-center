from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Meal, Category


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'description', 'category', 'price', 'image', 'preparation_time', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('price', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'image',
            Row(
                Column('preparation_time', css_class='form-group col-md-6 mb-0'),
                Column('is_available', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Meal', css_class='btn btn-primary')
        )
