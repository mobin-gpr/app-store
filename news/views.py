from django.http import HttpRequest, JsonResponse
from django.views.generic import ListView, DetailView
from .models import (
    NewsModel,
    NewsVisitModel,
    NewsLikesModel,
    NewsDisLikesModel,
    TagsModel,
    NewsCommentsModel,
    NewsCommentsLikeModel,
    NewsCommentsDisLikeModel,
)
from accounts.models import User
from utils.http_services import get_ip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.contrib.sites.models import Site


class NewsListView(ListView):
    """Display the list of news"""

    template_name = "news/news-list.html"
    model = NewsModel
    context_object_name = "news_list"
    paginate_by = 5

    def get_queryset(self):
        return NewsModel.objects.filter(is_published=True).order_by(
            "-created_at"
        )  # Only show published news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = TagsModel.objects.filter(is_active=True)
        return context


class NewsDetailView(DetailView):
    """Displat the news detals"""

    template_name = "news/news_detail.html"
    model = NewsModel
    context_object_name = "news"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)  # Only show published news
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_id = self.object.pk
        likes = NewsLikesModel.objects.filter(news_id=news_id).count()
        dislike = NewsDisLikesModel.objects.filter(news_id=news_id).count()
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context["site_name"] = site_name
        context["likes"] = likes
        context["dislike"] = dislike
        # Record view by user model if user was authenticated
        if self.request.user.is_authenticated:
            user: User = User.objects.filter(id=self.request.user.id).first()
            # If user visited the news before do nothing
            if NewsVisitModel.objects.filter(user_id=user.id, news_id=news_id).exists():
                pass
            # Record a view
            else:
                NewsVisitModel.objects.create(user_id=user.id, news_id=news_id)
        # Record view by ip if user was not authenticated
        else:
            user_ip = get_ip(self.request)
            # If user visited the news before do nothing
            if NewsVisitModel.objects.filter(ip=user_ip, news_id=news_id).exists():
                pass
            # Record a view
            else:
                NewsVisitModel.objects.create(ip=user_ip, news_id=news_id)
        comments = (
            NewsCommentsModel.objects.filter(
                is_active=True, news_id=news_id, parent=None
            )
            .order_by("-create_date")
            .prefetch_related("newscommentsmodel_set")
        )
        paginator = Paginator(comments, 5)
        page = self.request.GET.get("page")

        try:
            paginated_comments = paginator.page(page)
        except PageNotAnInteger:
            paginated_comments = paginator.page(1)
        except EmptyPage:
            paginated_comments = paginator.page(paginator.num_pages)
        context["comments"] = paginated_comments
        context["comments_count"] = NewsCommentsModel.objects.filter(
            is_active=True, news_id=news_id
        ).count()
        return context


