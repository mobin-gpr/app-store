from django.contrib.sitemaps import Sitemap
from applications.models import ApplicationModel, AppsHelpModel
from news.models import NewsModel


class ApplicationModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ApplicationModel.objects.filter(is_active=True)


class AppsHelpModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return AppsHelpModel.objects.filter(is_active=True)


class NewsModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return NewsModel.objects.filter(is_published=True)
