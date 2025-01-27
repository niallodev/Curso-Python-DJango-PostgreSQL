"""
URL configuration for gym_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('pages.urls', 'pages'), namespace='pages')),
    path('users/', include(('users.urls', 'users'), namespace='users')),  # Las URLs de la app users
    path('classes/', include(('classes.urls', 'classes'), namespace='classes')),  # Las URLs de la app classes
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),  # Las URLs de la app payments
    path('memberships/', include(('memberships.urls', 'memberships'), namespace='memberships')),  # Las URLs de la app memberships
    path('routines/', include(('routines.urls', 'routines'), namespace='routines')),  # Las URLs de la app routines
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)