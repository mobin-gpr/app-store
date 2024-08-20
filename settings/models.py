from django.db import models


class FooterModel(models.Model):
    """
    Model to represent footer information.

    This model stores the footer content such as copyright text and social media links.
    It also includes an 'is_active' field to indicate whether this footer is currently active.
    """

    copyright = models.CharField(max_length=255, verbose_name="متن کپی رایت")
    telegram_url = models.URLField(verbose_name="لینک تلگرام", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    class Meta:
        # Human-readable names for this model in the admin interface
        verbose_name = "فوتر"
        verbose_name_plural = "فوتر"

    def __str__(self):
        # Return the copyright text as the string representation of the model
        return self.copyright


class LogoModel(models.Model):
    """
    Model to represent logos.

    This model stores the logo image and an 'is_active' field to indicate whether this logo is currently in use.
    """

    logo = models.ImageField(upload_to="logo/")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیر فعال")

    class Meta:
        # Human-readable names for this model in the admin interface
        verbose_name = "لوگو"
        verbose_name_plural = "لوگوها"

    def __str__(self):
        # Return the logo's file name as the string representation of the model
        return self.logo.name
