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

        # all_user_emails = User.objects.values("email")
        # emails = []

        # for user_email in all_user_emails:
        #     emails.append(user_email["email"])

        # if email in emails:
        #     raise ValidationError("Email already registered!")

        if not email:
            raise ValidationError("Email is required!")

        # better way:
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered!")

        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        is_match = re.fullmatch(pattern, password)

        if not is_match:
            raise ValidationError(
                "Password must be minimum of 8 characters and include at least one uppercase letter, one lowercase letter, one number and one special character"
            )

        return password

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Username",
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm Password",
        }
