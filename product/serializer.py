from rest_framework import serializers


from .models import Product,RefferalLink,RegionData,UserPaymentDetailsOfProduct,PaymentRquest
from userapp.models import UserData, UserDetails
from userapp.serializer import UserDataSerializer, UserRequestingforUpgradingToOrganiser, UserDetailsSerializer


class ProductSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RefferalLinkSerializer(serializers.ModelSerializer):
    product = ProductSeriaizer(read_only=True)
    user = UserDataSerializer(read_only=True)
    user_details = UserDetailsSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(), source='product')   
    user_id = serializers.PrimaryKeyRelatedField(write_only = True, queryset=UserData.objects.all(), source='user')
    user_details_id = serializers.PrimaryKeyRelatedField(write_only = True, queryset=UserDetails.objects.all(), source='user_details',required = False)
    direct_referred_link_owner_id =serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='direct_referred_link_owner',required = False)   
    indirect_referred_link_owner_id =serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='indirect_referred_link_owner',required = False)   
    class Meta:
        model = RefferalLink
        fields = '__all__'


class UserRequestingforUpgradingToOrganiserSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(read_only=True)
    user_refferal_link = RefferalLinkSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='user', required = False)
    ref_link_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=RefferalLink.objects.all(), source='user_refferal_link', required = False)
    admin_user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='approved_or_reject_by', required = False)
    class Meta:
        model = UserRequestingforUpgradingToOrganiser
        fields = '__all__'


