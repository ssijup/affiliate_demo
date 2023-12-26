from django.contrib import admin

from .models import Product,RefferalLink,RegionData,Payment

# Register your models here.

admin.site.register(Product)
admin.site.register(RefferalLink)
admin.site.register(RegionData)
admin.site.register(Payment)
