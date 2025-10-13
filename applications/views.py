from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.core.cache import cache

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
from utils.mixins import SiteContextMixin, PaginationMixin
from utils.reactions import handle_reaction
from utils.validators import validate_json_request, validate_positive_integer, validate_choice
from .forms import AppRequestForm


class GamesListView(SiteContextMixin, PaginationMixin, ListView):
    """
    View for listing active games.

    Displays all games (group=2) with pagination and category filtering.
    Uses caching for improved performance.
    """

    template_name = "application/games_list.html"
    model = ApplicationModel
    context_object_name = "apps"

    def get_queryset(self):
        """Get active games ordered by ID."""
        return (
            ApplicationModel.objects.filter(is_active=True, group="2")
            .select_related("main_caregory", "author")
            .order_by("-id")
        )

    def get_context_data(self, **kwargs):
        """Add categories to context with caching."""
        context = super().get_context_data(**kwargs)

        # Cache categories for 10 minutes
        cache_key = "game_categories"
        categories = cache.get(cache_key)
        if not categories:
            categories = (
                ApplicationMainCaregoryModel.objects.filter(is_active=True, applicationmodel__group="2")
                .order_by("-id")
                .distinct()
            )
            cache.set(cache_key, categories, 600)

        context["categories"] = categories
        return context


class GamesDetailView(SiteContextMixin, DetailView):
    """
    View for displaying details of a single game.

    Includes:
    - Game details
    - Related suggestions from the same category
    - Paginated comments with replies
    - Help articles
    """

    template_name = "application/game_detail.html"
    model = ApplicationModel
    context_object_name = "app"

    def get_queryset(self):
        """Get active games with related data."""
        return super().get_queryset().filter(is_active=True).select_related("main_caregory", "author")

    def get_context_data(self, **kwargs):
        """Add suggestions, comments, and help articles to context."""
        context = super().get_context_data(**kwargs)
        app_id = self.object.id

        # Get related apps from same category
        context["suggestions"] = (
            ApplicationModel.objects.filter(is_active=True, main_caregory=self.object.main_caregory)
            .exclude(id=app_id)
            .select_related("main_caregory")[:6]
        )

        # Get comments with pagination
        comments = (
            AppsCommentsModel.objects.filter(is_active=True, app_id=app_id, parent=None)
            .select_related("user", "user__avatar")
            .prefetch_related("replies__user", "replies__user__avatar")
        )

        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get("page", 1)

        try:
            page_obj = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        context.update(
            {
                "cat_link": self.object,
                "helps": AppsHelpModel.objects.filter(is_active=True).only("id", "title", "slug"),
                "user": self.request.user if self.request.user.is_authenticated else None,
                "comments": page_obj,
                "comments_count": comments.count(),
            }
        )

        return context


class ApplicationsListView(SiteContextMixin, PaginationMixin, ListView):
    """
    View for listing active applications.

    Displays all applications (group=1) with pagination and category filtering.
    Uses caching for improved performance.
    """

    template_name = "application/applications_list.html"
    model = ApplicationModel
    context_object_name = "apps"

    def get_queryset(self):
        """Get active applications ordered by ID."""
        return (
            ApplicationModel.objects.filter(is_active=True, group="1")
            .select_related("main_caregory", "author")
            .order_by("-id")
        )

    def get_context_data(self, **kwargs):
        """Add categories to context with caching."""
        context = super().get_context_data(**kwargs)

        # Cache categories for 10 minutes
        cache_key = "app_categories"
        categories = cache.get(cache_key)
        if not categories:
            categories = (
                ApplicationMainCaregoryModel.objects.filter(is_active=True, applicationmodel__group="1")
                .order_by("-id")
                .distinct()
            )
            cache.set(cache_key, categories, 600)

        context["categories"] = categories
        return context


