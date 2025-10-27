from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re


class UserForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise ValidationError("Username is required!")

        if len(username) < 5:
            raise ValidationError("Username must be over 5 characters long.")

        if len(username) > 20:
            raise ValidationError("Username is too long, must be under 20 characters.")

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Similar username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise ValidationError("Email is required!")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered!")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        is_match = re.fullmatch(pattern, password1)

        if not is_match:
            raise ValidationError(
                "Password must be minimum of 8 characters and include at least one uppercase letter, one lowercase letter, one number and one special character"
            )

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords don't match")

        return password2

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Username",
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm Password",
        }
