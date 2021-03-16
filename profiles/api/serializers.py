# DRF
from rest_framework import serializers

# Models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import UserDetailsSerializer
from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField('get_profile_url')
    
    def get_profile_url(self, obj):
        return obj.get_absolute_url()
    
    class Meta:
        model = Profile
        exclude = ['user', 'created_on', 'updated_on']
        

class ProfileMinSerialzer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField('get_profile_url')
    
    def get_profile_url(self, obj):
        return obj.get_absolute_url()
    
    class Meta:
        model = Profile
        fields = ['id', 'profile_image', 'profile_url']
        

class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        exclude = ['user']


class UserMinSerializer(serializers.ModelSerializer):
    profile = ProfileMinSerialzer(many=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class UserSerializer(UserDetailsSerializer):

    profile = ProfileSerializer()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile',)

    def update(self, instance, validated_data):
        userprofile_serializer = self.fields['profile']
        userprofile_instance = instance.userprofile
        userprofile_data = validated_data.pop('profile', {})

        # to access the 'company_name' field in here
        # company_name = userprofile_data.get('company_name')

        # update the userprofile fields
        userprofile_serializer.update(userprofile_instance, userprofile_data)

        instance = super().update(instance, validated_data)
        return instance
        
