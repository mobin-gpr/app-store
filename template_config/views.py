from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from applications.models import ApplicationModel, AppsHelpModel
from settings.models import FooterModel, LogoModel
from .forms import SearchForm


class NavbarPartialView(View):
    """
    View to render the navigation bar, including user authentication status and search form.
    """

    def get(self, request):
        """
        Handles GET requests to render the navigation bar with guides and user information.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Rendered HTML template for the navigation bar.
        """
        guides = AppsHelpModel.objects.filter(is_active=True)
        user = request.user if request.user.is_authenticated else None
        form = SearchForm()
        logo = LogoModel.objects.filter(is_active=True).first()
        context = {
            "user": user,
            "check_auth": request.user.is_authenticated,
            "form": form,
            "guides": guides,
            "logo": logo,
        }
        return render(request, "_base_components/navbar.html", context)

    def post(self, request):
        """
        Handles POST requests to render the navigation bar with the search form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Rendered HTML template for the navigation bar.
        """
        user = request.user if request.user.is_authenticated else None
        form = SearchForm()
        logo = LogoModel.objects.filter(is_active=True).first()
        context = {
            "user": user,
            "check_auth": request.user.is_authenticated,
            "form": form,
            "logo": logo,
        }
        return render(request, "_base_components/navbar.html", context)


def footer_partial(request):
    """
    Renders the footer partial template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template for the footer.
    """
    footer = FooterModel.objects.filter(is_active=True).first()
    logo = LogoModel.objects.filter(is_active=True).first()
    context = {
        "footer": footer,
        "logo": logo,
    }

    return render(request, "_base_components/footer.html", context)


class SearchView(ListView):
    """
    View to handle search functionality and display search results for applications.
    """

    template_name = "template_config/search.html"
    model = ApplicationModel
    context_object_name = "objects"

    def get_queryset(self):
        """
        Retrieves a filtered queryset based on the search query parameter.

        Filters `ApplicationModel` objects by title, content, or category.

        Returns:
            QuerySet: Filtered queryset of application models.
        """
        query = self.request.GET.get("search")
        get_object = ApplicationModel.objects.filter(is_active=True)
        objects = get_object.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(main_caregory__category__icontains=query)
        )
        return objects


def custom_404_error(request, exception):
    """
    Custom 404 error handler.

    Args:
        request (HttpRequest): The HTTP request object.
        exception (Exception): The exception that triggered the 404 error.

    Returns:
        HttpResponse: Rendered HTML template for the 404 error page.
    """
    return render(request, "404.html", status=404)


class RobotTXT(TemplateView):
    """
    View to serve the robots.txt file.
    """

    template_name = "Robots.txt"
    content_type = "text/plain"
