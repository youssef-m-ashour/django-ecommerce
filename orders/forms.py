from django import forms


class ShippingForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
