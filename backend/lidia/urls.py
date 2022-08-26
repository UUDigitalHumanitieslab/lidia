from django.conf import settings
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import RedirectView

from rest_framework import routers

from .index import index
from .proxy_frontend import proxy_frontend

from example.views import hooray as ExampleView  # DELETEME, see below
from annotations.views import post_annotation_view

api_router = routers.DefaultRouter()  # register viewsets with this router


if settings.PROXY_FRONTEND:
    spa_url = re_path(r'^(?P<path>.*)$', proxy_frontend)
else:
    spa_url = re_path(r'', index)

urlpatterns = [
    path('api/example/', ExampleView),
    path('api/post-annotation/', post_annotation_view),
    path('admin', RedirectView.as_view(url='/admin/', permanent=True)),
    path('api', RedirectView.as_view(url='/api/', permanent=True)),
    path('api-auth', RedirectView.as_view(url='/api-auth/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework',
    )),
    spa_url,  # catch-all; unknown paths to be handled by a SPA
]
