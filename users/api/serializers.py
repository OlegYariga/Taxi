from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import (
    Driver,
    Passenger,
    Taxi,
    User,
)


class TaxiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Taxi
        fields = ('type', 'price')


class DriverRegistrationSerializer(serializers.ModelSerializer):
    taxi = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = Driver
        fields = ('name', 'email', 'phone', 'taxi')
    
    def create(self, validated_data):
        driver = Driver.objects.create_driver(**validated_data)
        refresh = RefreshToken.for_user(driver)
        user_details = dict()
        user_details['user'] = {'id': driver.id, 
                                'name': driver.name, 
                                'email': driver.email, 
                                'phone': driver.phone}
        return user_details

    def validate_taxi(self, taxi):
        taxi_obj = Taxi.objects.filter(type=taxi) 
        if not taxi_obj.exists():
            raise serializers.ValidationError('Such type of taxi not exists')
        return taxi_obj.first()


class PassengerRegistrationSerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=4, max_length=4)

    class Meta:
        model = Passenger
        fields = ('name', 'email', 'phone', 'code')
        read_only_fields = ('code', ) 

    def create(self, validated_data):
        validated_data.pop('code')
        passenger = Passenger.objects.create_passenger(**validated_data)
        refresh = RefreshToken.for_user(passenger)
        user_details = dict()
        user_details['user'] = {'id': passenger.id, 'name': passenger.name, 'email': passenger.email, 'phone': passenger.phone}
        user_details['refresh'] = str(refresh)
        user_details['access'] = str(refresh.access_token)
        return user_details

    def validate_code(self, code):
        if not str(code).isdigit():
            raise serializers.ValidationError({'code': 'Code must contain only digits'})
        return code


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('id', 'name', 'email', 'phone')


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'name', 'email', 'phone', 'is_confirmed')


class PassengerLoginSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4, max_length=4, write_only=True)
    country_code = serializers.CharField(max_length=5, write_only=True)
    phone = serializers.CharField(max_length=17, write_only=True)
    user = PassengerSerializer(read_only=True)
    refresh = serializers.CharField(max_length=500, read_only=True)
    access = serializers.CharField(max_length=500, read_only=True)

    def validate(self, data):
        phone = data.get('phone', None)
        passenger = Passenger.objects.filter(phone=phone)
        if not passenger:
            raise serializers.ValidationError('User with this phone number does not exists')
        passenger = passenger.get()
        refresh = RefreshToken.for_user(passenger)
        user_details = dict()
        user_details['user'] = PassengerSerializer(passenger).data
        user_details['refresh'] = str(refresh)
        user_details['access'] = str(refresh.access_token)
        return user_details

    def validate_code(self, code):
        if not str(code).isdigit():
            raise serializers.ValidationError('Code must contain only digits')
        return code


class DriverLoginSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4, max_length=4, write_only=True)
    country_code = serializers.CharField(max_length=5, write_only=True)
    phone = serializers.CharField(max_length=17, write_only=True)
    user = DriverSerializer(read_only=True)
    refresh = serializers.CharField(max_length=500, read_only=True)
    access = serializers.CharField(max_length=500, read_only=True)

    def validate(self, data):
        phone = data.get('phone', None)
        driver = Driver.objects.filter(phone=phone)
        if not driver.exists():
            raise serializers.ValidationError({'errors': 'driver does not exists'})
        if not driver[0].is_confirmed is True:
            raise serializers.ValidationError({'errors': 'user account was not confirmed'})
        driver = driver.get()
        refresh = RefreshToken.for_user(driver)
        user_details = dict()
        user_details['user'] = DriverSerializer(driver).data
        user_details['refresh'] = str(refresh)
        user_details['access'] = str(refresh.access_token)
        return user_details


class PhoneVerificationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, write_only=True)
    country_code = serializers.CharField(max_length=5, write_only=True)
    code = serializers.CharField(max_length=4, write_only=True)

    def validate_code(self, code):
        if not str(code).isdigit():
            raise serializers.ValidationError('Code must contain only digits')
        return code


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17, write_only=True)
    country_code = serializers.CharField(max_length=5, write_only=True)
    user_exist = serializers.BooleanField(read_only=True)
    user_has_info = serializers.BooleanField(read_only=True, default=False)
    role = serializers.CharField(max_length=20, read_only=True)
    detail = serializers.CharField(max_length=500, default='code has been send', read_only=True)

    def validate(self, data):
        phone = data.get('phone')
        user = User.objects.filter(phone=phone)
        role = None
        if not user:
            return {'user_exist': False}
        user = user.get()
        role = getattr(user, 'passenger', 'driver')
        if not isinstance(role, str):
            role = 'passenger'
        if not user.name:
            return {'user_exist': True, 'role': role}
        return {'user_exist': True, 'user_has_info': True, 'role': role}


class VerificationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=14, write_only=True)
    code = serializers.CharField(min_length=4, max_length=4, write_only=True)
    role = serializers.CharField(max_length=10, write_only=True)

    def validate_role(self, role):
        if role != 'passenger' or role != 'driver':
            raise serializers.ValidationError('Incorrect role')
        return role
    
    def validate_code(self, code):
        if not str(code).isdigit():
            raise serializers.ValidationError('Code must contain only digits')
        return code


class PassengerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('email', 'name')

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class FinishRegistrationSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=17, write_only=True)
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(max_length=40, write_only=True)
    user = PassengerSerializer(read_only=True)
    refresh = serializers.CharField(max_length=500, read_only=True)
    access = serializers.CharField(max_length=500, read_only=True)

    def validate(self, data):
        passenger_id = data.get('id')
        email = data.get('email')
        name = data.get('name')
        passenger = Passenger.objects.filter(id=passenger_id)
        if not passenger:
            raise serializers.ValidationError('User with this phone number does not exists')
        passenger = passenger.get()
        passenger.email = email
        passenger.name = name
        passenger.save()
        refresh = RefreshToken.for_user(passenger)
        user_details = dict()
        user_details['user'] = PassengerSerializer(passenger).data
        user_details['refresh'] = str(refresh)
        user_details['access'] = str(refresh.access_token)
        return user_details

    def validate_id(self, id):
        if not str(id).isdigit():
            raise serializers.ValidationError('Id must be integer')
        return id

    def validate_email(self, email):
        if not email:
            return serializers.ValidationError('Email must be set')
        return email
    
    def validate_name(self, name):
        if not name:
            return serializers.ValidationError('Name must be set')
        return name


class UserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=14)
