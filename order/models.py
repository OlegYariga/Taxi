from django.db import models
from users.models import Passenger, Taxi


STATUS_CHOICES = (
    ('search', 'searching'),
    ('active', 'active'),
    ('close', 'closed'),
)


PAYMENT_CHOICES = (
    ('card', 'card'),
    ('cash', 'cash')
)


class ArrivalCoord(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class DepartureCoord(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Order(models.Model):
    arrival = models.CharField(max_length=257)
    arrival_coords = models.ForeignKey(ArrivalCoord, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    departure = models.CharField(max_length=257)
    departure_coords = models.ForeignKey(DepartureCoord, on_delete=models.PROTECT)
    taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Order for {self.passenger.phone}({self.passenger.name}) is {self.status} pay by {self.payment_type}'