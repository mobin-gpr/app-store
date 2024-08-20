from django import forms
from django.core import validators
from .models import User
from django.urls import reverse
from django.utils.html import format_html


class RegisterForm(forms.Form):
    """
    Form for user registration including username, password, confirmation password, and email.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "required": True, "id": "name"}
        ),
        validators=[
            validators.MinLengthValidator(4),
            validators.MaxLengthValidator(20),
            validators.RegexValidator(
                regex=r"^[a-zA-Z0-9_]*$",
                message="نام کاربری فقط می تواند شامل حروف، اعداد و زیرخط باشد.",
            ),
        ],
        label="نام کاربری",
        error_messages={
            "min_length": "طول نام کاربری باید حداقل 4 کاراکتر باشد",
            "max_length": "طول نام کاربری باید حداکثر 20 کاراکتر باشد",
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "required": True, "id": "password1"}
        ),
        validators=[
            validators.MinLengthValidator(8),
            validators.MaxLengthValidator(16),
            validators.RegexValidator(
                regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="رمز عبور باید ترکیبی از حروف بزرگ و کوچک لاتین، عدد و کاراکتر خاص باشد",
            ),
        ],
        label="رمز عبور",
        error_messages={
            "min_length": "طول رمز عبور باید حداقل 8 کاراکتر باشد",
            "max_length": "طول رمز عبور باید حداکثر 16 کاراکتر باشد",
        },
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "required": True, "id": "password2"}
        ),
        validators=[
            validators.MinLengthValidator(8),
            validators.MaxLengthValidator(16),
            validators.RegexValidator(
                regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="رمز عبور باید ترکیبی از حروف بزرگ و کوچک لاتین، عدد و کاراکتر خاص باشد",
            ),
        ],
        label="تایید رمز عبور",
        error_messages={
            "min_length": "طول رمز عبور باید حداقل 8 کاراکتر باشد",
            "max_length": "طول رمز عبور باید حداکثر 16 کاراکتر باشد",
        },
    )

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "required": False, "id": "email"}
        ),
        validators=[
            validators.MaxLengthValidator(60),
            validators.EmailValidator(message="لطفاَ یک ایمیل معتبر وارد کنید"),
        ],
        label="ایمیل",
    )

    def clean_confirm_password(self):
        """
        Validates that the confirm password matches the password.
        """
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password == confirm_password:
            return confirm_password
        else:
            raise forms.ValidationError("رمز عبور و تایید رمز عبور مغایرت دارند.")

    def clean_email(self):
        """
        Validates that the email is unique. Checks if the email already exists in the database.
        """
        email = self.cleaned_data.get("email")
        url = reverse("index_page")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                format_html(
                    "ایمیل وارد شده در سایت موجود است، "
                    'آیا قبلاً ثبت نام کرده اید؟ برای ورود <a href="{}">کلیک</a> کنید.',
                    url,
                )
            )
        return email


class LoginForm(forms.Form):
    """
    Form for user login including username and password.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": True,
            }
        ),
        label="نام کاربری",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="رمز عبور",
        validators=[
            validators.MinLengthValidator(8),
            validators.MaxLengthValidator(16),
        ],
    )


class ResetPasswordForm(forms.Form):
    """
    Form for resetting the password, including new password and confirmation.
    """

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "required": True, "id": "password1"}
        ),
        validators=[
            validators.MinLengthValidator(8),
            validators.MaxLengthValidator(16),
            validators.RegexValidator(
                regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="رمز عبور باید ترکیبی از حروف بزرگ و کوچک لاتین، عدد و کاراکتر خاص باشد",
            ),
        ],
        label="رمز عبور",
        error_messages={
            "min_length": "طول رمز عبور باید حداقل 8 کاراکتر باشد",
            "max_length": "طول رمز عبور باید حداکثر 16 کاراکتر باشد",
        },
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "required": True, "id": "password2"}
        ),
        validators=[
            validators.MinLengthValidator(8),
            validators.MaxLengthValidator(16),
            validators.RegexValidator(
                regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="رمز عبور باید ترکیبی از حروف بزرگ و کوچک لاتین، عدد و کاراکتر خاص باشد",
            ),
        ],
        label="تایید رمز عبور",
        error_messages={
            "min_length": "طول رمز عبور باید حداقل 8 کاراکتر باشد",
            "max_length": "طول رمز عبور باید حداکثر 16 کاراکتر باشد",
        },
    )

    def clean_confirm_password(self):
        """
        Validates that the confirm password matches the new password.
        """
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if new_password == confirm_password:
            return confirm_password
        else:
            raise forms.ValidationError("رمز عبور و تایید رمز عبور مغایرت دارند.")


class ForgetPasswordForm(forms.Form):
    """
    Form for requesting a password reset email by providing the registered email.
    """

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "required": False, "id": "email"}
        ),
        validators=[
            validators.MaxLengthValidator(60),
            validators.EmailValidator(message="لطفاَ یک ایمیل معتبر وارد کنید"),
        ],
        label="ایمیل",
    )
