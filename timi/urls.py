from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/app/", include("user_forms.urls")),
    path("api/user/", include("timi_app.urls")),
]
