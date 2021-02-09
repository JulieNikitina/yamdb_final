from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()
v1_router.register("users", views.UserViewSet)

urlpatterns = [
    path("v1/", include(v1_router.urls)),
    path("v1/auth/email/", views.send_confirmation_code),
    path("v1/auth/token/", views.send_token),
]