class ApplicationsDetailView(SiteContextMixin, DetailView):
    """
    View for displaying details of a single application.

    Includes:
    - Application details
    - Related suggestions from the same category
    - Paginated comments with replies
    - Help articles
    """

    template_name = "application/application_detail.html"
    model = ApplicationModel
    context_object_name = "app"

    def get_queryset(self):
        """Get active applications with related data."""
        return super().get_queryset().filter(is_active=True).select_related("main_caregory", "author")

    def get_context_data(self, **kwargs):
        """Add suggestions, comments, and help articles to context."""
        context = super().get_context_data(**kwargs)
        app_id = self.object.id

        # Get related apps from same category
        context["suggestions"] = (
            ApplicationModel.objects.filter(is_active=True, main_caregory=self.object.main_caregory)
            .exclude(id=app_id)
            .select_related("main_caregory")[:6]
        )

        # Get comments with pagination
        comments = (
            AppsCommentsModel.objects.filter(is_active=True, app_id=app_id, parent=None)
            .select_related("user", "user__avatar")
            .prefetch_related("replies__user", "replies__user__avatar")
        )

        paginator = Paginator(comments, 10)
        page_number = self.request.GET.get("page", 1)

        try:
            page_obj = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        context.update(
            {
                "cat_link": self.object,
                "helps": AppsHelpModel.objects.filter(is_active=True).only("id", "title", "slug"),
                "user": self.request.user if self.request.user.is_authenticated else None,
                "comments": page_obj,
                "comments_count": comments.count(),
            }
        )

        return context


def apps_reaction(request: HttpRequest):
    """
    Handle like/dislike reactions for applications.

    Expects POST request with JSON body containing:
    - app_id: ID of the application
    - type: 'like' or 'dislike'

    Returns:
        JSON response with updated like and dislike counts
    """
    try:
        # Validate request
        data = validate_json_request(request, required_fields=["app_id", "type"])
        app_id = validate_positive_integer(data["app_id"], "app_id")
        reaction_type = validate_choice(data["type"], ["like", "dislike"], "type")

        # Get user IP
        ip = get_ip(request)

        # Handle reaction with utility function
        success, counts = handle_reaction(
            ip=ip,
            object_id=app_id,
            reaction_type=reaction_type,
            like_model=AppsLikesModel,
            dislike_model=AppsDisLikesModel,
            field_name="app",
        )

        return JsonResponse(
            {
                "success": success,
                "likes": counts["likes"],
                "dislikes": counts["dislikes"],
            }
        )

    except ValidationError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    except Exception:
        return JsonResponse({"success": False, "error": "An error occurred"}, status=500)


class CategoryListView(SiteContextMixin, PaginationMixin, ListView):
    """
    View to display apps filtered by category.

    Shows all applications (both apps and games) that belong to a specific category.
    Includes pagination and related categories for navigation.
    """

    model = ApplicationModel
    template_name = "application/category.html"
    context_object_name = "apps"

    def get_queryset(self):
        """Get active apps in the specified category."""
        return ApplicationModel.objects.filter(is_active=True, main_caregory__slug=self.kwargs["slug"]).select_related(
            "main_caregory", "author"
        )

    def get_context_data(self, **kwargs):
        """Add category information and all categories to context."""
        context = super().get_context_data(**kwargs)

        # Get category for display (use first app's category to avoid extra query)
        queryset = self.get_queryset()
        context["category"] = queryset.first()

        # Cache all categories for 10 minutes
        cache_key = "all_categories"
        categories = cache.get(cache_key)
        if not categories:
            categories = ApplicationMainCaregoryModel.objects.filter(is_active=True).order_by("-id")
            cache.set(cache_key, categories, 600)

        context["categories"] = categories
        return context


class TopAppsView(SiteContextMixin, ListView):
    """
    View for displaying top applications based on like count.

    Shows the top 100 most-liked applications and games.
    Uses aggregation for efficient counting and caching for performance.
    """

    template_name = "application/top.html"
    model = ApplicationModel
    context_object_name = "apps"

    def get_queryset(self):
        """Get top 100 apps ordered by like count."""
        # Cache top apps for 5 minutes
        cache_key = "top_apps_list"
        top_apps = cache.get(cache_key)

        if not top_apps:
            top_apps = (
                ApplicationModel.objects.filter(is_active=True)
                .select_related("main_caregory", "author")
                .annotate(like_count=Count("appslikesmodel"))
                .order_by("-like_count")[:100]
            )
            cache.set(cache_key, top_apps, 300)

        return top_apps


