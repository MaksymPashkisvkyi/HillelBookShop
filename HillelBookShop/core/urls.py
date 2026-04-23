"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from payments.views import checkout_view

urlpatterns = ([
    path('', include('shop.urls'), name='shop'),
    path('pages/', include('pages.urls'), name='pages'),
    path('admin/', admin.site.urls, name='admin'),
    path('account/', include('accounts.urls'), name='account'),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
    path('payments/', include('payments.urls'), name='payments'),
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/<int:order_id>', checkout_view, name='checkout_order'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()