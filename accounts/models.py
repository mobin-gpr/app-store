from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.jalali_date import yyyy_month_dd_hh_mm


class AvatarImagesModel(models.Model):
    """
    Model to store avatar images for users.

    Attributes:
        image (ImageField): The image file for the avatar, uploaded to "images/avatars/" directory.
        is_active (BooleanField): Indicates whether the avatar image is active or not.
    """

    image = models.ImageField(upload_to="images/avatars/", verbose_name="تصویر آواتار")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیر فعال")

    class Meta:
        verbose_name = "تصویر آواتار"  # Singular verbose name in Persian
        verbose_name_plural = "تصاویر آواتار"  # Plural verbose name in Persian

    def __str__(self):
        """Return the name of the image file as the string representation."""
        return self.image.name


class User(AbstractUser):
    """
    Custom user model extending the default Django AbstractUser.

    Attributes:
        email_activate_code (CharField): A unique code used for email activation.
        avatar (ForeignKey): A reference to the user's avatar image from the AvatarImagesModel.
    """

    email_activate_code = models.CharField(
        max_length=100, unique=True, verbose_name="کد فعالسازی حساب"
    )
    avatar = models.ForeignKey(
        AvatarImagesModel,
        on_delete=models.CASCADE,
        verbose_name="تصویر آواتار",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "کاربر"  # Singular verbose name in Persian
        verbose_name_plural = "کاربران"  # Plural verbose name in Persian

    def __str__(self):
        """Return the username as the string representation of the user."""
        return self.username

    def jajali_sign_up_date(self):
        """Return the user's signup date in Jalali (Persian) calendar format."""
        return yyyy_month_dd_hh_mm(self.date_joined)

    def jajali_last_login_date(self):
        """Return the user's last login date in Jalali (Persian) calendar format."""
        return yyyy_month_dd_hh_mm(self.last_login)
