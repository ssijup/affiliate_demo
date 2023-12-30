from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from .views import (GetUserDetails, CustomTokenObtainPairView,UserRegisration,UserRequestingAdminforUpgradeToOrganiser,
                    GetUSerUpgradationRequests,DetailsOfUserUsingId, UserResquestApproValForUpgradation,RegionDataVillageListByState,
                      CreateProductClicksForUser, UploadFileView, RegionDataVillageListByDistrict,UserTotalCommissionView,
                      RegionDataVillageListByLocalBody,GetUSerUpgradationRequestsStausInUserDash,GetAllUserProduct, 
                     GetAdminUserDetails, UserTotalCliks,TotalGrossSaleOfEachUser,TotalGrossSaleofEachProduct,RegionDataVillageListByVillage,
                    UserTotalCliksOfEachProduct,GetUserBankAccountsViewUsingId, GetUserBankAccountsView,AddUserBankAccountDetailsView, 
                    NetCommissionAtAdminSide,EidtUserBankAccount, UserTotalTranctionForallTheLink)



urlpatterns = [

path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


path('region-data/upload', UploadFileView.as_view(), name='UploadFileView'),

path('state/<str:state>', RegionDataVillageListByState.as_view(), name='state-list'),
path('district/<str:district>', RegionDataVillageListByDistrict.as_view(), name='district-list'),
path('localbody/<str:local_body>', RegionDataVillageListByLocalBody.as_view(), name='localbody-list'),
path('village/<str:village>', RegionDataVillageListByVillage.as_view(), name='village-list'),


#USER
#To register a user
path('user/registration/<product_unique_id>/<influncer_uuid>/<organiser_uuid>', UserRegisration.as_view(), name='UserRegisration'),
#To get the user details  logged user after login
path('single/user/dashboard/details', GetUserDetails.as_view(), name='GetUserDetails'),
#To get all the product a particular user .user will be Fetched using request
path('single/user/all/product/details', GetAllUserProduct.as_view(), name='GetAllUserProduct'),




#UPGRADATION REQUEST
#user request for level upgradation ie from influncer to organiser
path('user/upgrdation/request', UserRequestingAdminforUpgradeToOrganiser.as_view(), name='UserRequestingAdminforUpgradeToOrganiser'),
#To get the user request for upgradation in the admin dashboard
path('user/upgrdation/request/in/admin', GetUSerUpgradationRequests.as_view(), name='GetUSerUpgradationRequests'),
#to get the user request status of upgradation in the user dashboard
path('user/upgrdation/status/in/user/dash', GetUSerUpgradationRequestsStausInUserDash.as_view(), name='GetUSerUpgradationRequestsStausInUserDash'),

#To approve or reject user request to upgradation
path('user/upgrdation/request/approval/<upgrading_request_id>', UserResquestApproValForUpgradation.as_view(), name='UserResquestApproValForUpgradation'),

#To increase click count of a particular user  ie the influncer or oraganiser link
path('user/link/clicked/<product_unique_id>/<link_uuid>', CreateProductClicksForUser.as_view(), name='CreateProductClicksForUser'),
#To displaying the details of a user when clicked     
path('user/details/<user_id>', DetailsOfUserUsingId.as_view(), name='DetailsOfUserUsingId'),


#User Total commission using request
path('user/total/commission',UserTotalCommissionView.as_view(), name = 'UserTotalCommissionView'),
#Gross sale of a particualr user(total sale amount) iesum of total price of all the product slled under tha user
path('user/total/gross/sale',TotalGrossSaleOfEachUser.as_view(), name = 'TotalGrossSaleOfEachUser'),
#Gross sale of a particualr product(total sale amount) ie sum of total price of  the product selled 
path('total/gross/sale/each/product/<product_id>',TotalGrossSaleofEachProduct.as_view(), name = 'TotalGrossSaleofEachProduct'),
#Total gross sale each product in adminside

#Total cliks of the user (sum ofall product clicks)
path('user/total/clicks',UserTotalCliks.as_view(), name = 'UserTotalCliks'),
#Total cliks of the user for each product (sum ofall product clicks)
path('user/total/clicks/each/product/<product_id>',UserTotalCliksOfEachProduct.as_view(), name = 'UserTotalCliksOfEachProduct'),



#ADDING BANK ACCOUNT
#User create bank account
path('user/add/bank/account/<link_id>',AddUserBankAccountDetailsView.as_view(), name = 'AddUserBankAccountDetailsView'),
#Edit bank user bank account
path('user/edit/bank/account/<accouunt_id>',EidtUserBankAccount.as_view(), name = 'EidtUserBankAccount'),
#All the accounts In the user dash
path('user/get/all/bank/account>',GetUserBankAccountsView.as_view(), name = 'GetUserBankAccountsView'),
#The bank acc of a particular user  to the admin  
path('user/get/all/bank/account>',GetUserBankAccountsViewUsingId.as_view(), name = 'GetUserBankAccountsViewUsingId'),


#To get the admin details 
  path('admin/dash/details', GetAdminUserDetails.as_view(), name='GetAdminUserDetails'),
#Net commission at the admin side 
  path('net/overoll/commission/in/admin', NetCommissionAtAdminSide.as_view(), name='NetCommissionAtAdminSide'),


#Done in excel ^^

# #User total transaction to display in overview
  path('user/overall/transaction/for/all/link', UserTotalTranctionForallTheLink.as_view(), name='UserTotalTranctionForallTheLink'),

 
    
]
