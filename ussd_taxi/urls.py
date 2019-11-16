from django.contrib import admin
from django.urls import path, include
from users.api.views import TaxiListView
from order.api.views import USSDCallBack


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.api.urls')),
    path('api/v1/taxi/', TaxiListView.as_view()),
    path('', USSDCallBack.as_view()),
    path('api/v1/orders/', include('order.api.urls')),
]
