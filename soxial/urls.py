"""soxial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps URLS
    path('', include('home.urls')),
    path('profile/', include('profiles.urls')),
    path('api/v1/profile/', include('profiles.api.urls')),
    path('api/v1/post/', include('posts.api.urls')),
    path('api/v1/friends/', include('friends.api.urls')),
    
    # DJRESTAUTH
    # path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/api/v1/account/', include('dj_rest_auth.urls')),
    path('rest-auth/api/v1/registration/', include('dj_rest_auth.registration.urls')),   

    # AllAuth
    path('account/', include('allauth.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls import url
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
        
    schema_view = get_schema_view(
    openapi.Info(
        title="Soxial API",
        default_version='v1',
        description="Web API for Soxial Api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soxial@email.local"),
        license=openapi.License(name="Private License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    )
    
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ] + urlpatterns
