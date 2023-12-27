from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from .views import (GetUserDetails, CustomTokenObtainPairView,UserRegisration,UserRequestingAdminforUpgradeToOrganiser,
                    GetUSerUpgradationRequests,DetailsOfUserUsingId, UserResquestApproValForUpgradation,
                      CreateProductClicksForUser, UploadFileView, RegionDataVillageListByDistrict,UserTotalCommissionView,
                      RegionDataVillageListByLocalBody,GetUSerUpgradationRequestsStausInUserDash,GetAllUserProduct, RegionDataVillageListByVillage)


urlpatterns = [

    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('region-data/upload', UploadFileView.as_view(), name='UploadFileView'),
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
    path('user/link/clicked/<product_unique_i>/<link_uuid>', CreateProductClicksForUser.as_view(), name='CreateProductClicksForUser'),
    #To displaying the details of a user when clicked     
    path('user/details/<user_id>', DetailsOfUserUsingId.as_view(), name='DetailsOfUserUsingId'),
   
   #Done in excel ^^

#User Total commission using request
    path('total/commission',UserTotalCommissionView.as_view(), name = 'UserTotalCommissionView'),

    
]
