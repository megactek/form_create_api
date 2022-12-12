from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RegisterView, UpdateUserView, UserProfile

app_name = "user"
router = DefaultRouter(trailing_slash=True)
router.register("login", LoginView, "login")
router.register("signup", RegisterView, "signup")
router.register("update_user", UpdateUserView, "update_user")
router.register("profile", UserProfile, "profile")


urlpatterns = [
    path("", include(router.urls)),
]
