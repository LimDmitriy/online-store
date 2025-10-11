from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .services import get_products_from_cache
from catalog.models import Product, Category
from .forms import ProductForm, ProductModeratorForm


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"

    def get_queryset(self):
        products = cache.get("products_all")
        if products is None:
            products = list(super().get_queryset())
            cache.set("products_all", products, 60 * 10)  # 10 минут
        return products


class ProductByCategoryView(ListView):
    model = Product
    template_name = "catalog/products_by_category.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return get_products_from_cache(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        context["category"] = Category.objects.get(pk=category_id)
        return context

class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.user != product.owner:
            return HttpResponseForbidden(
                "У вас нет прав для редактирования этого продукта."
            )

        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("catalog:product_detail", pk=pk)
        return render(request, "catalog/product_form.html", {"form": form})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not (
            obj.owner == self.request.user
            or self.request.user.has_perm("catalog.can_unpublish_product")
        ):
            raise Http404("У вас нет прав на удаление этого продукта.")
        return obj


class ProductModerateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductModeratorForm
    template_name = "catalog/product_moderate.html"
    permission_required = "catalog.can_unpublish_product"
    success_url = reverse_lazy("catalog:product_list")
