from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create an OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    # if you want scertain fields only you can do it like
    # fields = ["user", "full_name"]
    inlines = [OrderItemInline]

# We have unregister and reregister the order model to make the  changes visible
# Unresister the order Model
admin.site.unregister(Order)

# Re-register the Order model and OrderAdmin
admin.site.register(Order, OrderAdmin)
