from django.urls import path
from .views import (CreateProductView,CreateProductClicks,GetAllProductDeatilsInAdminDash,
                     GetSingleProductDetailUisngId,ListAllInfluencersView, ListAllOraganiserView, ListAllOrganiserofAproduct, 
                     ListAllinfluencerofAproduct, ProductPaymentView, SubcriptionPaymentSucessfullView)

urlpatterns = [
    #To create a product in  admin side 
    path('create',CreateProductView.as_view(), name = 'CreateProductView'),

    #To create ie increce prodct link clicked  count
    path('link/clicked/<product_unique_id>',CreateProductClicks.as_view(), name = 'CreateProductClicks'),
    #To get all the product and its details in the admin side
    path('list/all/details',GetAllProductDeatilsInAdminDash.as_view(), name = 'GetAllProductDeatilsInAdminDash'),
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
    #This will be call when the user start the payment creation or subcription of a product
    path('subcription/payment/intiated/<product_id>',ProductPaymentView.as_view(), name = 'ProductPaymentView'),
    #To confirm the payment that the request to the payment has been Completed sucessfully ie payment completed
    path('subcription/sucessfull/completed/<paymentId>/<payment_oredr_RequestId>/<signature_id>',SubcriptionPaymentSucessfullView.as_view(), name = 'SubcriptionPaymentSucessfullView'),


#Done in excel ^^

#COMMISSION








]
