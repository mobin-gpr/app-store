from django.urls import path
from .views import (
    GamesListView,
    ApplicationsListView,
    GamesDetailView,
    ApplicationsDetailView,
    apps_reaction,
    CategoryListView,
    TopAppsView,
    AppsHelpView,
    DownloadAppView,
    add_app_comment,
    AppRequestView,
    comments_reactions,
    FilterAppByAuthorView,
)

urlpatterns = [
    path("games/", GamesListView.as_view(), name="games_list"),
    path("games/<slug:slug>", GamesDetailView.as_view(), name="game_detail"),
    path("applications/", ApplicationsListView.as_view(), name="applications_list"),
    path(
        "applications/<slug:slug>",
        ApplicationsDetailView.as_view(),
        name="application_detail",
    ),
    path("category/<slug:slug>", CategoryListView.as_view(), name="softwares_category"),
    path(
        "category/author/<str:user>",
        FilterAppByAuthorView.as_view(),
        name="filter_app_by_author",
    ),
    path("helps/<slug:slug>", AppsHelpView.as_view(), name="help_detail"),
    path("download/<slug:slug>", DownloadAppView.as_view(), name="download_app"),
    path("tops/", TopAppsView.as_view(), name="top_apps"),
    path("request-app/", AppRequestView.as_view(), name="request_app"),
    path("reactions/", apps_reaction),
    path("ajax/comments/", add_app_comment),
    path("ajax/comments/reactions/", comments_reactions),
]
