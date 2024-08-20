from django.urls import path
from .views import (
    NewsListView,
    NewsDetailView,
    news_reaction,
    NewsCategoryListView,
    add_news_comment,
    news_comments_reactions,
    FilterNewsByAuthorView,
)

urlpatterns = [
    path("", NewsListView.as_view(), name="news_list"),
    path("<slug:slug>/", NewsDetailView.as_view(), name="news_detail"),
    path("category/<slug:slug>/", NewsCategoryListView.as_view(), name="news_category"),
    path(
        "category/author/<str:user>/",
        FilterNewsByAuthorView.as_view(),
        name="filter_news_by_author",
    ),
    path("ajax/reactions/", news_reaction),
    path("ajax/comments/", add_news_comment),
    path("ajax/comments/reactions/", news_comments_reactions),
]
