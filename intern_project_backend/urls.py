from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
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
    path('checkserver', index, name='index'),
    path('admin/', admin.site.urls),
    #url(r'^auth/obtain_token/', obtain_jwt_token),
    #url(r'^auth/refresh_token/', refresh_jwt_token),
    path('auth/', include('authapp.urls')),

    url(r'^api/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]