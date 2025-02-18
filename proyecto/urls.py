from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Pruebas unitarias",
        license=openapi.License(name="BSD License")
    ),
    public=True,
    # permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('inventory.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc")
]
