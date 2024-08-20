from django.urls import path
from .views import (
    RegisterView,
    ActivateAccountView,
    logout_view,
    ProfileView,
    login_user,
    check_username,
    PublicProfileView,
    ResetPasswordView,
    ForgetPasswordView,
    ConfirmEmailView,
    login_required,
    change_avatar,
)

urlpatterns = [
    path("register", RegisterView.as_view(), name="register_page"),
    path(
        "account-activate/<email_activate_code>",
        ActivateAccountView.as_view(),
        name="account_activate",
    ),
    path("logout/", logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile_page"),
    path(
        "profile/<str:get_user>",
        PublicProfileView.as_view(),
        name="public_profile_page",
    ),
    path(
        "reset-password/<str:get_code>",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path("forget-password/", ForgetPasswordView.as_view(), name="forget-password"),
    path("login/", login_user, name="login"),
    path("ajax/check-username/", check_username),
    path("ajax/change-avatar/", change_avatar),
    path("confirm-email/", ConfirmEmailView.as_view(), name="confirm_email"),
    path("login-required/", login_required, name="login_required"),
]
