from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from accounts.models import User
from .models import (
    ApplicationModel,
    AppsLikesModel,
    AppsDisLikesModel,
    ApplicationMainCaregoryModel,
    AppsHelpModel,
    ApplicationLinkModel,
    AppRequestModel,
    AppsCommentsModel,
    AppsCommentsLikeModel,
    AppsCommentsDisLikeModel,
)
from utils.http_services import get_ip
from .forms import AppRequestForm
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.models import Site


class GamesListView(ListView):
    """
    View for listing active games.

    Displays games filtered by 'group=2' and paginated.
    """

    template_name = "application/games_list.html"
    model = ApplicationModel
    context_object_name = "apps"
    paginate_by = 12

    def get_queryset(self):
        return ApplicationModel.objects.filter(is_active=True, group="2").order_by(
            "-id"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            ApplicationMainCaregoryModel.objects.filter(
                is_active=True, applicationmodel__group="2"
            )
            .order_by("-id")
            .distinct()
        )
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context["site_name"] = site_name
        return context


class GamesDetailView(DetailView):
    """
    View for displaying details of a single game.

    Includes game details, related suggestions, and comments.
    """

    template_name = "application/game_detail.html"
    model = ApplicationModel
    context_object_name = "app"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object.id
        get_object = ApplicationModel.objects.get(id=obj)
        get_category = (
            ApplicationModel.objects.filter(
                is_active=True, main_caregory=get_object.main_caregory
            )
            .exclude(id=obj)
            .order_by("-id")[:6]
        )
        comments = (
            AppsCommentsModel.objects.filter(is_active=True, app_id=obj, parent=None)
            .order_by("-create_date")
            .prefetch_related("appscommentsmodel_set")
        )

        paginator = Paginator(comments, 5)
        page = self.request.GET.get("page")

        try:
            paginated_comments = paginator.page(page)
        except PageNotAnInteger:
            paginated_comments = paginator.page(1)
        except EmptyPage:
            paginated_comments = paginator.page(paginator.num_pages)
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context["suggestions"] = get_category
        context["cat_link"] = ApplicationModel.objects.get(id=obj)
        context["helps"] = AppsHelpModel.objects.filter(is_active=True)
        context["user"] = User.objects.filter(id=self.request.user.id).first()
        context["comments"] = paginated_comments
        context["comments_count"] = AppsCommentsModel.objects.filter(
            is_active=True, app_id=obj
        ).count()
        context["site_name"] = site_name
        return context


