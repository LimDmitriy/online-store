from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductModerateView, ProductByCategoryView,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path(
        "catalog/<int:pk>",
        cache_page(60)(ProductDetailView.as_view()),
        name="product_detail",
    ),
    path("catalog/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "catalog/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "catalog/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path("<int:pk>/moderate/", ProductModerateView.as_view(), name="product_moderate"),
    path("category/<int:category_id>/", ProductByCategoryView.as_view(), name="product_category"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