class AppsHelpView(View):
    """
    View for displaying help/tutorial pages.

    Shows detailed help articles for users about app installation,
    usage, or other topics.
    """

    def get(self, request, slug):
        """Display a specific help article."""
        help_article = get_object_or_404(AppsHelpModel, slug=slug, is_active=True)
        return render(request, "application/help.html", {"help": help_article})


class DownloadAppView(View):
    """
    View for handling application downloads.

    Displays download page with authentication check.
    Shows different content for authenticated vs anonymous users.
    """

    def get(self, request, slug):
        """Display download page for a specific app version."""
        link = get_object_or_404(ApplicationLinkModel.objects.select_related("application"), is_active=True, slug=slug)

        context = {
            "link": link,
            "check_auth": request.user.is_authenticated,
        }
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
                if not AppRequestModel.objects.filter(app_link=app_link, user=user).exists():
                    AppRequestModel.objects.create(user=user, app_link=app_link)
                    messages.success(request, "درخواست شما با موفقیت ثبت شد")
                else:
                    form.add_error("app_link", "شما قبلاً برای این اپلیکیشن درخواست ارسال کرده اید.")
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
    Add a new comment to an application.

    Expects POST request with JSON body containing:
    - app_id: ID of the application
    - app_comment: Comment text
    - parent_id: ID of parent comment (0 for top-level comments)

    Requires authentication.

    Returns:
        JSON response indicating success/failure
    """
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Authentication required"}, status=401)

    try:
        # Validate request
        data = validate_json_request(request, required_fields=["app_id", "app_comment", "parent_id"])
        app_id = validate_positive_integer(data["app_id"], "app_id")
        comment_text = data["app_comment"].strip()
        parent_id = int(data["parent_id"]) or None

        # Validate comment text
        if not comment_text or len(comment_text) < 3:
            raise ValidationError("Comment must be at least 3 characters long")

        if len(comment_text) > 1000:
            raise ValidationError("Comment must be less than 1000 characters")

        # Create comment
        AppsCommentsModel.objects.create(
            app_id=app_id,
            text=comment_text,
            parent_id=parent_id,
            user_id=request.user.id,
            is_active=request.user.is_staff,  # Auto-approve for staff
        )

        return JsonResponse({"success": True})

    except ValidationError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    except Exception:
        return JsonResponse({"success": False, "error": "An error occurred"}, status=500)


def comments_reactions(request: HttpRequest):
    """
    Handle like/dislike reactions for comments.

    Expects POST request with JSON body containing:
    - comment_id: ID of the comment
    - type: 'like' or 'dislike'

    Returns:
        JSON response with updated like and dislike counts
    """
    try:
        # Validate request
        data = validate_json_request(request, required_fields=["comment_id", "type"])
        comment_id = validate_positive_integer(data["comment_id"], "comment_id")
        reaction_type = validate_choice(data["type"], ["like", "dislike"], "type")

        # Get user IP
        ip = get_ip(request)

        # Handle reaction with utility function
        success, counts = handle_reaction(
            ip=ip,
            object_id=comment_id,
            reaction_type=reaction_type,
            like_model=AppsCommentsLikeModel,
            dislike_model=AppsCommentsDisLikeModel,
            field_name="comment",
        )

        return JsonResponse(
            {
                "success": success,
                "likes": counts["likes"],
                "dislikes": counts["dislikes"],
            }
        )

    except ValidationError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    except Exception:
        return JsonResponse({"success": False, "error": "An error occurred"}, status=500)


class FilterAppByAuthorView(SiteContextMixin, PaginationMixin, ListView):
    """
    View for filtering applications by author/publisher.

    Displays all applications published by a specific user.
    Useful for browsing all apps from a trusted developer.
    """

    model = ApplicationModel
    template_name = "application/category.html"
    context_object_name = "apps"

    def get_queryset(self):
        """Get active apps by specific author."""
        return ApplicationModel.objects.filter(is_active=True, author__username=self.kwargs["user"]).select_related(
            "main_caregory", "author"
        )

    def get_context_data(self, **kwargs):
        """Add author information to context."""
        context = super().get_context_data(**kwargs)
        context["author_username"] = self.kwargs["user"]
        return context
