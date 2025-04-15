from django.contrib import admin
from django.urls import path, include
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Minha API",
        default_version='v1',
        description="Documentação da API",
        terms_of_service="https://www.seusite.com/termos/",
        contact=openapi.Contact(email="seuemail@exemplo.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/organization/', include('organization.urls')),  # Inclui as rotas da organização
    path('api/user/', include('duser.urls')),  # Inclui as rotas do investidor
    path('api/announcement/', include('announcements.urls')),
    path('api/property/', include('property.urls')),
    path('api/property-media/', include ('property_media.urls')),
    path('api/property-roi/', include('property_roi.urls')),
    path('api/roles/', include('roles.urls')),  # 👈 Add this line


]
