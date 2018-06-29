from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

api = []

apps = settings.APPS

for app_name in apps:
    try:
        api.append(
            url(r'^' + app_name + '/', include(app_name + '.build.urls')))
    except ImportError:
        pass

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
