from django.contrib import admin
from .models import Part, Extra, Group, Product, Offer, OrderHeader, OrderDetail

# Register your models here.
admin.site.register(Part)
admin.site.register(Extra)
admin.site.register(Group)
admin.site.register(Product)
admin.site.register(Offer)
admin.site.register(OrderHeader)
admin.site.register(OrderDetail)

