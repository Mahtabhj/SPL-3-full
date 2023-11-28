from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from wafrauth import urls as auth_urls
from wafrcloudaccount import urls as cloud_urls
from wafrworkload import urls as workload_urls
from wafrlense import urls as lense_urls
from wafrquestion import urls as question_urls
from wafrreport import urls as reports_urls
from wafrregions import urls as regions_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(auth_urls)),
    path('api/', include(cloud_urls)),
    path('api/lense/', include(lense_urls)),
    path('api/workloads/', include(workload_urls)),
    path('api/questions/', include(question_urls)),
    path('api/reports/', include(reports_urls)),
    path('api/regions/', include(regions_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
