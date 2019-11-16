from django.contrib import admin
from users.models import Taxi, User, Driver
from order.models import Order


@admin.register(Taxi)
class TaxiAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdminView(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdminView(admin.ModelAdmin):
    pass


@admin.register(Driver)
class DriverAdminView(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'email', 'taxi',)
        }),
        ('Confirm driver account', {
            'fields': ('is_confirmed',)
        }),
    )
    pass
