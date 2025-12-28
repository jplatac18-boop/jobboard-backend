# jobboard_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings

import users.views

urlpatterns = [
    # Admin en ruta no trivial
    path("super-panel-2025/", admin.site.urls),

    # Auth
    path(
        "api/auth/register/",
        users.views.RegisterView.as_view(),
        name="auth-register",
    ),
    path(
        "api/auth/login/",
        users.views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/auth/me/",
        users.views.MeView.as_view(),
        name="auth-me",
    ),

    # Resto de APIs
    path("api/", include("jobs.urls")),
    path("api/", include("applications.urls")),
    path("api/", include("companies.urls")),
]

# Debug toolbar solo en desarrollo
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
