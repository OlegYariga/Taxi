from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from ussd_taxi.settings import AUTHY_API
from rest_framework.views import APIView
from rest_framework.response import Response
from users.api.serializers import (
    PassengerRegistrationSerializer, 
    FinishRegistrationSerializer,
    DriverRegistrationSerializer, 
    PhoneVerificationSerializer,
    PassengerProfileSerializer,
    PassengerLoginSerializer,
    DriverLoginSerializer,
    PhoneSerializer, 
    UserSerializer,
    TaxiSerializer, 
)
from users.api.permissions import (
    BaseUserPermission,
    PassengerPermission, 
    DriverPermission,
)
from users.models import Passenger, Driver, Taxi, User
from authy.api import AuthyApiClient 

authy_api = AuthyApiClient(AUTHY_API)


class TaxiListView(ListAPIView):
    permission_classes = (BaseUserPermission, )
    serializer_class = TaxiSerializer
    queryset = Taxi.objects.all()


class PassengerLoginView(APIView):
    serializer_class = PassengerLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        check = authy_api.phones.verification_check(request.data['phone'], request.data['country_code'], request.data['code'])
        if check.ok():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': check.response.json()['message']}, status=check.response.status_code)            


class DriverLoginView(APIView):
    serializer_class = DriverLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        check = authy_api.phones.verification_check(request.data['phone'], request.data['country_code'], request.data['code'])
        if check.ok():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': check.response.json()['message']}, status=check.response.status_code)            


class DriverRegistrationView(APIView):
    serializer_class = DriverRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = serializer.save()
        return Response(driver, status=status.HTTP_201_CREATED)


class PassengerRegistrationView(APIView):
    serializer_class = PassengerRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        check = authy_api.phones.verification_check(serializer.validated_data['phone'], 7, serializer.validated_data['code'])
        if check.ok():
            passenger = serializer.save()
            return Response(passenger, status=status.HTTP_201_CREATED)
        return Response({'detail': check.response.json()['message']}, status=check.response.status_code)            
            

class PhoneView(APIView):
    serializer_class = PhoneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = authy_api.phones.verification_start(phone_number=request.data['phone'], country_code=request.data['country_code'], via='sms')
        if res.ok():
            return Response(serializer.data)
        return Response({'detail': res.response.json()['message']}, status=res.response.status_code)            


class PhoneVerificationPassengerView(APIView):
    serializer_class = PhoneVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        if Passenger.objects.filter(phone=phone).exists():
            return Response({'detail': 'user already exist'}, status=status.HTTP_400_BAD_REQUEST)
        check = authy_api.phones.verification_check(phone, request.data['country_code'], request.data['code'])
        if check.ok():
            passenger = Passenger.objects.create_passenger(phone)
            return Response({'detail': 'user has been create', 'id': passenger.id}, status=status.HTTP_201_CREATED)
        return Response({'detail': check.response.json()['message']}, status=check.response.status_code)            


class PassengerUpdate(UpdateAPIView,
                      UpdateModelMixin,
                      RetrieveAPIView,
                      RetrieveModelMixin):
    permission_classes = (PassengerPermission,)
    serializer_class = PassengerProfileSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        passenger = self.get_queryset()
        serializer = self.get_serializer(self.get_queryset(), data=request.data)
        serializer.is_valid(raise_exception=True)
        passenger = serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        return get_object_or_404(Passenger, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        passenger = self.get_queryset()
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data)
        

class PassengerInfo(RetrieveAPIView):
    permission_classes = (PassengerPermission, )
    serializer_class = PassengerProfileSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return get_object_or_404(Passenger, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        passenger = self.get_queryset()
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data)



class FinishPassengerRegistration(APIView):
    serializer_class = FinishRegistrationSerializer

    def put(self, request, *args, **kwargs):
        serializer = FinishRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class PhoneVerificationDriverView(APIView):
    pass


class DeleteUserView(APIView,
                     DestroyModelMixin):
    serializer_class = UserSerializer

    def get_object(self, phone):
        return get_object_or_404(User, phone=phone)

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object(request.data['phone'])
        user.delete()
        return Response({'detail': 'user delete'})

