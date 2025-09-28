from django.urls import path
from blog.apps import BlogConfig
from django.conf import settings
from django.conf.urls.static import static
from blog.views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
)

app_name = BlogConfig.name

urlpatterns = [
    path("blogs/list/", ArticleListView.as_view(), name="article_list"),
    path("blogs/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("blogs/create/", ArticleCreateView.as_view(), name="article_create"),
    path("blogs/<int:pk>/update/", ArticleUpdateView.as_view(), name="article_update"),
    path("blogs/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
