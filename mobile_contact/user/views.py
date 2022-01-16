
from django.db.models import Q
from django.http import request, response
from .serializer import UserReg_Serialzer,LoginSerializer,UserSearchserializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from .models import Golbal_users, User
from user import serializer


# Create your views here.

# ----------------User registration -----------------#
class UserRegistration(generics.GenericAPIView,mixins.CreateModelMixin):    
    def post(self, request):
        serializer = UserReg_Serialzer(data = request.data)
        if serializer.is_valid():
        
            if request.data.get('email'):
                user = User.objects.create_user(name = request.data.get('name'),
                                                mobile_number = request.data.get('mobile_number'),email = request.data.get('email'),password = request.data.get('password'))
                
                userglobal = Golbal_users.objects.create(Name = request.data.get('name'),
                                                         mobile_number = request.data.get('mobile_number'),is_registered = True,email = request.data.get('email'))
            else:
                user = User.objects.create_user(name = request.data.get('name'),mobile_number = request.data.get('mobile_number')
                                                ,password = request.data.get('password') )
                
                userglobal = Golbal_users.objects.create(Name = request.data.get('name'),
                                                         mobile_number = request.data.get('mobile_number'),is_registered = True)
            user.save()
            userglobal.save()
            message = {'success': "user Created successfully",'Name':request.data.get('name')}
            return Response(message,status=status.HTTP_201_CREATED)
        else:
            message = {"error":"user not Created"}
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#------------- user login view ----------------- #    
class UserLogin(APIView): 
    def post(self, request):
        try:
            mobile_number = request.data.get('mobile_number')
            password = request.data.get('password')
            
            user = authenticate(username=mobile_number, password=password)
            serializers = LoginSerializer(user)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    
                    return Response({
                        "user"  : serializers.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },status = status.HTTP_200_OK)
                else:
                    message = {"error":"user is not activate"}
                    return Response(message,status=status.HTTP_404_NOT_FOUND)
            else:
                message = {"error" : "invalide password or username"}
                return Response(message,status=status.HTTP_404_NOT_FOUND)
        except:
            message = {"error" : "clients side error"}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        

#--------------user contact import---------------#
class import_contact(APIView):
    authentication_classes =  [JWTAuthentication]
    permission_classes     =  [IsAuthenticated]
    def post(self,request):
        try:
            mobile_number = request.data.get('mobile_number')
            name = request.data.get('Name')
            globel_user = Golbal_users.objects.create(Name = name,mobile_number = mobile_number)
            globel_user.save()
            messages = {'success': "added successfully"}
            return Response(messages,status=status.HTTP_201_CREATED)
        except:
            message = {"error" : "clients side error"}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
            
     
#----------------user searchview--------------#
class UserSearchView(APIView):
    authentication_classes =  [JWTAuthentication]
    permission_classes     =  [IsAuthenticated]
    def post(self,request):
        search = request.data.get('search')
        print(type(search))
        users = Golbal_users.objects.filter(Q(Name__istartswith = search) | Q(Name__icontains = search) | Q(mobile_number__istartswith = str(search)) | Q(mobile_number__icontains = str(search)))
        serializer =  UserSearchserializer(users,many = True)
        if  type(search) == int:
            for user in users:
                if user.is_registered:
                    UserSearchserializer(user,many = True)
                    return Response({"mail":user.email}, status = status.HTTP_200_OK)
        return Response(serializer.data, status = status.HTTP_200_OK)


 #----------------spam reporting-----------------#   
class SpamReport(APIView):
    authentication_classes =  [JWTAuthentication]
    permission_classes     =  [IsAuthenticated]
    def post(self,request):
        try:
            mobile_number = request.data.get('mobile_number')
            globel_user = Golbal_users.objects.get(mobile_number = mobile_number)
            globel_user.spam =  globel_user.spam + 1
            globel_user.save()
            return Response({"message": "Successfully reported"},status=status.HTTP_201_CREATED) 
        except:
            message = {"error" : "clients side error"}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        
      
#----------- email adding----------#  
class Emailadding(APIView):
    authentication_classes =  [JWTAuthentication]
    permission_classes     =  [IsAuthenticated]
    def patch(self,request):
        email = request.data.get('email')
        user = User.objects.get(id = request.user.id)
        user.email = email
        user.save()
        return Response({"message": "email added"})
            