"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers #viewsets, serializers
from rest_framework.documentation import include_docs_urls

from hyperion.views import user_views, auth_views, post_views

# Routers provide a way of automatically determining the URL conf.
# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', user_views.UserViewSet)
router.register(r'groups', user_views.GroupViewSet)

# https://stackoverflow.com/a/51659083
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth', csrf_exempt(auth_views.AuthView.as_view())),
    path('admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='API Documentation')),

    path('author/posts', post_views.PostViewSet.as_view(
        {'get': 'get_auth_posts',
         'post': 'create',
        }
    )),
    path('posts', post_views.PostViewSet.as_view({'get': 'list'})),
    path('posts/<int:pk>', post_views.PostViewSet.as_view({'get': 'retrieve'})),
]
# pylint: enable=invalid-name
