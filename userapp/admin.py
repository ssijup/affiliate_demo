from django.contrib import admin

from .models import UserData,UserDetails,UserRequestingforUpgradingToOrganiser,UserBankAccountDetails, RegionDataVillage, SupportingExcelData

admin.site.register(UserData),
admin.site.register(UserDetails),
admin.site.register(RegionDataVillage),
admin.site.register(SupportingExcelData)
admin.site.register(UserBankAccountDetails)
admin.site.register(UserRequestingforUpgradingToOrganiser)






