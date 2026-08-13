"""
URL configuration for Social_Media project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('app/',include('social_login.urls')), 
    path('accounts/', include('allauth.urls')),

    path('', include('apps.Account.urls')),
    path('posts/', include('apps.posts.urls')),
    path('notifications/',include('apps.Notifications.urls')),
    path('stories/',include('apps.Stories.urls')),
    path('comments/',include('apps.comments.urls')),
    path("payment/",include("apps.payments.urls")),

    
    path('api/', include(('apps.Account.api.urls', 'Account'), namespace='account_api')),
    path('posts/api/', include(('apps.posts.api.urls', 'posts'), namespace='posts_api')),
    path('stories/api/', include(('apps.Stories.api.urls', 'Stories'), namespace='stories_api')),
    path('comments/api/', include(('apps.comments.api.urls', 'comments_api'), namespace='comments_api')),
    path('Notifications/api/', include(('apps.Notifications.api.urls', 'Notifications_api'), namespace='Notifications_api')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

 

    
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )




