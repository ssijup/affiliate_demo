from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import random
import string
from django.db.models import Sum





from .models import Product,RefferalLink,RegionData,UserPaymentDetailsOfProduct, UserCommissions,PaymentRquest
from .serializer import ProductSeriaizer,RefferalLinkSerializer, UserPaymentDetailsOfProductSerializer
from userapp.models import UserData
from affiliate.settings import SITE_DOMAIN_NAME
from django.conf import settings
import razorpay







# class CreateProductView(APIView):


class CreateProductView(APIView):

    def generate_unique_id(self):
        characters = string.ascii_letters + string.digits
        unique_id = ''.join(random.choices(characters, k=12))
        print(unique_id)
        return unique_id
    
    def post(self, request):
        user = request.user
        try:
            user_data = UserData.objects.get(id=user.id)
            data = request.data
            product_serializer = ProductSeriaizer(data=data)
            unique_product_id = self.generate_unique_id()
            while Product.objects.filter(unique_id=unique_product_id).exists():
                unique_product_id = self.generate_unique_id()
            data['unique_id'] = unique_product_id
            data['user_id'] = user_data.id
            print('ooooooooo')
            if product_serializer.is_valid():
                print('yyyyyyyyyyy')
                product = product_serializer.save()
                # link = f'{SITE_DOMAIN_NAME}/#/user/register?li={}&product_id={product.unique_id}&influ_1={None}&org_2={None}'

                # product.product_link = link
                # product.save()
                product = Product.objects.get(unique_id=unique_product_id)
                data['product_id'] = product.id
                data['link_generated_by_id'] = user_data.id
                # creating the link
                link_serializer = RefferalLinkSerializer(data=data)
                print('iiiiiiiiiiiiiiiiiiiiiiiioooiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                if link_serializer.is_valid():
                    print('qqkkkkkkkkkk')
                    link_obj =link_serializer.save()
                    link_id = link_obj.uuid
                    link = f'{SITE_DOMAIN_NAME}/#/user/register?li={link_id}&product_id={product.unique_id}&influ_1={None}&org_2={None}'
                    link_obj.user_refferal_link = link
                    product.product_link= link
                    link_obj.save()
                    product.save()

                    return Response({'message': 'Product created successfully','link_data' :link_serializer.data, 'product_data': product_serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    print(link_serializer.errors)
                    return Response({'message': 'Failed: Link generation failed', 'errors': link_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(product_serializer.errors)
                return Response({'message': 'Enter valid details', 'errors': product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'message': 'Something went wrong. Please try again later.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Something went wrong. Please try again later.', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



'''To Increase(ie create) the count every time when the product link is clicked .
Why this?for first time there will not be any infuncer if or organiser link .
Its admin or simply the product link '''
class CreateProductClicks(APIView):
    def patch(self, request, product_unique_id):
        try:
            product = Product.objects.get(unique_id = product_unique_id)
            product.clicks += 1
            print('product.clicks :' , product.clicks)
            product.save()
            return Response({'message' : 'Product clicked'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)


#To get all the product details min admin dash
class GetAllProductDeatilsInAdminDash(APIView):
    def get(self, request):
        try:
            products= Product.objects.all()
            serializer = ProductSeriaizer(products, many = True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)


        
    #To get the details of a single product using its id  
class GetSingleProductDetailUisngId(APIView):
    def get(self, request, product_id):
        try:
            products= Product.objects.get(id =product_id)
            serializer = ProductSeriaizer(products)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)

    #To show user particular product link
class GetUserProductLink(APIView):
    def get(self, request, product_id):
        try:
            user = request.user
            user_data = UserData.objects.get(id = user.id)
            products= Product.objects.get(id =product_id)
            obj = RefferalLink.objects.get(product = products, user = user_data)
            serializer = RefferalLinkSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)



   
# To list all the organisers in the admin side(didn't consider scaling ie admin cretion for a company)
class ListAllOraganiserView(APIView):
    def get(self,request):
        organisers = RefferalLink.objects.filter(link_holder_current_role = 'organiser')
        serializer = RefferalLinkSerializer(organisers, many = True)
        return Response(serializer.data,status= status.HTTP_200_OK)



# To list all the organisers of a particular product in the admin side
class ListAllOrganiserofAproduct(APIView):
    def get(self,request, product_id):
        try:
            product = Product.objects.get(id = product_id)
            organisers = RefferalLink.objects.filter(product=product,link_holder_current_role = 'organiser')
            serializer = RefferalLinkSerializer(organisers, many = True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        except RefferalLink.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)


 
# To list all the influencers in the admin side(didn't consider scaling ie admin cretion for a company)
class ListAllInfluencersView(APIView):
    def get(self,request):
        print('iiio')
        influencers = RefferalLink.objects.filter(link_holder_current_role = 'influencer')
        serializer = RefferalLinkSerializer(influencers, many = True)
        return Response(serializer.data,status= status.HTTP_200_OK)

# To list all the influencers of a particular product in the admin side
class ListAllinfluencerofAproduct(APIView):
    def get(self,request, product_id):
        try:
            product = Product.objects.get(id = product_id)
            influencers = RefferalLink.objects.filter(product=product,link_holder_current_role = 'influencer')
            serializer = RefferalLinkSerializer(influencers, many = True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        except RefferalLink.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)


        

#payment ie subcription of the product and calculating the commission is doing in this view
class ProductPaymentView(APIView):

    def post(self ,request, product_id):
        try:
            user = request.user
            user_data =UserData.objects.get(id= user.id)
            product = Product.objects.get(id = product_id)
            user_infos = RefferalLink.objects.get(user = user_data, product = product)

            client = razorpay.Client(auth=(settings.API_KEY, settings.AUTH_TOKEN))
            razorpay_amount=int(product.subcription_fee)*100  
            keys =  settings.API_KEY
            DATA = {
                # 'KEY' :keys,
                "amount": razorpay_amount ,
                "currency": "INR",
                "receipt": "receipt#1",
                "notes": {
                    "key1": keys,
                    "key2": "value2"
                }
            }

            response=client.order.create(data=DATA)

            print(response)
            if response['status'] == 'created':
                order_id = response['id']
                amount =response['amount'] 
                PaymentRquest.objects.create(
                    user_link = user_infos,
                    pay_request_order_id = order_id,
                    product = product, 
                    total_amount = amount/100
                      )
                return Response({'message' : 'Your payment request intialted sucessfully .Commission calculated',"data" :response}, status=status.HTTP_202_ACCEPTED)
        except RefferalLink.DoesNotExist:
            return Response({'message' : '1Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'message' : '2Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'message' : '3Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'message' : '4Something whent wrong...PLease try after sometime'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubcriptionPaymentSucessfullView(APIView):
    def calculate_commision_amount(self,influencer_percentage, organiser_percentage, product):
        print('influencer_percentage :' , influencer_percentage)
        print('organiser_percentage :' , organiser_percentage)
        gst_rate = product.inclusive_GST #(the gst rate of the product)
        product_fee = product.subcription_fee
        product_fee_without_gst = (product_fee / (100 + gst_rate)) * 100
        
        if influencer_percentage and organiser_percentage:
            influencer_comm_amt = (influencer_percentage / 100) * product_fee_without_gst
            organiser_comm_amt = (organiser_percentage / 100) * product_fee_without_gst
            return influencer_comm_amt,organiser_comm_amt

        if not influencer_percentage :
            influencer_comm_amt = 0
        else :
            influencer_comm_amt = (influencer_percentage / 100) * product_fee_without_gst
       
        if not organiser_percentage:
            organiser_comm_amt = 0
        else :
            organiser_comm_amt = (organiser_percentage / 100) * product_fee_without_gst

        return influencer_comm_amt,organiser_comm_amt
    
    def calculate_commission_percentage( self,influencer, organiser, product):
        subcription_fee = product.subcription_fee
        # inclusive_GST = product.
        organiser_commission_percentage = product.organiser_commission_percentage
        influencer_commission_percentage = product.influencer_commission_percentage
        
        if influencer and organiser:#(give the com% as it is for both)
            influencer_percent = influencer_commission_percentage
            organiser_percentage = organiser_commission_percentage
            influencer_amt, organiser_amt =self.calculate_commision_amount(influencer_percent,organiser_percentage, product)
            return influencer_amt, organiser_amt

        elif influencer and not organiser:
            influencer_percent = influencer_commission_percentage
            organiser_percentage = None
            influencer_amt, organiser_amt =self.calculate_commision_amount(influencer_percent,organiser_percentage, product)
            return influencer_amt, organiser_amt
        
        elif organiser and not influencer:
            influencer_percent = None
            organiser_percentage = influencer_commission_percentage #(Means he is the directreffer in this case ie no inter mediate)
            # amount =self.calculate_commision_amount(influencer_percent,organiser_percentage, product)
            influencer_amt, organiser_amt =self.calculate_commision_amount(influencer_percent,organiser_percentage, product)
            return influencer_amt, organiser_amt
    def post(self, request, paymentId,payment_oredr_RequestId,signature_id):
        client = razorpay.Client(auth=(settings.API_KEY, settings.AUTH_TOKEN))
        try:
            verify_signature = client.utility.verify_payment_signature({
                'razorpay_order_id': payment_oredr_RequestId,
                'razorpay_payment_id': paymentId,
                'razorpay_signature': signature_id
            })
            payment_vrification_status  = verify_signature
            response = client.payment.fetch(paymentId)
            print(response)

            
            if not verify_signature:
                return Response({'message': 'Signature verification failed. Payment failed.'}, status=status.HTTP_400_BAD_REQUEST)
            else :
                try:
                    pay_request_obj = PaymentRquest.objects.get(pay_request_order_id = payment_oredr_RequestId )
                    user_data = pay_request_obj.user_link.user
                    product = pay_request_obj.product  
                    print('uuuuuuuuuuuuuuuuu')                 
                    user_infos = RefferalLink.objects.get(user = user_data, product = product)
                    print('iiiiiiiiiiiiiiiiiiiiiiiii',user_infos)
                    direct_refferr = user_infos.direct_referred_link_owner
                    indirect_reffer = user_infos.indirect_referred_link_owner
                    # product = user_infos.product
                    # amount = 
                    UserPaymentDetailsOfProduct.objects.create(
                        user_link =user_infos,
                        product =product,
                         payment_status = True,
                         payment_total_amount_paid = pay_request_obj.total_amount,
                        payment_status_of_gateway = response['status'],
                        payment_order_id = response['order_id'],
                        payment_id =response['id'],
                        payment_signature = signature_id

                        )
                    if direct_refferr or indirect_reffer:
                        print('Calculation started')
                        influencer_comm_amt,organiser_comm_amt = self.calculate_commission_percentage(direct_refferr, indirect_reffer, product)
                        print('influencer_percentage :' , influencer_comm_amt)
                        print('organiser_percentage :' , organiser_comm_amt)          
                        if direct_refferr:
                            print('Calculation started : direct_refferraaa')
                            # user = direct_refferr
                            direct_user_data = UserData.objects.get(id = direct_refferr.id)
                            print(',,,,,,,,,,,,,,,,,,,,,,,',direct_user_data,)
                            direct_user = RefferalLink.objects.get(user = direct_user_data, product =product)
                            user_commission = UserCommissions.objects.create(
                                user = direct_user,
                                commission_amount =influencer_comm_amt,
                                paid_user = user_infos,
                                product = product,
                                commissioned_user_role = direct_user.link_holder_current_role,
                                paid_user_role = user_infos.link_holder_current_role,
                            )
                            
                        if indirect_reffer:
                            print('Calculation started : indirect_refferr')

                            # user = indirect_reffer
                            indirect_user_data = UserData.objects.get(id = indirect_reffer.id)
                            print(indirect_user_data)
                            indirect_user = RefferalLink.objects.get(user = indirect_user_data, product =product)
                            user_commission = UserCommissions.objects.create(
                                user = indirect_user,
                                commission_amount =organiser_comm_amt,
                                paid_user = user_infos,
                                product = product,
                                commissioned_user_role = indirect_user.link_holder_current_role,
                                paid_user_role = user_infos.link_holder_current_role,
                            )
                
                    return Response({'message':' Payment completed'}, status=status.HTTP_200_OK)
                except PaymentRquest.DoesNotExist:
                    return Response({'message' : 'Your payment is under process'}, status=status.HTTP_206_PARTIAL_CONTENT)

        except Exception as e:
            print(e)
            return Response({'message': str(e) + ' Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
        


class ListAllProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSeriaizer(products, many = True)
        return Response(serializer.data , status = status.HTTP_200_OK)



#Done api in url ^^
    
#To get all the payment details in admin side 
class AllPayedUsersView(APIView):
    def get(self, request):
        user =  request.user
        try:
            payess = UserPaymentDetailsOfProduct.objects.all()
            serializer = UserPaymentDetailsOfProductSerializer(payess, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message' : '1Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
    

#To get suscribers of  each product in admin side 
class ProductSuscribedUers(APIView):
    def get(self, request, product_id):
        user =  request.user
        try:
            print('///////////')
            product = Product.objects.get(id = product_id)
            user_data = RefferalLink.objects.get(user = user.id)
            payess = UserPaymentDetailsOfProduct.objects.filter(product =product )
            serializer = UserPaymentDetailsOfProductSerializer(payess, many = True)
            return Response(serializer.data , status=status.HTTP_200_OK)
            # return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)
        except RefferalLink.DoesNotExist:
            return Response({'message' : '1Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'message' : '2Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'message' : '3Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message' : '1Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
    

#Show overall transaction count in admin side 
class TransactionCount(APIView):
    def get(self, request):
        transaction_count = UserPaymentDetailsOfProduct.objects.all().count()
        return Response({'message' : transaction_count}, status=status.HTTP_200_OK)


#Show overall transaction count of a single product 
class TransactionCountOfParticularProduct(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)

            product_transaction_count = UserPaymentDetailsOfProduct.objects.filter(product_id = product).count()
            return Response({'message' : product_transaction_count}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'message' : '3Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)
        


# PARTICULAR PRODUCT ANALYTICS
        
#Total transaction/Customer/gross sale of the product of a particular user
class UserSIngleProductTranction(APIView):
    def get(self, request, product_id):
        try:
            user = request.user
            user_data = UserData.objects.get(id = user.id)
            product = Product.objects.get(id = product_id)
            clicks_obj = RefferalLink.objects.get(product = product ,user = user_data )
            clicks = clicks_obj.clicks
            transactions = UserCommissions.objects.filter(user__user=user_data, product=product)
            transaction_count = transactions.count()

            total_commission = transactions.aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0
            total_gross_sale = transactions.aggregate(Sum('product__subcription_fee'))['product__subcription_fee__sum'] or 0
            converstion_rate = transaction_count/clicks
            e_p_c = total_commission/clicks
            avg_order_value = total_gross_sale/transaction_count
            return Response({'transaction_count' : transaction_count,
                              'total_gross_sale' : total_gross_sale, 
                              'total_commission' : total_commission, 
                              'clicks' : clicks,
                              'e_p_c' : e_p_c,
                              'converstion_rate' : converstion_rate,
                              'avg_order_value': avg_order_value},
                                status=status.HTTP_200_OK)
        except RefferalLink.DoesNotExist:
            return Response({'message' : 'Something whent wrong'}, status = status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'message' : 'Something whent wrong'}, status = status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'message' : 'Something whent wrong'}, status = status.HTTP_400_BAD_REQUEST)


#To show the details in admin overview
class AdminOverView(APIView):
    def get(self, request, product_id):
        try:
            # user = request.user
            # user_data = UserData.objects.get(id = user.id)
            # product = Product.objects.get(id = product_id)
            # clicks_obj = RefferalLink.objects.get(product = product ,user = user_data )
            # clicks = clicks_obj.clicks
            product = Product.objects.all()

            transactions = UserCommissions.objects.all()
            transaction_count = transactions.count()
            clicks = product.aggregate(Sum('clicks'))['clicks__sum'] or 0
            total_commission = transactions.aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0
            total_gross_sale = transactions.aggregate(Sum('product__subcription_fee'))['product__subcription_fee__sum'] or 0
            converstion_rate = transaction_count/clicks
            e_p_c = total_commission/clicks
            avg_order_value = total_gross_sale/transaction_count
            return Response({'transaction_count' : transaction_count,
                              'total_gross_sale' : total_gross_sale, 
                              'total_commission' : total_commission, 
                              'clicks' : clicks,
                              'e_p_c' : e_p_c,
                              'converstion_rate' : converstion_rate,
                              'avg_order_value': avg_order_value},
                                status=status.HTTP_200_OK)
        except RefferalLink.DoesNotExist:
            return Response({'message' : 'Something whent wrong'}, status = status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'message' : 'Something whent wrong'}, status = status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'message' : 'Something whent wrong'}, status = status.HTTP_400_BAD_REQUEST)


# #Total clicks of the a product for a user link
# class UserTotalSingleproductClicks(APIView):
#     def hget(self, request, product_id):



#Total coustomer for the user for a particular product
# class UserSingleProductCustomerCount:
#     def get(self, request, product_id)

# class Total
#Average Order Value





