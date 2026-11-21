from django import forms
from .models import Category


ORDERING_CHOICES = [
    ('', 'Default'),
    ('price', 'Price: Low to High'),
    ('-price', 'Price: High to Low'),
    ('title', 'Name: A to Z'),
    ('-title', 'Name: Z to A'),
]


class ProductFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search", widget=forms.TextInput(
        attrs={'placeholder': 'Search products...'}))
    category = forms.ModelChoiceField(
        required=False, queryset=Category.objects.all(), empty_label="All categories")
    min_price = forms.DecimalField(required=False, min_value=0, label="Min price")
    max_price = forms.DecimalField(required=False, min_value=0, label="Max price")
    ordering = forms.ChoiceField(required=False, choices=ORDERING_CHOICES)