class ApplicationsListView(ListView):
    """
    View for listing active applications.

    Displays applications filtered by 'group=1' and paginated.
    """

    template_name = "application/applications_list.html"
    model = ApplicationModel
    context_object_name = "apps"
    paginate_by = 12

    def get_queryset(self):
        return ApplicationModel.objects.filter(is_active=True, group="1").order_by(
            "-id"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = (
            ApplicationMainCaregoryModel.objects.filter(
                is_active=True, applicationmodel__group="1"
            )
            .order_by("-id")
            .distinct()
        )
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context["site_name"] = site_name
        return context


class ApplicationsDetailView(DetailView):
    """
    View for displaying details of a single application.

    Includes application details, related suggestions, and comments.
    """

    template_name = "application/application_detail.html"
    model = ApplicationModel
    context_object_name = "app"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object.id
        get_object = ApplicationModel.objects.get(id=obj)
        get_category = (
            ApplicationModel.objects.filter(
                is_active=True, main_caregory=get_object.main_caregory
            )
            .exclude(id=obj)
            .order_by("-id")[:6]
        )
        comments = (
            AppsCommentsModel.objects.filter(is_active=True, app_id=obj, parent=None)
            .order_by("-create_date")
            .prefetch_related("appscommentsmodel_set")
        )

        paginator = Paginator(comments, 10)
        page = self.request.GET.get("page")

        try:
            paginated_comments = paginator.page(page)
        except PageNotAnInteger:
            paginated_comments = paginator.page(1)
        except EmptyPage:
            paginated_comments = paginator.page(paginator.num_pages)
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context["suggestions"] = get_category
        context["cat_link"] = ApplicationModel.objects.get(id=obj)
        context["helps"] = AppsHelpModel.objects.filter(is_active=True)
        context["user"] = User.objects.filter(id=self.request.user.id).first()
        context["comments"] = paginated_comments
        context["comments_count"] = AppsCommentsModel.objects.filter(
            is_active=True, app_id=obj
        ).count()
        context["site_name"] = site_name
        return context


def apps_reaction(request: HttpRequest):
    """
    Handles reactions (likes and dislikes) to applications.

    Returns the updated like and dislike counts in JSON format.
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        app_id = int(data["app_id"])
        reaction = data["type"]
        ip = get_ip(request)
        if reaction == "like":
            # Check If User Liked The App Befor Do Nothing
            if AppsLikesModel.objects.filter(ip=ip, app_id=app_id).exists():
                response = {
                    "like": AppsLikesModel.objects.filter(app_id=app_id).count(),
                    "dislike": AppsDisLikesModel.objects.filter(app_id=app_id).count(),
                }

            else:
                # If User Was Disliked The App Before Delete Dislike & Then Like The App
                if AppsDisLikesModel.objects.filter(ip=ip, app_id=app_id).exists():
                    AppsDisLikesModel.objects.filter(ip=ip, app_id=app_id).delete()
                AppsLikesModel.objects.create(ip=ip, app_id=app_id)
                response = {
                    "like": AppsLikesModel.objects.filter(app_id=app_id).count(),
                    "dislike": AppsDisLikesModel.objects.filter(app_id=app_id).count(),
                }
        elif reaction == "dislike":
            # Check If User Disliked The App Befor Do Nothing
            if AppsDisLikesModel.objects.filter(ip=ip, app_id=app_id).exists():
                response = {
                    "like": AppsLikesModel.objects.filter(app_id=app_id).count(),
                    "dislike": AppsDisLikesModel.objects.filter(app_id=app_id).count(),
                }
            else:
                # If User Was Liked The App Before Delete Like & Then Dislike The App
                if AppsLikesModel.objects.filter(ip=ip, app_id=app_id).exists():
                    AppsLikesModel.objects.filter(ip=ip, app_id=app_id).delete()
                AppsDisLikesModel.objects.create(ip=ip, app_id=app_id)
                response = {
                    "like": AppsLikesModel.objects.filter(app_id=app_id).count(),
                    "dislike": AppsDisLikesModel.objects.filter(app_id=app_id).count(),
                }

    return JsonResponse(response)


class CategoryListView(ListView):
    """
    View to display apps by category.

    Attributes:
        model (ApplicationModel): The model to retrieve apps data.
        template_name (str): The template used to render the category page.
        context_object_name (str): The name of the context variable containing the apps.
        paginate_by (int): Number of apps per page.
    """

    model = ApplicationModel
    template_name = "application/category.html"
    context_object_name = "apps"
    paginate_by = 12

    def get_queryset(self):
        return ApplicationModel.objects.filter(
            is_active=True, main_caregory__slug=self.kwargs["slug"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = ApplicationModel.objects.filter(
            is_active=True, main_caregory__slug=self.kwargs["slug"]
        ).first()
        context["categories"] = ApplicationMainCaregoryModel.objects.filter(
            is_active=True
        ).order_by("-id")
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context["site_name"] = site_name
        return context


class TopAppsView(ListView):
    """
    View for displaying the top applications.
    """

    template_name = "application/top.html"
    model = ApplicationModel
    context_object_name = "apps"

    def get_queryset(self):
        return (
            ApplicationModel.objects.filter(is_active=True)
            .annotate(like_count=Count("appslikesmodel"))
            .order_by("-like_count")[:100]
        )


class AppsHelpView(View):
    """
    View for displaying help pages related to applications.
    """

    def get(self, request, slug):
        print(slug)
        help = get_object_or_404(AppsHelpModel, slug=slug, is_active=True)
        context = {"help": help}
        return render(request, "application/help.html", context)


class DownloadAppView(View):
    """
    View for downloading applications.
    """

    def get(self, request, slug):
        check_auth = False
        link = get_object_or_404(ApplicationLinkModel, is_active=True, slug=slug)
        if request.user.is_authenticated:
            check_auth = True
        context = {"link": link, "check_auth": check_auth}
        return render(request, "application/download.html", context)


class AppRequestView(View):
    """
    View for handling requests for new applications.

    Allows authenticated users to submit requests for new apps.
    """

    def get(self, request):
        if request.user.is_authenticated:
            form = AppRequestForm()
            user = User.objects.filter(id=request.user.id).first()
            request_count = AppRequestModel.objects.all().count()
            user_request_count = AppRequestModel.objects.filter(user_id=user.id).count()
            context = {
                "form": form,
                "request_count": request_count,
                "user_request_count": user_request_count,
            }
            return render(request, "application/app_request.html", context)

        else:
            return redirect(reverse("login_required"))

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.filter(id=request.user.id).first()
            form = AppRequestForm(request.POST)
            user = User.objects.filter(id=request.user.id).first()
            request_count = AppRequestModel.objects.all().count()
            user_request_count = AppRequestModel.objects.filter(user_id=user.id).count()
            if form.is_valid():
                app_link = form.cleaned_data["app_link"]
                if not AppRequestModel.objects.filter(
                    app_link=app_link, user=user
                ).exists():
                    AppRequestModel.objects.create(user=user, app_link=app_link)
                    messages.success(request, "درخواست شما با موفقیت ثبت شد")
                else:
                    form.add_error(
                        "app_link", "شما قبلاً برای این اپلیکیشن درخواست ارسال کرده اید."
                    )
            context = {
                "form": form,
                "request_count": request_count,
                "user_request_count": user_request_count,
            }
            return render(request, "application/app_request.html", context)

        else:
            return redirect(reverse("login_required"))


def add_app_comment(request: HttpRequest):
    """
    Handles adding comments to applications.

    Requires the user to be authenticated and returns the newly created comment in JSON format.
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            is_staff = True if request.user.is_staff else False
            data = json.loads(request.body.decode("utf-8"))
            app_id = data["app_id"]
            app_comment = data["app_comment"]
            get_parent_id = int(data["parent_id"])
            parent_id = None if get_parent_id == 0 else get_parent_id
            new_comment = AppsCommentsModel(
                app_id=app_id,
                text=app_comment,
                parent_id=parent_id,
                user_id=request.user.id,
                is_active=is_staff,
            )
            new_comment.save()
            response = {"success": True}
            return JsonResponse(response)


def comments_reactions(request: HttpRequest):
    """
    Handles reactions (likes and dislikes) to comments.

    Returns the updated like and dislike counts for the comment in JSON format.
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        comment_id = int(data["comment_id"])
        reaction = data["type"]
        print(comment_id, reaction)
        ip = get_ip(request)
        if reaction == "like":
            # Check If User Liked The App Befor Do Nothing
            if AppsCommentsLikeModel.objects.filter(
                ip=ip, comment_id=comment_id
            ).exists():
                response = {
                    "like": AppsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": AppsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }

            else:
                # If User Was Disliked The App Before Delete Dislike & Then Like The App
                if AppsCommentsDisLikeModel.objects.filter(
                    ip=ip, comment_id=comment_id
                ).exists():
                    AppsCommentsDisLikeModel.objects.filter(
                        ip=ip, comment_id=comment_id
                    ).delete()
                AppsCommentsLikeModel.objects.create(ip=ip, comment_id=comment_id)
                response = {
                    "like": AppsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": AppsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }
        elif reaction == "dislike":
            # Check If User Disliked The App Befor Do Nothing
            if AppsCommentsDisLikeModel.objects.filter(
                ip=ip, comment_id=comment_id
            ).exists():
                response = {
                    "like": AppsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": AppsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }
            else:
                # If User Was Liked The App Before Delete Like & Then Dislike The App
                if AppsCommentsLikeModel.objects.filter(
                    ip=ip, comment_id=comment_id
                ).exists():
                    AppsCommentsLikeModel.objects.filter(
                        ip=ip, comment_id=comment_id
                    ).delete()
                AppsCommentsDisLikeModel.objects.create(ip=ip, comment_id=comment_id)
                response = {
                    "like": AppsCommentsLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                    "dislike": AppsCommentsDisLikeModel.objects.filter(
                        comment_id=comment_id
                    ).count(),
                }

    return JsonResponse(response)


class FilterAppByAuthorView(ListView):
    """
    View for filtering applications by a specific author.
    """

    model = ApplicationModel
    template_name = "application/category.html"
    context_object_name = "apps"
    paginate_by = 12

    def get_queryset(self):
        return ApplicationModel.objects.filter(
            is_active=True, author__username=self.kwargs["user"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = Site.objects.get_current()
        site_name = current_site.name
        context["site_name"] = site_name
