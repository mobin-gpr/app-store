# Generated by Django 5.0.4 on 2024-08-18 20:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TagsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="عنوان")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=400,
                        unique=True,
                        verbose_name="اسلاگ",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="فعال/غیرفعال"),
                ),
            ],
            options={
                "verbose_name": "برچسب",
                "verbose_name_plural": "برچسب ها",
            },
        ),
        migrations.CreateModel(
            name="NewsCommentsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت"),
                ),
                ("text", models.TextField(verbose_name="متن نظر")),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="منتشر شود؟"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news.newscommentsmodel",
                        verbose_name="والد",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر",
                    ),
                ),
            ],
            options={
                "verbose_name": "نظر خبر",
                "verbose_name_plural": "نظرات اخبار",
            },
        ),
        migrations.CreateModel(
            name="NewsCommentsLikeModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ip",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="ایپی کاربر"
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news.newscommentsmodel",
                        verbose_name="نظر",
                    ),
                ),
            ],
            options={
                "verbose_name": "لایک نظر",
                "verbose_name_plural": "لایک های نظرات",
            },
        ),
        migrations.CreateModel(
            name="NewsCommentsDisLikeModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ip",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="ایپی کاربر"
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news.newscommentsmodel",
                        verbose_name="نظر",
                    ),
                ),
            ],
            options={
                "verbose_name": "دیسلایک نظر",
                "verbose_name_plural": "دیسلایک های نظرات",
            },
        ),
        migrations.CreateModel(
            name="NewsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="عنوان")),
                (
                    "seo_description",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="توضیحات سئو",
                    ),
                ),
                ("content", models.TextField(verbose_name="محتوا")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        max_length=400,
                        unique=True,
                        verbose_name="اسلاگ",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="images/news/",
                        verbose_name="تصویر خبر",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ انتشار"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="منتشر شود؟"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tag",
                    models.ManyToManyField(to="news.tagsmodel", verbose_name="برچسب"),
                ),
            ],
            options={
                "verbose_name": "خبر",
                "verbose_name_plural": "اخبار",
            },
        ),
        migrations.CreateModel(
            name="NewsLikesModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ip",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="ایپی کاربر"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر",
                    ),
                ),
                (
                    "news",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news.newsmodel",
                        verbose_name="خبر",
                    ),
                ),
            ],
            options={
                "verbose_name": "لایک",
                "verbose_name_plural": "لایک ها",
            },
        ),
        migrations.CreateModel(
            name="NewsDisLikesModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ip",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="ایپی کاربر"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر",
                    ),
                ),
                (
                    "news",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news.newsmodel",
                        verbose_name="خبر",
                    ),
                ),
            ],
            options={
                "verbose_name": "دیسلایک",
                "verbose_name_plural": "دیسلایک ها",
            },
        ),
        migrations.AddField(
            model_name="newscommentsmodel",
            name="news",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="news.newsmodel",
                verbose_name="خبر",
            ),
        ),
        migrations.CreateModel(
            name="NewsVisitModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip", models.CharField(max_length=100, verbose_name="آی پی کاربر")),
                (
                    "news",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="news.newsmodel",
                        verbose_name="خبر",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر",
                    ),
                ),
            ],
            options={
                "verbose_name": "بازدید خبر",
                "verbose_name_plural": "بازدید اخبار",
            },
        ),
    ]
