from rest_framework import serializers
from order.api.utils import calculate_distance
from order.models import (
    Order,
    ArrivalCoord,
    DepartureCoord,
)
from users.models import Taxi
from users.api.serializers import TaxiSerializer

class ArrivalCoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalCoord
        fields = ('latitude', 'longitude')
        extra_kwargs = {
            'latitude': {'write_only': True},
            'longitude': {'write_only': True},
        }


class ArrivalCoordReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalCoord
        fields = ('latitude', 'longitude')


class DepartureCoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartureCoord
        fields = ('latitude', 'longitude')
        extra_kwargs = {
            'latitude': {'write_only': True},
            'longitude': {'write_only': True},
        }

class DepartureCoordReadOnlySerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = DepartureCoord
        fields = ('latitude', 'longitude')


class OrderCoordsSerializer(serializers.Serializer):
    arrival_lat = serializers.FloatField(write_only=True)
    departure_lat = serializers.FloatField(write_only=True)
    arrival_lng = serializers.FloatField(write_only=True)
    departure_lng = serializers.FloatField(write_only=True)
    taxi = serializers.CharField(max_length=10, write_only=True)
    price = serializers.IntegerField(read_only=True)

    def validate(self, data):
        # TODO: make request to GOOGLE API and calculate distance
        taxi = data.pop('taxi')
        distance = calculate_distance(**data)
        return {'price': distance * taxi.price}

    def validate_taxi(self, taxi):
        taxi_obj = Taxi.objects.filter(type=taxi) 
        if not taxi_obj.exists():
            raise serializers.ValidationError('Taxi not exists')
        return taxi_obj.first()


class OrderPriceSerializer(serializers.Serializer):
    arrival_coords = ArrivalCoordSerializer(write_only=True)
    departure_coords = DepartureCoordSerializer(write_only=True)
    taxi = serializers.CharField(max_length=10, write_only=True)
    price = serializers.IntegerField(read_only=True)

    def validate(self, validated_data):
        return validated_data


class OrderSerializer(serializers.ModelSerializer):
    arrival_coords = ArrivalCoordSerializer(write_only=True)
    departure_coords = DepartureCoordSerializer(write_only=True)
    taxi = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = Order
        fields = ('arrival', 'arrival_coords', 'departure', 'departure_coords', 
                  'taxi', 'payment_type', 'status', 'price')
        read_only_fields = ('status', 'price')

    def create(self, validated_data):
        user = self.context['user']
        departure_coords = DepartureCoord.objects.create(**validated_data['departure_coords'])
        arrival_coords = ArrivalCoord.objects.create(**validated_data['arrival_coords'])
        price = validated_data['taxi'].price * 50
        validated_data.pop('departure_coords')
        validated_data.pop('arrival_coords')
        return Order.objects.create(arrival_coords=arrival_coords, 
                                    departure_coords=departure_coords,
                                    passenger=user.passenger,
                                    price=price,
                                    **validated_data)
    
    def validate_taxi(self, taxi):
        taxi_obj = Taxi.objects.filter(type=taxi) 
        if not taxi_obj.exists():
            raise serializers.ValidationError('Taxi not exists')
        return taxi_obj.first()


class LastPassengerOrderInfoSerializer(serializers.ModelSerializer):
    arrival_coords = ArrivalCoordReadOnlySerializer(read_only=True)
    departure_coords = DepartureCoordReadOnlySerilizer(read_only=True)
    taxi = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('arrival', 'arrival_coords', 'departure', 'departure_coords', 
                  'taxi', 'payment_type', 'price')
        read_only_fields = ('status', 'price', 'payment_type', 'arrival', 'departure')

    def get_taxi(self, obj):
        return obj.taxi.type