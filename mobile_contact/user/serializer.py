from django.contrib.postgres import fields
from user import models
from user.models import Golbal_users, User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator




class UserReg_Serialzer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),message=("Email already exists"))],read_only = True)
                                        
    class Meta:
        model = User
        fields =['id', 'name', 'password','mobile_number','email']
        
        extra_kwargs = {'password':{
        'write_only':True,
        'required' : True
        }}
        
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.ModelSerializer):
     class Meta: 
        model = User
        fields =['mobile_number', 'password']
        
        extra_kwargs = {'password':{
        'write_only':True,
        'required' : True
        }}
        

class UserSearchserializer(serializers.ModelSerializer):
    class Meta:
        model = Golbal_users
        fields = ['Name','mobile_number','spam']