from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("buyback/", include("buyback.urls", namespace="buyback")),
    path("blueprint/", include("blueprint.urls", namespace="blueprint")),
    path("admin/", admin.site.urls),
]
