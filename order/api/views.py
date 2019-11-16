import ast
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from users.api.permissions import PassengerPermission
from .serializers import (
    LastPassengerOrderInfoSerializer,
    OrderCoordsSerializer,
    OrderPriceSerializer, 
    OrderSerializer, 
)
from order.models import Order
from users.models import Taxi
from users.api.serializers import TaxiSerializer


class USSDCallBack(APIView):

    def get(self, request, *args, **kwargs):
        response  = "END What would you want to check \n"
        response += "1. My Account \n"
        response += "2. My phone number"
        return HttpResponse(response) 

    def post(self, request, *args, **kwargs):
        text = request.data.getlist('text')[0]
        response = 'END Try Again'
        if not text:
            response  = "CON What would you want to check \n"
            response += "1. My Account \n"
            response += "2. My phone number"
        elif text == '1':
            response = 'END Ruslan Klimov'
        elif text == '2':
            response = 'END ' + request.data.getlist('phoneNumber')[0]
        return HttpResponse(response) 

class OrderPriceView(APIView):
    serializer_class = OrderPriceSerializer

    def get(self, request):
        serializer = OrderCoordsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    

class OrderCreateView(ListAPIView, CreateAPIView):
    queryset = Order.objects.all()
    permission_classes = (PassengerPermission, )
    serializer_class = OrderSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LastPassengerOrderView(ListAPIView):
    permission_classes = (PassengerPermission, )
    serializer_class = LastPassengerOrderInfoSerializer
    
    def get_queryset(self):
        last = Order.objects.filter(passenger=self.request.user).last()
        if last is not None:
            return [last]
        return []


class OrderRemoveView(DestroyAPIView):
    permission_classes = (PassengerPermission,)

    def get_list_objects(self, arrival, departure, user):
        return get_list_or_404(Order, arrival=arrival, departure=departure, passenger=user)

    def destroy(self, request, *args, **kwargs):
        orders = self.get_list_objects(request.data['arrival'], request.data['departure'], self.request.user)
        for order in orders:
            order.delete()
        return Response({'departure': order.departure, 'arrival': order.arrival, 'status': "deleted"})


class TaxiPriceView(ListAPIView):
    queryset = Taxi.objects.all()
    serializer_class = TaxiSerializer
