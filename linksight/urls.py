from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('registration.backends.admin_approval.urls')),
    path('api/', include('linksight.api.urls')),
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

handler500 = 'rest_framework.exceptions.server_error'
