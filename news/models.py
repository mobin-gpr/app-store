from django.urls import reverse
from django.db import models
from accounts.models import User
from utils.jalali_date import yyyy_month_dd_hh_mm


# region - Database Model of Tags
class TagsModel(models.Model):
    """
    Model representing tags that can be associated with news articles.
    """

    name = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(
        max_length=400, unique=True, verbose_name="اسلاگ", allow_unicode=True
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    def __str__(self):
        return self.name


# endregion


# region - Database Model of News
class NewsModel(models.Model):
    """
    Model representing news articles.
    """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, verbose_name="عنوان")
    seo_description = models.CharField(
        max_length=200, verbose_name="توضیحات سئو", null=True, blank=True
    )
    content = models.TextField(verbose_name="محتوا")
    slug = models.SlugField(
        max_length=400, unique=True, verbose_name="اسلاگ", allow_unicode=True
    )
    image = models.ImageField(
        upload_to="images/news/", verbose_name="تصویر خبر", null=True, blank=True
    )
    tag = models.ManyToManyField(TagsModel, verbose_name="برچسب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شود؟")

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"

    def __str__(self):
        return self.title

    def jalali_created_at(self):
        """
        Returns the creation date in Jalali (Persian) format.
        """
        return yyyy_month_dd_hh_mm(self.created_at)

    def get_absolute_url(self):
        """
        Returns the URL to access a detail view for this news article.
        """
        return reverse("news_detail", kwargs={"slug": self.slug})

    def seo_desc(self):
        """
        Returns the SEO description for this news article.
        """
        return self.seo_description or ""


# endregion


# region - Database Model of View News
class NewsVisitModel(models.Model):
    """
    Model to track visits to news articles.
    """

    news = models.ForeignKey(
        NewsModel, on_delete=models.SET_NULL, verbose_name="خبر", null=True
    )
    ip = models.CharField(max_length=100, verbose_name="آی پی کاربر")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "بازدید خبر"
        verbose_name_plural = "بازدید اخبار"

    def __str__(self):
        """
        Returns a string representation of the news visit, showing either the user or IP.
        """
        return f"{self.news_id} - {self.user if self.user else self.ip}"


# endregion


# region - Database Model of News Likes
class NewsLikesModel(models.Model):
    """
    Model to represent likes on news articles.
    """

    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE, verbose_name="خبر")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="کاربر", null=True, blank=True
    )
    ip = models.CharField(
        max_length=100, verbose_name="ایپی کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"

    def __str__(self):
        """
        Returns a string representation of the news like, showing either the user or IP.
        """
        return f"{self.news_id} - {self.user if self.user else self.ip}"


# endregion


# region - Database Model of News Dislikes
class NewsDisLikesModel(models.Model):
    """
    Model to represent dislikes on news articles.
    """

    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE, verbose_name="خبر")
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
        """
        Returns a string representation of the news dislike, showing either the user or IP.
        """
        return f"{self.news_id} - {self.user if self.user else self.ip}"


# endregion


# region - Database Model of News Comment
class NewsCommentsModel(models.Model):
    """
    Model representing comments on news articles.
    """

    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE, verbose_name="خبر")
    parent = models.ForeignKey(
        "NewsCommentsModel",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="والد",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    text = models.TextField(verbose_name="متن نظر")
    is_active = models.BooleanField(default=False, verbose_name="منتشر شود؟")

    class Meta:
        verbose_name = "نظر خبر"
        verbose_name_plural = "نظرات اخبار"

    def __str__(self):
        """
        Returns a string representation of the comment text.
        """
        return str(self.text)


# endregion


# region - Database Model of News Comments Like
class NewsCommentsLikeModel(models.Model):
    """
    Model to represent likes on news comments.
    """

    comment = models.ForeignKey(
        NewsCommentsModel, on_delete=models.CASCADE, verbose_name="نظر"
    )
    ip = models.CharField(
        max_length=100, verbose_name="ایپی کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "لایک نظر"
        verbose_name_plural = "لایک های نظرات"

    def __str__(self):
        """
        Returns a string representation of the comment like, showing a snippet of the comment text.
        """
        return f"{self.comment.text[:30]}..."


# endregion


# region - Database Model of News Comments Dislike
class NewsCommentsDisLikeModel(models.Model):
    """
    Model to represent dislikes on news comments.
    """

    comment = models.ForeignKey(
        NewsCommentsModel, on_delete=models.CASCADE, verbose_name="نظر"
    )
    ip = models.CharField(
        max_length=100, verbose_name="ایپی کاربر", null=True, blank=True
    )

    class Meta:
        verbose_name = "دیسلایک نظر"
        verbose_name_plural = "دیسلایک های نظرات"

    def __str__(self):
        """
        Returns a string representation of the comment dislike, showing a snippet of the comment text.
        """
        return f"{self.comment.text[:30]}..."


# endregion
