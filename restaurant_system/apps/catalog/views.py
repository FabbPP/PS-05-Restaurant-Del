from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.catalog.forms import CategoryForm, ProductForm
from apps.catalog.models import Category, Product


@require_http_methods(["GET"])
def category_list(request):
    data = list(Category.objects.values("id", "name", "description"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = form.save()
        return JsonResponse({"id": category.id, "name": category.name}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


@require_http_methods(["GET"])
def product_list(request):
    data = list(
        Product.objects.select_related("category").values(
            "id", "name", "price", "is_active", "category__id", "category__name"
        )
    )
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def product_create(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        product = form.save()
        return JsonResponse({"id": product.id, "name": product.name}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
