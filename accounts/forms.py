from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import CustomUser, egyptian_phone_validator


class RegistrationForm(UserCreationForm):
    """
    Registration form: first name, last name, email, password, confirm
    password, mobile phone. Email uniqueness and Egyptian phone format
    are validated here (in addition to the model-level validation).
    """
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    mobile_phone = forms.CharField(
        max_length=11,
        required=True,
        validators=[egyptian_phone_validator],
        help_text="Egyptian mobile number, e.g. 01012345678",
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'mobile_phone',
                   'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # auto-fill required username
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobile_phone = self.cleaned_data['mobile_phone']
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    """Simple login form using email + password."""
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
