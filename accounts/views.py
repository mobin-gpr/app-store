from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.cache import cache

from .forms import RegisterForm, ResetPasswordForm, ForgetPasswordForm
from .models import User, AvatarImagesModel
from applications.models import AppsCommentsModel, AppRequestModel
from news.models import NewsCommentsModel
from utils.email_service import send_styled_mail
from utils.validators import validate_json_request


def get_site_name():
    """
    Get current site name with caching.

    Returns:
        str: Site name or default fallback
    """
    site_name = cache.get("site_name")
    if not site_name:
        try:
            from django.contrib.sites.models import Site

            site_name = Site.objects.get_current().name
            cache.set("site_name", site_name, 3600)  # Cache for 1 hour
        except Exception:
            site_name = "App Store"  # Fallback
    return site_name


class RegisterView(View):
    """
    Handle user registration.

    GET: Display registration form (redirect if already authenticated)
    POST: Process registration, create user, send activation email
    """

    def get(self, request):
        """Display registration form or redirect if authenticated."""
        if request.user.is_authenticated:
            return redirect(reverse("profile_page"))

        return render(request, "user_app/register.html", {"form": RegisterForm()})

    def post(self, request):
        """Process registration form and create new user."""
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                form.add_error("username", "نام کاربری توسط شخص دیگری انتخاب شده است.")
            else:
                # Create inactive user with activation code
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    email_activate_code=get_random_string(72),
                    is_active=False,
                )
                user.set_password(password)
                user.save()

                # Send activation email
                send_styled_mail(
                    "فعالسازی حساب کاربری",
                    user.email,
                    {"user": user, "site_name": get_site_name()},
                    "template_config/emails/account_activate.html",
                )

                # Store email in session for confirmation page
                request.session["user_email"] = user.email
                return redirect(reverse("confirm_email"))

        return render(request, "user_app/register.html", {"form": form})


class ActivateAccountView(View):
    """
    Handle email activation for user accounts.

    Activates user account using the provided activation code.
    Generates new code after activation for security.
    """

    def get(self, request, email_activate_code):
        """Activate user account with the provided code."""
        user = User.objects.filter(email_activate_code__iexact=email_activate_code).first()

        if user is None:
            raise Http404("Invalid activation code")

        if not user.is_active:
            # Activate user and regenerate code
            user.is_active = True
            user.email_activate_code = get_random_string(72)
            user.save()
            messages.success(request, "حساب کاربری شما با موفقیت فعال شد.")

        return redirect(reverse("index_page"))


def logout_view(request):
    """
    Log out the current user.

    Clears the session and redirects to homepage.
    """
    logout(request)
    messages.info(request, "شما با موفقیت خارج شدید.")
    return redirect(reverse("index_page"))


class ProfileView(LoginRequiredMixin, View):
    """
    Display user's private profile page.

    Shows user information and available avatars.
    Requires authentication.
    """

    login_url = "/login-required/"

    def get(self, request):
        """Render the private profile page."""
        # Get available avatars (cached)
        cache_key = "available_avatars"
        avatars = cache.get(cache_key)
        if not avatars:
            avatars = AvatarImagesModel.objects.filter(is_active=True).only("id", "image").order_by("-id")[:16]
            cache.set(cache_key, avatars, 600)  # Cache for 10 minutes

        context = {
            "user": request.user,
            "avatars": avatars,
        }
        return render(request, "user_app/private_profile.html", context)


def login_user(request: HttpRequest):
    """
    Handle user login via AJAX request.

    Expects POST request with JSON array: [username, password]

    Returns:
        JSON response with authentication status:
        - 'success': Login successful
        - 'not_active': Account not activated
        - 'failed': Invalid credentials
    """
    if request.method != "POST":
        return JsonResponse({"authenticated": "failed"}, status=405)

    try:
        # Parse request data
        data = validate_json_request(request)
        username = data[0] if isinstance(data, list) and len(data) >= 2 else None
        password = data[1] if isinstance(data, list) and len(data) >= 2 else None

        if not username or not password:
            return JsonResponse({"authenticated": "failed"})

        # Try to authenticate
        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            return JsonResponse({"authenticated": "failed"})

        if not user.is_active:
            return JsonResponse({"authenticated": "not_active"})

        # Log user in
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return JsonResponse({"authenticated": "success"})

    except Exception:
        return JsonResponse({"authenticated": "failed"}, status=400)


def check_username(request: HttpRequest):
    """
    Check if a username is already taken.

    Expects POST request with JSON containing username string.

    Returns:
        JSON response with 'exist' boolean
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = validate_json_request(request)
        username = data if isinstance(data, str) else data.get("username", "")

        if not username or len(username) < 3:
            return JsonResponse({"exist": False, "error": "Invalid username"})

        exists = User.objects.filter(username__iexact=username).exists()
        return JsonResponse({"exist": exists})

    except Exception:
        return JsonResponse({"exist": False, "error": "Invalid request"}, status=400)


class PublicProfileView(View):
    """
    Display a public user profile page.

    Shows user's public information, comment count, and app request count.
    Visible to all users (authenticated or not).
    """

    def get(self, request, get_user):
        """Render the public profile page for a specific user."""
        # Get target user
        user = get_object_or_404(User.objects.select_related("avatar"), username=get_user)

        # Get statistics (optimized with single queries)
        comments_count = (
            AppsCommentsModel.objects.filter(user_id=user.id, is_active=True).count()
            + NewsCommentsModel.objects.filter(user_id=user.id, is_active=True).count()
        )

        app_requests_count = AppRequestModel.objects.filter(user_id=user.id).count()

        context = {
            "user": user,
            "comments_count": comments_count,
            "app_requests_count": app_requests_count,
            "c_user": request.user if request.user.is_authenticated else None,
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
                    {"user": user, "site_name": get_site_name()},
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
    Change user's avatar.

    Expects POST request with JSON containing avatar_id.
    Requires authentication.

    Returns:
        JSON response with status and username
    """
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    try:
        data = validate_json_request(request, required_fields=["avatar_id"])
        avatar_id = int(data["avatar_id"])

        # Verify avatar exists and is active
        avatar = get_object_or_404(AvatarImagesModel, id=avatar_id, is_active=True)

        # Update user's avatar
        request.user.avatar = avatar
        request.user.save(update_fields=["avatar"])

        # Invalidate user cache if any
        cache.delete(f"user_{request.user.id}_avatar")

        return JsonResponse(
            {
                "status": "ok",
                "username": request.user.username,
                "avatar_url": avatar.image.url if avatar.image else None,
            }
        )

    except ValidationError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    except Exception:
        return JsonResponse({"status": "error", "message": "An error occurred"}, status=500)
