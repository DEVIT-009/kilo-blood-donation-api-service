from django.urls import path
from api.securities.auth_view import AuthView  # for admin

urlpatterns = [
    # Admin login
    path("admin/auth/login", AuthView.as_view({'post': 'login_admin'}), name="admin-auth-login"),

    # Public routes mapped manually
    path("public/auth/login", AuthView.as_view({'post': 'login_user'}), name="public-auth-login"),
    path("public/auth/register", AuthView.as_view({'post': 'register_user'}), name="public-auth-register"),
]