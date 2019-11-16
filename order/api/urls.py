from django.urls import path
from order.api import views


urlpatterns = [
    path('passenger/', views.OrderCreateView.as_view()),
    path('passenger/last/', views.LastPassengerOrderView.as_view()),
    path('taxi/', views.TaxiPriceView.as_view()),
    path('price/', views.OrderPriceView.as_view()),
    path('remove_order/', views.OrderRemoveView.as_view())
]