def news_reaction(request: HttpRequest):
    """
    Add reaction to news
    :param request:
    :return:
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        news_id = int(data["post_id"])
        reaction = data["type"]
        ip = get_ip(request)
        if reaction == "like":
            # Check If User Liked The News Befor Do Nothing
            if NewsLikesModel.objects.filter(ip=ip, news_id=news_id).exists():
                response = {
                    "like": NewsLikesModel.objects.filter(news_id=news_id).count(),
                    "dislike": NewsDisLikesModel.objects.filter(
                        news_id=news_id
                    ).count(),
                }

            else:
                # If User Was Disliked The News Before Delete Dislike & Then Like The News
                if NewsDisLikesModel.objects.filter(ip=ip, news_id=news_id).exists():
                    NewsDisLikesModel.objects.filter(ip=ip, news_id=news_id).delete()
                NewsLikesModel.objects.create(ip=ip, news_id=news_id)
                response = {
                    "like": NewsLikesModel.objects.filter(news_id=news_id).count(),
                    "dislike": NewsDisLikesModel.objects.filter(
                        news_id=news_id
                    ).count(),
                }
        elif reaction == "dislike":
            # Check If User Disliked The News Befor Do Nothing
            if NewsDisLikesModel.objects.filter(ip=ip, news_id=news_id).exists():
                response = {
                    "like": NewsLikesModel.objects.filter(news_id=news_id).count(),
                    "dislike": NewsDisLikesModel.objects.filter(
                        news_id=news_id
                    ).count(),
                }
            else:
                # If User Was Liked The News Before Delete Like & Then Dislike The News
                if NewsLikesModel.objects.filter(ip=ip, news_id=news_id).exists():
                    NewsLikesModel.objects.filter(ip=ip, news_id=news_id).delete()
                NewsDisLikesModel.objects.create(ip=ip, news_id=news_id)
                response = {
                    "like": NewsLikesModel.objects.filter(news_id=news_id).count(),
                    "dislike": NewsDisLikesModel.objects.filter(
                        news_id=news_id
                    ).count(),
                }

    return JsonResponse(response)


class NewsCategoryListView(ListView):
    """
    Listing Categories of News
    """

    model = NewsModel
    template_name = "news/category.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return NewsModel.objects.filter(
            is_published=True, tag__slug=self.kwargs["slug"]
        ).order_by("-id")


def add_news_comment(request: HttpRequest):
    """
    Add comment for news comment
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            is_staff = True if request.user.is_staff else False
            data = json.loads(request.body.decode("utf-8"))
            news_id = data["news_id"]
            news_comment = data["news_comment"]
            get_parent_id = int(data["parent_id"])
            parent_id = None if get_parent_id == 0 else get_parent_id
            new_comment = NewsCommentsModel(
                news_id=news_id,
                text=news_comment,
                parent_id=parent_id,
                user_id=request.user.id,
                is_active=is_staff,
            )
            new_comment.save()
            response = {"success": True}
            return JsonResponse(response)


def news_comments_reactions(request: HttpRequest):
    """Handle News Comments Likes & Dislikes Reactions"""
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        comment_id = int(data["comment_id"])
        reaction = data["type"]
        ip = get_ip(request)
        print(comment_id, reaction, ip)

        if reaction == "like":
            # Check If User Liked The App Befor Do Nothing
            if NewsCommentsLikeModel.objects.filter(
                ip=ip, comment_id=comment_id
            ).exists():
                response = {
                    "like": NewsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": NewsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }

            else:
                # If User Was Disliked The App Before Delete Dislike & Then Like The App
                if NewsCommentsDisLikeModel.objects.filter(
                    ip=ip, comment_id=comment_id
                ).exists():
                    NewsCommentsDisLikeModel.objects.filter(
                        ip=ip, comment_id=comment_id
                    ).delete()
                NewsCommentsLikeModel.objects.create(ip=ip, comment_id=comment_id)
                response = {
                    "like": NewsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": NewsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }
        elif reaction == "dislike":
            # Check If User Disliked The App Befor Do Nothing
            if NewsCommentsDisLikeModel.objects.filter(
                ip=ip, comment_id=comment_id
            ).exists():
                response = {
                    "like": NewsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": NewsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }
            else:
                # If User Was Liked The App Before Delete Like & Then Dislike The App
                if NewsCommentsLikeModel.objects.filter(
                    ip=ip, comment_id=comment_id
                ).exists():
                    NewsCommentsLikeModel.objects.filter(
                        ip=ip, comment_id=comment_id
                    ).delete()
                NewsCommentsDisLikeModel.objects.create(ip=ip, comment_id=comment_id)
                response = {
                    "like": NewsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": NewsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }

    return JsonResponse(response)


class FilterNewsByAuthorView(ListView):
    """Filtering new by author"""

    model = NewsModel
    template_name = "news/category.html"
    context_object_name = "news_list"
    paginate_by = 12

    def get_queryset(self):
        return NewsModel.objects.filter(
            is_published=True, author__username=self.kwargs["user"]
        )
