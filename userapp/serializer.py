from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserData, UserDetails, UserRequestingforUpgradingToOrganiser, RegionDataVillage
from product.models import RefferalLink



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print('ioioio')
        token = super().get_token(user)

        # Include the email in the token's payload
        token['email'] = user.email
        # print(user.uuid,'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        token['user_id'] =user.id
        return token



class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        # fields = '__all__'
        exclude = ['password']


class UserDetailsSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='user')
    class Meta:
        model = UserDetails
        fields = '__all__'




class RegionDataVillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionDataVillage
        fields = '__all__'




