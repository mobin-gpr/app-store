from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.generic import View
from .forms import RegisterForm, ResetPasswordForm, ForgetPasswordForm
from .models import User, AvatarImagesModel
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from utils.email_service import send_styled_mail
import json
from applications.models import AppsCommentsModel, AppRequestModel
from news.models import NewsCommentsModel
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist


def get_site_name():
    try:
        current_site = Site.objects.get_current()
        return current_site.name
    except ObjectDoesNotExist:
        return "Default Site Name"  # Fallback if Site model is not available


site_name = get_site_name()


class RegisterView(View):
    """
    View to handle user registration.
    """

    def get(self, request):
        """
        Renders the registration page. Redirects to profile page if the user is authenticated.
        """
        if request.user.is_authenticated:
            return redirect(reverse("profile_page"))
        form = RegisterForm()
        context = {"form": form}
        return render(request, "user_app/register.html", context)

    def post(self, request):
        """
        Handles form submission for user registration. Validates and creates a new user.
        """
        form = RegisterForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")

            if User.objects.filter(username=username).exists():
                form.add_error("username", "نام کاربری توسط شخص دیگری انتخاب شده است.")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    email_activate_code=get_random_string(72),
                    is_active=False,
                )
                user.set_password(password)
                user.save()
                send_styled_mail(
                    "فعالسازی حساب کاربری",
                    user.email,
                    {"user": user, "site_name": site_name},
                    "template_config/emails/account_activate.html",
                )
                request.session.pop("user_email", None)
                request.session["user_email"] = user.email
                return redirect(reverse("confirm_email"))

        return render(request, "user_app/register.html", context)


class ActivateAccountView(View):
    """
    View to handle email activation for user accounts.
    """

    def get(self, request, email_activate_code):
        """
        Activates the user account based on the provided activation code.
        """
        user: User = User.objects.filter(
            email_activate_code__iexact=email_activate_code
        ).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_activate_code = get_random_string(72)
                user.save()
                return redirect(reverse("index_page"))
            else:
                return redirect(reverse("index_page"))
        raise Http404


def logout_view(request):
    """
    Logs out the user and redirects to the index page.
    """
    logout(request)
    return redirect(reverse("index_page"))


class ProfileView(LoginRequiredMixin, View):
    """
    View to display the user's profile page. Requires the user to be logged in.
    """

    def get(self, request):
        """
        Renders the profile page for the authenticated user.
        """
        user = get_object_or_404(User, id=request.user.id)
        avatars = AvatarImagesModel.objects.filter(is_active=True).order_by("-id")[:16]
        context = {"user": user, "avatars": avatars}
        return render(request, "user_app/private_profile.html", context)


def login_user(request: HttpRequest):
    """
    Handles user login via a POST request. Returns authentication status as JSON.
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data[0]
        password = data[1]
        user = User.objects.filter(username=username).first()

        if user is not None:
            if user.check_password(password):
                if user.is_active:
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    response = {"authenticated": "success"}
                else:
                    response = {"authenticated": "not_active"}
            else:
                response = {"authenticated": "failed"}
        else:
            response = {"authenticated": "failed"}
    return JsonResponse(response)


def check_username(request: HttpRequest):
    """
    Checks if the provided username exists in the database. Returns the result as JSON.
    """
    if request.method == "POST":
        username = json.loads(request.body.decode("utf-8"))
        exist = User.objects.filter(username__iexact=username).exists()
        return JsonResponse({"exist": exist})
    if request.method == "GET":
        raise Http404


class PublicProfileView(View):
    """
    View to display a public user profile page.
    """

    def get(self, request, get_user):
        """
        Renders the public profile page for the specified user.
        """
        c_user = None
        if request.user.is_authenticated:
            c_user = User.objects.filter(id=request.user.id).first()
        user = get_object_or_404(User, username=get_user)
        comments_count = (
            AppsCommentsModel.objects.filter(user_id=user.id, is_active=True).count()
            + NewsCommentsModel.objects.filter(user_id=user.id, is_active=True).count()
        )
        app_requests_count = AppRequestModel.objects.filter(user_id=user.id).count()
        context = {
            "user": user,
            "comments_count": comments_count,
            "app_requests_count": app_requests_count,
            "c_user": c_user,
        }
        return render(request, "user_app/user.html", context)


class ResetPasswordView(View):
    """
    View to handle password reset requests.
    """

    def get(self, request, get_code):
        """
        Renders the password reset page if the activation code is valid.
        """
        user = User.objects.filter(email_activate_code__iexact=get_code).first()
        if user is None:
            return redirect(reverse("index_page"))
        form = ResetPasswordForm()
        context = {"form": form}
        return render(request, "user_app/reset_password.html", context)

    def post(self, request, get_code):
        """
        Handles form submission for resetting the password.
        """
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email_activate_code__iexact=get_code).first()
            if user is None:
                return redirect(reverse("index_page"))
            password = form.cleaned_data["new_password"]
            user.set_password(password)
            user.email_activate_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse("index_page"))
        context = {"form": form}
        return render(request, "user_app/reset_password.html", context)


class ForgetPasswordView(View):
    """
    View to handle forget password requests and send reset password emails.
    """

    def get(self, request):
        """
        Renders the forget password page.
        """
        form = ForgetPasswordForm()
        context = {"form": form}
        return render(request, "user_app/forget_password.html", context)

    def post(self, request):
        """
        Handles form submission for forgetting password and sends a reset password email.
        """
        form = ForgetPasswordForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            get_email = form.cleaned_data["email"]
            user: User = User.objects.filter(email=get_email).first()
            if user is not None:
                send_styled_mail(
                    "فراموشی رمز عبور",
                    user.email,
                    {"user": user, "site_name": site_name},
                    "template_config/emails/reset_password.html",
                )
                messages.success(request, "ایمیل بازیابی برای شما ارسال شد")
            else:
                form.add_error("email", "ایمیل وارد شده در سایت موجود نیست")
        return render(request, "user_app/forget_password.html", context)


class ConfirmEmailView(View):
    """
    View to confirm the user's email after registration.
    """

    def get(self, request):
        """
        Renders the email confirmation page if the email is present in the session.
        """
        get_email = request.session.get("user_email")
        user: User = User.objects.filter(email=get_email).first()
        if user is not None:
            context = {"user": user}
        else:
            return redirect(reverse("index_page"))
        return render(request, "user_app/confirm_email.html", context)


def login_required(request):
    """
    Renders a page indicating that login is required.
    """
    return render(request, "user_app/login_required.html")


def change_avatar(request):
    """
    Allows the authenticated user to change their avatar.
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body.decode("utf-8"))
            user: User = User.objects.filter(id=request.user.id).first()
            avatar_id = data["avatar_id"]
            get_avatar = AvatarImagesModel.objects.filter(id=avatar_id).first()
            user.avatar = get_avatar
            user.save()
            response = {"status": "ok", "username": user.username}
        else:
            response = {"status": "error"}

    return JsonResponse(response)
