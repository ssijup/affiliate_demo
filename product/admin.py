from django.contrib import admin

from .models import Product,RefferalLink,RegionData,PaymentRquest,UserPaymentDetailsOfProduct, UserCommissions

# Register your models here.

admin.site.register(Product)
admin.site.register(RefferalLink)
admin.site.register(RegionData)
admin.site.register(UserPaymentDetailsOfProduct)
admin.site.register(UserCommissions)
admin.site.register(PaymentRquest)



