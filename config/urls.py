from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("cuentas.urls")),
    path("mentorias/", include("mentorias.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Mentoría entre Estudiantes"
admin.site.site_title = "Administración"
admin.site.index_title = "Panel de administración"
