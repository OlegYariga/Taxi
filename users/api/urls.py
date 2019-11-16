from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path('passenger/sign_up/', views.PhoneVerificationPassengerView.as_view()),
    path('passenger/sign_up/finish/', views.FinishPassengerRegistration.as_view()),
    path('passenger/profile/<int:id>/', views.PassengerUpdate.as_view()),
    path('passenger/sign_in/', views.PassengerLoginView.as_view()),
    path('driver/sign_up/', views.DriverRegistrationView.as_view()),
    path('driver/sign_in/', views.DriverLoginView.as_view()),
    path('verification/', views.PhoneView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('', views.DeleteUserView.as_view()),
]
