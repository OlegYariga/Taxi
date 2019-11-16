import datetime
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_superuser(self, phone, name='Admin', password=None):
        user = self.model(phone=phone, name=name)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(phone=username)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=17, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def get_full_name(self):
        return f'{self.name}'

    def __str__(self):
        return self.phone


class PassengerManager(BaseUserManager):
    def create_passenger(self, phone, password=None):
        if phone is None:
            raise TypeError('User must have phone number')

        passenger = Passenger(
            phone=phone,
        )
        passenger.last_login = datetime.datetime.now()
        passenger.set_unusable_password()
        passenger.save()
        return passenger


class Passenger(User):
    email = models.EmailField()
    USERNAME_FIELD = 'phone'

    objects = PassengerManager()

    def __str__(self):
        return f'{self.phone} is a passenger'


class DriverManager(BaseUserManager):
    def create_driver(self, name, phone, email, taxi, password=None):
        taxi = Taxi.objects.filter(type=taxi.type)
        if not taxi:
            raise TypeError('No taxi with this TYPE')

        if phone is None:
            raise TypeError('User must have phone number')

        driver = Driver(
            name=name,
            phone=phone,
            email=email,
            taxi=taxi.first()
        )
        driver.last_login = datetime.datetime.now()
        driver.set_unusable_password()
        driver.save()
        return driver   


CAR_CHOICES = (
    ('econom', 'Econom class'),
    ('business', 'Business class'),
    ('first', 'First class'),
    ('keke', 'Tricycle(Keke)')
)


class Taxi(models.Model):
    type = models.CharField(max_length=15, choices=CAR_CHOICES, default=CAR_CHOICES[0][0])
    price = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.type} cost {self.price}'


class Driver(User):
    email = models.EmailField()
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE) # after some time replace CASCADE -> PROTECT
    is_confirmed = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('email', 'taxi')

    objects = DriverManager()

    def __str__(self):
        return f'{self.phone} is a driver. He drive on {self.taxi.type}'
