from .serializer import CustomTokenObtainPairSerializer, UserDetailsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from django.shortcuts import render
from django.db import transaction

from userapp.serializer import UserDataSerializer,UserDetailsSerializer, RegionDataVillageSerializer
from product.serializer import ( ProductSeriaizer,RefferalLinkSerializer, UserRequestingforUpgradingToOrganiserSerializer)
from .models import UserData,UserDetails, UserRequestingforUpgradingToOrganiser, SupportingExcelData, RegionDataVillage
from product.models import Product, RefferalLink, UserCommissions
from affiliate.settings import SITE_DOMAIN_NAME

import pandas as pd

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




##new api for region data upload     
class UploadFileView(APIView):
    def post(self, request):
        try:
            print('inside1')
            xlsx = SupportingExcelData.objects.get(id=1)
            print(xlsx)
            file_path = xlsx.xlsx_file.path
            print(file_path)
            df = pd.read_excel(file_path, engine='openpyxl')
            print("DF HEAD\n", df.head(5)) 
            with transaction.atomic():
                for row_number, (index, row) in enumerate(df.iterrows(), start=1):
                    district = row.iloc[2]     
                    sub_district = row.iloc[6]
                    village = row.iloc[10]
                    local_body = row.iloc[14]   
                    if True:
                        print(f"Row {row_number}: {district},{sub_district},{village},{local_body}")
                        member_instance = RegionDataVillage(
                            state = 'KERALA',
                            district=district,
                            sub_district=sub_district,
                            village=village,
                            local_body=local_body
                        )
                        member_instance.save()
            return Response({"message": "Excel data copied to MemberDirectory"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": "Unable to parse Excel file"}, status=status.HTTP_400_BAD_REQUEST)



class RegionDataVillageListByDistrict(generics.ListAPIView):
    serializer_class = RegionDataVillageSerializer

    def get_queryset(self):
        print('q555555555555555555555')
        district = self.kwargs['district']
        return RegionDataVillage.objects.filter(district=district)

class RegionDataVillageListByLocalBody(generics.ListAPIView):
    serializer_class = RegionDataVillageSerializer

    def get_queryset(self):
        local_body = self.kwargs['local_body']
        return RegionDataVillage.objects.filter(local_body=local_body)

class RegionDataVillageListByVillage(generics.ListAPIView):
    serializer_class = RegionDataVillageSerializer

    def get_queryset(self):
        village = self.kwargs['village']
        return RegionDataVillage.objects.filter(village=village)


class UserRegisration(APIView):
    # product_unique_id : will get the product_unique_id from the url of the registration link
    def post(self, request,product_unique_id, influncer_uuid, organiser_uuid):
        try:
            influncer_uuid = None if influncer_uuid == 'None' else influncer_uuid
            organiser_uuid = None if organiser_uuid == 'None' else organiser_uuid
            print(influncer_uuid,organiser_uuid)
            # influncer_uuid = None
            # organiser_uuid = None 
            with transaction.atomic():

                data = request.data
                name = request.data.get('name')
                email = request.data.get('email')
                password = request.data.get('password')
                # product_unique_id = request.data.get('product_unique_id')#will get it from the 
                if UserData.objects.filter(email = email).exists():
                    return Response({'message' : 'This email alredy exists .Try another one'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        product = Product.objects.get(unique_id = product_unique_id)
                    except Product.DoesNotExist:
                        return Response({'message' : 'Sorry..This product is not avaliable or The link has expired.Please contact siju'})
                    user = UserData.objects.create_user(name = name, email = email,  password=password)
                    data['user_id'] = user.id
                    print(user.name,'kl')
                    user_details_serializer =UserDetailsSerializer(data = data)
                    if user_details_serializer.is_valid():
                        user_uuid = user.uuid
                        # role_hoding = 'influencer'
                        # link = f'{SITE_DOMAIN_NAME}/association/{role_hoding}/linkactivation/{product_unique_id}/{user.name}/{user_uuid}'
                        # user_link =user_details_serializer.save()
                        # user_link.user_refferal_link = link
                        # user_link.save()
                        u_params =user_details_serializer.save()
                        print(u_params,id, '   8888888888888888888888')
                        data['user_id'] = user.id
                        data ['product_id'] = product.id
                        data['link_holder_role_at_link_generation'] = 'influencer'
                        data['link_holder_current_role'] = 'influencer'
                        data['user_details_id'] = u_params.id
                        role_hoding = 'influencer'
                        # link = f'{SITE_DOMAIN_NAME}/association/{role_hoding}/linkactivation/{product_unique_id}/{user.name}/{user_uuid}'
                        if not influncer_uuid and not organiser_uuid :
                            link = f'{SITE_DOMAIN_NAME}/signup?product_id={product_unique_id}&influ_1={user_uuid}&org_2={None}'
                        elif influncer_uuid and organiser_uuid:
                            try:
                                direct_ref = UserData.objects.get(uuid =influncer_uuid)
                                indirect_ref =UserData.objects.get(uuid =organiser_uuid)
                            except UserData.DoesNotExist:
                                return Response({'message' : '111qSometing whent wrong...Please try again'},status=status.HTTP_400_BAD_REQUEST)
                            data['direct_referred_link_owner_id'] = direct_ref.id
                            data['indirect_referred_link_owner_id'] = indirect_ref.id
                            link = f'{SITE_DOMAIN_NAME}/signup?product_id={product_unique_id}&influ_1={user_uuid}&org_2={None}'
                        elif influncer_uuid :
                            try:
                                direct_ref = UserData.objects.get(uuid =influncer_uuid)
                                data['direct_referred_link_owner_id'] = direct_ref.id
                                link = f'{SITE_DOMAIN_NAME}/signup?product_id={product_unique_id}&influ_1={user_uuid}&org_2={None}'

                            except UserData.DoesNotExist:
                                return Response({'message' : 'aaSometing whent wrong...Please try again'},status=status.HTTP_400_BAD_REQUEST)
                        elif organiser_uuid :
                            try:
                                direct_ref = UserData.objects.get(uuid =organiser_uuid)
                                data['direct_referred_link_owner_id'] = direct_ref.id
                                link = f'{SITE_DOMAIN_NAME}/signup?product_id={product_unique_id}&influ_1={user_uuid}&org_2={organiser_uuid}'
                            except UserData.DoesNotExist:
                                return Response({'message' : 'eerSometing whent wrong...Please try again'},status=status.HTTP_400_BAD_REQUEST)

                        link_serializer = RefferalLinkSerializer(data=data)
                        data['user_refferal_link'] = link
                        if link_serializer.is_valid():
                            link_serializer.save()
                            # user_link =link_serializer.save()
                            # user_link =user_details_serializer.save()
                            # user_link.user_refferal_link = link
                            # user_link.save()
                        return Response({'link_data' : link_serializer.data,'message' : "Your registration is successful.Please login Now"},status=status.HTTP_200_OK)
                    print(user_details_serializer.errors)
                    # user.delete()
                    return Response({'message' : "Please check the entered details"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('99',e)
            return Response({'message' : '1111111Someting whent wrong...Please try again'},status=status.HTTP_400_BAD_REQUEST)





#To get the user details once they logged in
class GetUserDetails(APIView):
    def get(self, request):
        user =request.user
        user_data = UserData.objects.get(id = user.id)
        try :
            details = UserDetails.objects.get(user = user_data)
            serializer = UserDetailsSerializer(details)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except UserDetails.DoesNotExist:
            return Response({'message' : "Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)


class UserRequestingAdminforUpgradeToOrganiser(APIView):
    def post(self,request):
        try:
            user = request.user
            user_data = UserData.objects.get(id = user.id)
            user_refferal_link = RefferalLink.objects.get(user = user_data)
            data = request.data
            data['user_id']= user.id
            data['ref_link_id'] = user_refferal_link.id
            user_up_serializer = UserRequestingforUpgradingToOrganiserSerializer(data =data)
            if user_up_serializer.is_valid():
                user_up_serializer.save()
                return Response({'message' : 'Your request for upgrading to organiser submmited sucessfully', 'data' : user_up_serializer.data}, status=status.HTTP_201_CREATED)
            print(user_up_serializer.errors)
            return Response({'message' : "1Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)
        except UserData.DoesNotExist:
            return Response({'message' : "2Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)
        except RefferalLink.DoesNotExist:
            return Response({'message' : "3Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)
    

#to get the user request for upgradation in the admin dashboard
class GetUSerUpgradationRequests(APIView):
    def get(self, request):
        users = UserRequestingforUpgradingToOrganiser.objects.filter(is_verified = False)
        serializer = UserRequestingforUpgradingToOrganiserSerializer(users, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

#to get the user request status of upgradation in the user dashboard
class GetUSerUpgradationRequestsStausInUserDash(APIView):
    def get(self, request):
        try:
            user = request.user
            users = UserRequestingforUpgradingToOrganiser.objects.get(user__id = user.id)
            serializer = UserRequestingforUpgradingToOrganiserSerializer(users)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except UserRequestingforUpgradingToOrganiser.DoesNotExist:
            return Response({'message' : "Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)

#To approve or reject user request to upgradation
class UserResquestApproValForUpgradation(APIView):
    def patch(self,request,upgrading_request_id):
        try:
            user =request.user
            data = request.data
            request_status = request.data.get('request_status') 
            print(request_status, 'pppppp')
            # request_status = request.data.get('description')
            # user_data = UserData.objects.get(id = user.id)
            request_obj = UserRequestingforUpgradingToOrganiser.objects.get(id = upgrading_request_id)
            product = request_obj.user_refferal_link.product
            ref_link = RefferalLink.objects.get(product = product, user = request_obj.user)
            # userdetails_obj = UserDetails.objects.get(user = request_obj.user )
            data['admin_user_id'] =  user.id
            data['is_verified'] = True
            # if request_status == 'Approved':
            #     data['request_status'] = request_status
            serializer = UserRequestingforUpgradingToOrganiserSerializer(request_obj, data = data)
            if serializer.is_valid():
                if request_status == 'Approved':
                    ref_link.link_holder_current_role = 'organiser'
                    print('222222222222222222')
                    role_hoding = 'organiser'
                    # link = f'{SITE_DOMAIN_NAME}/association/{role_hoding}/linkactivation/{ref_link.product.unique_id}/{ref_link.user.name}/{ref_link.user.uuid}'
                    link = f'{SITE_DOMAIN_NAME}/signup?product_id={ref_link.product.unique_id}&influ_1={None}&org_2={ref_link.user.uuid}'
                    ref_link.user_refferal_link = link
                    # userdetails_obj.save()
                    ref_link.save()
                    # if request_status == 'Approved':
                    #     ref_link.objects.filter(id=ref_link.id).update(
                    #         link_holder_current_role='organiser',
                    #         link=f'{SITE_DOMAIN_NAME}/association/organiser/linkactivation/{ref_link.product.unique_id}/{ref_link.user.name}/{ref_link.user.uuid}'
                    #     )
                serializer.save()
                return Response({'message' : 'Request for upgrading updated sucessfully','data' :serializer.data}, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response({'message' : "2Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)
        except UserRequestingforUpgradingToOrganiser.DoesNotExist:
            return Response({'message' : "1Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)
        except RefferalLink.DoesNotExist:
            return Response({'message' : "2Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)
        except UserDetails.DoesNotExist:
                    return Response({'message' : "2Something when wrong please try again"},status=status.HTTP_400_BAD_REQUEST)


#
class CreateProductClicksForUser(APIView):
    def patch(self, request, product_unique_id,link_uuid):
        try:
            link = RefferalLink.objects.get(uuid = link_uuid, product__unique_id = product_unique_id)
            link.clicks = +1
            link.save()
            return Response({'message' : 'link of user clicked'}, status=status.HTTP_201_CREATED)
        except RefferalLink.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"})


#To displaying the details of a user when clicked     
class DetailsOfUserUsingId(APIView):
    def get(self, request, user_id):
        try:
            user = UserData.objects.get(id = user_id) 
            user_details = RefferalLink.objects.filter(user = user)
            serializer = RefferalLinkSerializer(user_details, many = True)
            return Response(serializer.data,status= status.HTTP_200_OK)
        except UserData.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"})
        
        
#To get all the product of a particular user
class GetAllUserProduct(APIView):
    def get(self, request):
        try:
            user = request.user
            user_data = UserData.objects.get(id = user.id)
            link_and_product = RefferalLink.objects.filter(user = user_data)
            serializer = RefferalLinkSerializer(link_and_product, many = True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except UserData.DoesNotExist:
            return Response({'message' : "Something whent wrong...Please try again later"})


#Net Commission
#User Total commission using request
class UserTotalCommissionView(APIView):
    def get(self, request):
        user = request.user
        try :
            user_data = UserData.objects.get(id = user.id)
            commission = UserCommissions.objects.filter(user__user=user_data)
            intial_commission =0
            if commission:
                for each in commission:
                    each_commission = each.commission_amount
                    intial_commission += each_commission
                total_user_commission = intial_commission
                return Response({'commission' : total_user_commission}, status=status.HTTP_200_OK)
            else :
                return Response({'commission': 0}, status=status.HTTP_200_OK) 
        except UserData.DoesNotExist:
            return Response({'message' : 'Something whent wrong...PLease try again'}, status= status.HTTP_400_BAD_REQUEST)



#Done api in excel ^^
        
#Gross sale of a particualr user(total sale amount) iesum of total price of all the product slled under tha user
class TotalGrossSaleOfEachUser(APIView):
    def get(self, request):
        user = request.user
        try:
            user_data = UserData.objects.get(id = user.id)
            user_related_link = UserCommissions.objects.filter(user__user = user_data)
            initial_amount = 0
            for each in user_related_link:
                initial_amount += each.product.subcription_fee
            user_gross_sale = initial_amount
            return Response({'commission' : user_gross_sale}, status=status.HTTP_200_OK)

        except UserData.DoesNotExist:
            return Response({'message' : "Something when wrong please try again"}, status= status.HTTP_400_BAD_REQUEST)


#Gross sale of a particualr product(total sale amount) ie sum of total price of  the product selled 
class TotalGrossSaleofEachProduct(APIView):
    def get(self, request, product_id):
        user = request.user
        try:
            product = Product.objects.get(id = product_id)
            products_related_obj = UserCommissions.objects.filter(product = product)
            # initial_amount = 0
            initial_amount = sum(each.product.subcription_fee for each in products_related_obj)
            product_gross_sale = initial_amount
            return Response({'commission' : product_gross_sale}, status=status.HTTP_200_OK)

        except UserData.DoesNotExist:
            return Response({'message' : "Something when wrong please try again"}, status= status.HTTP_400_BAD_REQUEST)



class TotalGrossSaleInAdminSide(APIView):
    def get(self, request):
        user = request.user
        try:
            # product = Product.objects.get(id = product_id)
            admin_products_related_obj = UserCommissions.objects.all()
            # initial_amount = 0
            initial_amount = sum(each.product.subcription_fee for each in admin_products_related_obj)
            padmin_roduct_gross_sale = initial_amount
            return Response({'commission' : padmin_roduct_gross_sale}, status=status.HTTP_200_OK)

        except UserData.DoesNotExist:
            return Response({'message' : "Something when wrong please try again"}, status= status.HTTP_400_BAD_REQUEST)
        


        