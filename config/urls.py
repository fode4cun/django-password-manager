from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('layout.urls')),
    path('', include('pwdgen.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'layout.views.response_error_400'
handler403 = 'layout.views.response_error_403'
handler404 = 'layout.views.response_error_404'
handler500 = 'layout.views.response_error_500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
