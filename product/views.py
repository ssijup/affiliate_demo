from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import random
import string




from .models import Product,RefferalLink,RegionData,Payment
from .serializer import ProductSeriaizer,RefferalLinkSerializer
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
            if product_serializer.is_valid():
                product = product_serializer.save()
                # link = f'{SITE_DOMAIN_NAME}/association/linkactivation/{product.unique_id}'
                link = f'{SITE_DOMAIN_NAME}/signup?product_id={product.unique_id}&influ_1={None}&org_2={None}'
                    # http://yourmlmwebsite.com/signup?ref=<referrer_id>&level1=<level1_id>&level2=<level2_id>

                product.product_link = link
                product.save()
                product = Product.objects.get(unique_id=unique_product_id)
                data['product_id'] = product.id
                data['link_generated_by_id'] = user_data.id
                # creating the link
                link_serializer = RefferalLinkSerializer(data=data)
                if link_serializer.is_valid():
                    link_serializer.save()
                    return Response({'message': 'Product created successfully','link_data' :link_serializer.data, 'product_data': product_serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Failed: Link generation failed', 'errors': link_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
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
            product.clicks = +1
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
            product = Product.objects.get(product = product_id)
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
            product = Product.objects.get(product = product_id)
            influencers = RefferalLink.objects.filter(product=product,link_holder_current_role = 'influencer')
            serializer = RefferalLinkSerializer(influencers, many = True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        except RefferalLink.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"}, status=status.HTTP_400_BAD_REQUEST)


#Done api in url ^^
        

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
            return Response({'message' : 'Your payment request intialted sucessfully',"data" :response}, status=status.HTTP_202_ACCEPTED)
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
                return Response({'message':' Payment completed'}, status=status.HTTP_200_OK)       
        except Exception as e:
            return Response({'message': str(e) + ' Payment failed'}, status=status.HTTP_400_BAD_REQUEST)