from django.urls import path
from .views import (CreateProductView,CreateProductClicks,GetAllProductDeatilsInAdminDash,
                     GetSingleProductDetailUisngId,ListAllInfluencersView, ListAllOraganiserView, ListAllOrganiserofAproduct, 
                     ListAllinfluencerofAproduct, ProductPaymentView, SubcriptionPaymentSucessfullView)

urlpatterns = [
    #To create a product in  admin side 
    path('create',CreateProductView.as_view(), name = 'CreateProductView'),

#Done in excel ^
    #To create ie increce prodct link clicked  count
    path('link/clicked/<product_unique_id>',CreateProductClicks.as_view(), name = 'CreateProductClicks'),
    #To get all the product and its details in the admin side
    path('details/list',GetAllProductDeatilsInAdminDash.as_view(), name = 'GetAllProductDeatilsInAdminDash'),
    #To get the details of a single product using its id  
    path('details/<product_id>',GetSingleProductDetailUisngId.as_view(), name = 'GetSingleProductDetailUisngId'),

    # organisers & influencers
    # To list all the organisers in the admin side(didn't consider scaling ie admin cretion for a company)
    path('organiser/all/list',ListAllOraganiserView.as_view(), name = 'ListAllOraganiserView'),
    # To list all the organisers of a particular product in the admin side
    path('organiser/<product_id>',ListAllOrganiserofAproduct.as_view(), name = 'ListAllOrganiserofAproduct'),
    # To list all the influencers in the admin side(didn't consider scaling ie admin cretion for a company)
    path('influncers/all/list',ListAllInfluencersView.as_view(), name = 'ListAllInfluencersView'),
    # To list all the influencers of a particular product in the admin side
    path('influncers/<product_id>',ListAllinfluencerofAproduct.as_view(), name = 'ListAllinfluencerofAproduct'),


#PAYMENT

    path('subcription/payment/intiated/<product_id>',ProductPaymentView.as_view(), name = 'ProductPaymentView'),

    path('subcription/sucessfull/completed/<paymentId>/<payment_oredr_RequestId>/<signature_id>',SubcriptionPaymentSucessfullView.as_view(), name = 'SubcriptionPaymentSucessfullView'),





]
