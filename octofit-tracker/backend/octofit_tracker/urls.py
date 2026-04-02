"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'workouts', views.WorkoutViewSet)
router.register(r'leaderboard', views.LeaderboardViewSet)

@api_view(['GET'])
def api_root(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev/api/"
    else:
        # fallback to localhost for local development
        base_url = request.build_absolute_uri('/')
        if not base_url.endswith('/'):
            base_url += '/'
        base_url += 'api/' if not base_url.endswith('api/') else ''
    return Response({
        'users': f"{base_url}users/",
        'teams': f"{base_url}teams/",
        'activities': f"{base_url}activities/",
        'workouts': f"{base_url}workouts/",
        'leaderboard': f"{base_url}leaderboard/",
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
    path('schema/', get_schema_view(title="Octofit Tracker API"), name='openapi-schema'),
    path('docs/', include_docs_urls(title='Octofit Tracker API')),
]
