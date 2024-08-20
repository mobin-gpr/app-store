from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from django.utils.crypto import get_random_string
from accounts.models import User
from django.utils.text import slugify
from random import randint
from django.urls import reverse
from utils.jalali_date import yyyy_mm_dd, yyyy_month_dd_hh_mm
from utils.google_play_importer import get_app_data, en_genre_to_fa


class AppRequestModel(models.Model):
    """
    Model to represent an application request by a user.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="درخواست کننده"
    )
    app_link = models.URLField(verbose_name="لینک برنامه")

    class Meta:
        verbose_name = "درخواست برنامه"
        verbose_name_plural = "درخواست های برنامه"

    def __str__(self):
        return self.user.username


class AppsHelpModel(models.Model):
    """
    Model to represent an application help or tutorial.
    """

    title = models.CharField(max_length=200, verbose_name="عنوان آموزش")
    description = models.TextField(verbose_name="توضیح آموزش")
    slug = models.SlugField(
        verbose_name="اسلاگ", max_length=400, unique=True, allow_unicode=True
    )
    is_active = models.BooleanField(default=True, verbose_name="منشر شود؟")

    class Meta:
        verbose_name = "آموزش"
        verbose_name_plural = "آموزش ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("help_detail", kwargs={"slug": self.slug})


class ApplicationMainCaregoryModel(models.Model):
    """
    Model to represent the main categories of applications.
    """

    category = models.CharField(max_length=200, verbose_name="دسته اصلی")
    slug = models.SlugField(
        max_length=400, unique=True, verbose_name="اسلاگ", allow_unicode=True
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    class Meta:
        verbose_name = "دسته اصلی"
        verbose_name_plural = "دسته های اصلی"

    def __str__(self):
        return self.category


class ApplicationModel(models.Model):
    """
    Model to represent an application or game.
    """

    group = (
        ("1", "برنامه"),
        ("2", "بازی"),
    )

    title = models.CharField(max_length=200, verbose_name="عنوان")
    group = models.CharField(choices=group, max_length=50, verbose_name="گروه")
    main_caregory = models.ForeignKey(
        ApplicationMainCaregoryModel,
        on_delete=models.SET_NULL,
        verbose_name="دسته اصلی",
        null=True,
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="ناشر", null=True
    )
    slug = models.SlugField(
        max_length=400, unique=True, verbose_name="اسلاگ", allow_unicode=True
    )
    link_description = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="توضیحات بالای لینک"
    )
    link_information = models.TextField(
        blank=True, null=True, verbose_name="توضیحات زیر لینک"
    )
    update = models.DateTimeField(verbose_name="تاریخ به روزرسانی")
    version = models.CharField(
        max_length=200, verbose_name="نسخه", blank=True, null=True
    )
    android_version = models.CharField(
        max_length=200, verbose_name="نسخه مورد نیاز", blank=True, null=True
    )
    seo_description = models.CharField(
        max_length=200, verbose_name="توضیحات سئو", null=True, blank=True
    )
    content = models.TextField(verbose_name="محتوا", blank=True, null=True)
    price = models.CharField(
        max_length=200, verbose_name="قیمت در استور", blank=True, null=True
    )
    creator = models.CharField(
        max_length=200, verbose_name="سازنده", blank=True, null=True
    )
    score = models.CharField(
        max_length=200, verbose_name="امتیاز", blank=True, null=True
    )
    download_count = models.PositiveIntegerField(
        default=0, verbose_name="تعداد دانلود", blank=True, null=True
    )
    ages = models.CharField(
        max_length=200, verbose_name="رده سنی", blank=True, null=True
    )
    size = models.CharField(max_length=200, verbose_name="سایز", blank=True, null=True)
    icon = models.ImageField(upload_to="images/icons/", verbose_name="آیکون")
    is_update = models.BooleanField(default=False, verbose_name="آپدیت")
    is_online = models.BooleanField(default=False, verbose_name="آنلاین")
    is_new = models.BooleanField(default=False, verbose_name="جدید")
    is_mod = models.BooleanField(default=False, verbose_name="مود")
    is_free = models.BooleanField(default=False, verbose_name="رایگان")
    is_active = models.BooleanField(default=True, verbose_name="منتشر شود؟")

    class Meta:
        verbose_name = "نرم افزار"
        verbose_name_plural = "نرم افزارها"

    def __str__(self):
        return self.title

    def jalali_update_date(self):
        return yyyy_mm_dd(self.update)

    def get_absolute_url(self):
        if self.group == "1":
            url = reverse("application_detail", kwargs={"slug": self.slug})
        else:
            url = reverse("game_detail", kwargs={"slug": self.slug})
        return url

    def seo_desc(self):
        if self.seo_description is None:
            return ""
        else:
            self.seo_description


class SuggestedAppsModel(models.Model):
    """
    Model to represent suggested applications.
    """

    suggestion = models.ForeignKey(
        ApplicationModel,
        verbose_name="نرم افزار های پیشنهادی",
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True, verbose_name="منتشر شود؟")

    class Meta:
        verbose_name = "نرم افزار پیشنهادی"
        verbose_name_plural = "نرم افزارهای پیشنهادی"

    def __str__(self):
        return self.suggestion.title


class ApplicationScreenShotModel(models.Model):
    """
    Model to represent screenshots of an application.
    """

    title = models.CharField(max_length=200, verbose_name="عنوان تصویر")
    screenshot = models.ImageField(
        upload_to="images/screenshots/", verbose_name="اسکرین شات"
    )
    application = models.ForeignKey(
        ApplicationModel, on_delete=models.CASCADE, verbose_name="برنامه"
    )

    class Meta:
        verbose_name = "اسکریت شات"
        verbose_name_plural = "اسکرین شات ها"

    def __str__(self):
        return self.title + self.application.title


class ApplicationLinkModel(models.Model):
    """
    Model to represent links associated with an application.
    """

    color_options = (
        ("s-green", "سبز"),
        ("s-yellow", "زرد"),
        ("s-red", "قرمز"),
        ("s-blue", "آبی"),
    )
    title = models.CharField(max_length=200, verbose_name="متن دکمه")
    application = models.ForeignKey(
        ApplicationModel, on_delete=models.CASCADE, verbose_name="برنامه"
    )
    color = models.CharField(
        max_length=200,
        verbose_name="رنگ دکمه",
        choices=color_options,
        default="s-green",
    )
    slug = models.SlugField(
        max_length=400, verbose_name="اسلاگ", blank=True, unique=True
    )
    file = models.FileField(
        upload_to="files/", verbose_name="فایل برنامه", blank=True, null=True
    )
    volume = models.CharField(max_length=200, verbose_name="حجم")
    is_active = models.BooleanField(default=True, verbose_name="غعال/غیرغعال")

    class Meta:
        verbose_name = "لینک"
        verbose_name_plural = "لینک ها"

    def __str__(self):
        return self.application.title

    def save(self, *args, **kwargs):
        self.slug = slugify(
            self.application.title
            + "-"
            + str(randint(100000000000000, 999999999999999))
        )
        super(ApplicationLinkModel, self).save(*args, **kwargs)


class ApplicationImporterModel(models.Model):
    """
    Model to import applications information by google play store id .
    """

    google_play_id = models.CharField(max_length=200, verbose_name="آیدی google play")
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="ناشر", null=True, blank=True
    )

    class Meta:
        verbose_name = "ایمپورتر"
        verbose_name_plural = "ایمپورتر"

    def __str__(self):
        return self.google_play_id


class AppsLikesModel(models.Model):
    """
    Model to represent applications like.
    """

    app = models.ForeignKey(
        ApplicationModel, on_delete=models.CASCADE, verbose_name="نرم افزار"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="کاربر", null=True, blank=True
    )
    ip = models.CharField(
        max_length=100, verbose_name="ایپی کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"

    def __str__(self):
        if self.user is not None:
            user = self.user
        else:
            user = self.ip
        return f"{self.app} - {user}"


class AppsDisLikesModel(models.Model):
    """
    Model to represent applications like.
    """

    app = models.ForeignKey(
        ApplicationModel, on_delete=models.CASCADE, verbose_name="نرم افزار"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="کاربر", null=True, blank=True
    )
    ip = models.CharField(
        max_length=100, verbose_name="ایپی کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "دیسلایک"
        verbose_name_plural = "دیسلایک ها"

    def __str__(self):
        if self.user is not None:
            user = self.user
        else:
            user = self.ip
        return f"{self.app} - {user}"


class AppsCommentsModel(models.Model):
    """
    Model to represent applications comments.
    """

    app = models.ForeignKey(
        ApplicationModel, on_delete=models.CASCADE, verbose_name="نرم افزار"
    )
    parent = models.ForeignKey(
        "AppsCommentsModel",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="والد",
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر"
    )
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    text = models.TextField(verbose_name="متن نظر")
    is_active = models.BooleanField(default=False, verbose_name="منتشر شود؟")

    class Meta:
        verbose_name = "نظر برنامه"
        verbose_name_plural = "نظرات برنامه ها"

    def __str__(self):
        return str(self.text)

    # def save(self, *args, **kwargs):
    #     if self.parent.is_active == False:
    #         self.is_active = False
    #     super(AppsCommentsModel, self).save(*args, **kwargs)

    def send_date(self):
        return yyyy_month_dd_hh_mm(self.create_date)


class AppsCommentsLikeModel(models.Model):
    """
    Model to represent applications comments like.
    """

    comment = models.ForeignKey(
        AppsCommentsModel, on_delete=models.CASCADE, verbose_name="کامنت"
    )
    ip = models.CharField(
        max_length=100, verbose_name="ایپی کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "لایک کامنت"
        verbose_name_plural = "لایک های کامنت"

    def __str__(self):
        return f"{self.comment.text[:30]}..."


class AppsCommentsDisLikeModel(models.Model):
    """
    Model to represent applications comments like.
    """

    comment = models.ForeignKey(
        AppsCommentsModel, on_delete=models.CASCADE, verbose_name="کامنت"
    )
    ip = models.CharField(
        max_length=100, verbose_name="ایپی کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "دیسلایک کامنت"
        verbose_name_plural = "دیسلایک های کامنت"

    def __str__(self):
        return f"{self.comment.text[:30]}..."


@receiver(post_save, sender=ApplicationImporterModel)
def create_app_record(sender, instance, created, **kwargs):
    """
    Get Application Data From Application ID in Importer Model
    """
    if created:
        author = instance.author
        # Get App Data From Link
        google_app_id = instance.google_play_id
        data = get_app_data(google_app_id)
        # - Convert DateTime Type
        get_last_update = data["lastUpdatedOn"]
        date_string = get_last_update
        date_object = datetime.strptime(date_string, "%b %d, %Y")
        date_object = date_object.replace(hour=0, minute=0, second=0)

        # - Get App Type
        get_group = data.get("genreId")
        if "GAME" in get_group:
            group = "2"
        else:
            group = "1"

        # - Create Slug
        get_slug = slugify(data["title"])

        # - Convert Icon Link To JPG File
        img_url = data["icon"]
        img_response = requests.get(img_url)
        custom_url = "uploads/images/icons/"
        random_name = get_random_string(20) + ".jpg"
        if img_response.status_code == 200:
            with open(custom_url + random_name, "wb") as f:
                f.write(img_response.content)

        icon_dir = f"images/icons/{random_name}"

        # Get MainCategory & Set it
        if ApplicationMainCaregoryModel.objects.filter(
            slug=slugify(data["genreId"])
        ).exists():
            get_genre = ApplicationMainCaregoryModel.objects.get(
                slug=slugify(data["genreId"])
            )
        else:
            get_genre = ApplicationMainCaregoryModel(
                category=en_genre_to_fa(data["genreId"]), slug=slugify(data["genreId"])
            )
            get_genre.save()

        record_app = ApplicationModel(
            title=data["title"],
            group=group,
            update=date_object,
            version=data["version"],
            android_version="4.2.2",
            price=str(data["price"]),
            creator=data["developer"],
            download_count=data["realInstalls"],
            ages=data["contentRating"],
            is_active=True,
            icon=icon_dir,
            main_caregory=get_genre,
            slug=get_slug,
            author=author,
        )
        record_app.save()

        # Get ScreenShots & Set Them For App
        for screenshot in data["screenshots"][:4]:
            img_response = requests.get(screenshot)
            save_path = "uploads/images/screenshots/"
            random_file_name = get_random_string(20) + ".jpg"
            if img_response.status_code == 200:
                with open(save_path + random_file_name, "wb") as f:
                    f.write(img_response.content)
            screenshot_path = f"images/screenshots/{random_file_name}"

            ApplicationScreenShotModel.objects.create(
                title=data["title"],
                screenshot=screenshot_path,
                application_id=record_app.id,
            )
