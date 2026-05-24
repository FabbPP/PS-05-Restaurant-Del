"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('users/', include('apps.users.urls')),
    path('customers/', include('apps.customers.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('dining/', include('apps.dining.urls')),
    path('orders/', include('apps.orders.urls')),
    path('delivery/', include('apps.delivery.urls')),
    path('kitchen/', include('apps.kitchen.urls')),
    path('payments/', include('apps.payments.urls')),
    path('billing/', include('apps.billing.urls')),
]
