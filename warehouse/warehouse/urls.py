from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from . import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Warehouse API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('warehouse/admin/', admin.site.urls),
    path('warehouse/api/v1/', include('api.urls')),

    re_path(r'^warehouse/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^warehouse/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^warehouse/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]