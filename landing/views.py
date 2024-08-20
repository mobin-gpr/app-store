from django.shortcuts import render
from django.views.generic import View
from applications.models import (
    ApplicationModel,
    SuggestedAppsModel,
    AppsCommentsModel,
)
from news.models import NewsModel
from django.contrib.sites.models import Site


class IndexView(View):
    def get(self, request):
        games = ApplicationModel.objects.filter(is_active=True, group="2").order_by(
            "-id"
        )[:12]
        applications = ApplicationModel.objects.filter(
            is_active=True, group="1"
        ).order_by("-id")[:12]
        news = NewsModel.objects.filter(is_published=True).order_by("-id")[:2]
        suggestions = SuggestedAppsModel.objects.filter(is_active=True).order_by("-id")
        comments = (
            AppsCommentsModel.objects.filter(is_active=True)
            .exclude(user__is_staff=True)
            .order_by("-id")[:3]
        )
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context = {
            "games": games,
            "applications": applications,
            "news_list": news,
            "suggestions": suggestions,
            "comments": comments,
            "site_name": site_name,
        }
        return render(request, "landing/index.html", context)
