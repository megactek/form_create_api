from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormView, FormInputView

app_name = "app"
router = DefaultRouter(trailing_slash=True)
router.register("forms", FormView, "forms")
router.register("inputs", FormInputView, "inputs")

urlpatterns = [path("", include(router.urls))]
