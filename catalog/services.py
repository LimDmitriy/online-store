from catalog.models import Product
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def get_products_from_cache(category_id):
    if not CACHE_ENABLED:
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()
    key = "products_all" if category_id is None else f"products_category_{category_id}"
    products = cache.get(key)
    if products is not None:
        return products

    queryset = Product.objects.all()
    if category_id:
        queryset = queryset.filter(category_id=category_id)

    products = list(queryset)

    cache.set(key, products, timeout=10 * 60)

    return products
