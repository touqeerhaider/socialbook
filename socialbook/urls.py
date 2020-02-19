from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from socialbook import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social.urls')),
    path('', RedirectView.as_view(url='social/')),
    path('accounts/', include('registration.backends.default.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)