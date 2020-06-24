from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# TEMP for file serving
from django.conf.urls.static import static
from django.conf import settings

# project import
from intern_project_backend.views import index

# swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Swagger API",
      default_version='v1.420',
      description="glhf",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('sop/', include('sop.urls')),
    path('checkserver', index, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # TEMP for file serving