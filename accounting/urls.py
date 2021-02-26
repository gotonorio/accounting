"""accounting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register.urls')),
    path('asset_list/', include('asset_list.urls', namespace='asset_list')),
    path('kanrihi_in/', include('kanrihi_in.urls', namespace='kanrihi_in')),
    path('kanrihi_out/', include('kanrihi_out.urls', namespace='kanrihi_out')),
    path('shuuzenhi_in/', include(
        'shuuzenhi_in.urls', namespace='shuuzenhi_in')),
    path('shuuzenhi_out/', include(
        'shuuzenhi_out.urls', namespace='shuuzenhi_out')),
    path('parking_in/', include('parking_in.urls', namespace='parking_in')),
    path('parking_out/', include('parking_out.urls', namespace='parking_out')),
    path('cashier/', include('cashier.urls', namespace='cashier')),
    path('balance/', include('balance.urls', namespace='balance')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
