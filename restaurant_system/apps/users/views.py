from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.users.forms import UserRegisterForm
from apps.users.models import User


@require_http_methods(["GET"])
def user_list(request):
    data = list(User.objects.values("id", "username", "email", "role", "is_active"))
    return JsonResponse({"items": data})


@require_http_methods(["POST"])
def user_create(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        return JsonResponse({"id": user.id, "username": user.username}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)

# Create your views here.
