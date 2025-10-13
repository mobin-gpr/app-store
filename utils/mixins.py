"""
Common mixins and utility classes for views.

This module provides reusable mixins that can be used across different views
to avoid code duplication and maintain consistency.
"""

from django.contrib.sites.models import Site
from django.core.cache import cache


class SiteContextMixin:
    """
    Mixin to add site information to the context.

    This mixin automatically adds the current site name to the context,
    which is commonly needed across multiple views.
    """

    def get_site_name(self):
        """Get the current site name with caching."""
        site_name = cache.get("site_name")
        if not site_name:
            try:
                site_name = Site.objects.get_current().name
                cache.set("site_name", site_name, 3600)  # Cache for 1 hour
            except Exception:
                site_name = "App Store"
        return site_name

    def get_context_data(self, **kwargs):
        """Add site name to context."""
        context = super().get_context_data(**kwargs)
        context["site_name"] = self.get_site_name()
        return context


class PaginationMixin:
    """
    Standard pagination configuration mixin.

    This mixin provides consistent pagination settings across views.
    """

    paginate_by = 12

    def get_paginate_by(self, queryset):
        """Allow dynamic pagination override."""
        return self.request.GET.get("per_page", self.paginate_by)
