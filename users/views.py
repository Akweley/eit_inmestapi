from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib.auth import authenticate, login

from users.models import IMUser
from .models import *
from .serializers import *

from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action

from inmest_api.utils import *


# Create your views here.

def signup(request):
    username = request.POST["username"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    phone_number = request.POST["phone_number"]
    password = request.POST["password"]

    new_user = IMUser.objects.create(
        username = username,
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number
    )
    new_user.set_password(password)
    new_user.save()
    # new_user_generatetoken
    serializer = AuthSerializer(new_user, many=False)
    return Response({"message": "Account successfully created", "result": serializer.data})


def say_hello(req):
    return HttpResponse("<h1>Hello Fleur</h1>")

# create user_profile in a view function. let it return a json response
# name: your name, email: your email, phone_number: your phone number
# register the view function on a path called profile



def get_profile(req):
    user_profile = {
        "name": "AkweleyOkai",
        "email": "akweley.okai@meltwater.org",
        "phone_number": "0590000000"
        }
    return JsonResponse(user_profile)


# write a view function called filter_queries
# 1a. the view function should receive query_id through the url
# 1b. return a jsonresponse data with the following data:
# - id, title, description, status and submitted_by
# 1c. the id should be the id received through the url


def filter_queries(req,id):
    return JsonResponse(
    {
        "id" : id,
        "title" : "mental health break",
        "description" : "Adama left his girlfriend",
        "status" : "SINGLE",
        "submitted_by" : "Abena"
    }
    )
    
class QueryView(View):  

    queries = [
        {"id": 1,"title": "Adama declined Val shots"},
        {"id": 2,"title": "Adama declined Val shots"},
        ]   
    def get(self, request):        
        return JsonResponse({"result" : self.queries})
    
    def post(self, request):
        return JsonResponse({"status" : "ok"})


class UserViewSet(viewsets.ModelViewSet):
  
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password', None)
        player_id = request.data.get('player_id', None)

        user = authenticate(email=email, password=password)
        login(request, user)
   
    
#To create an API view for an existing user to login an app:
    
@api_view(["POST"])
@permission_classes([AllowAny])    
def login(request):
#Receive inputs/data from client and validate inputs
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "My friend behave yourself and send me username and password"}, status.HTTP_400_BAD_REQUEST)

    #2. Check user existence
    try:
        user = IMUser.objects.get(username=username)
#User authentication
        auth_user = authenticate(username=username, password=password)
        if auth_user:
#Login user
            login(username, password)
            serializer=AuthSerializer()
            return Response({"result": serializer.data})
        else:
            return Response({"detail": "Invalid credentials"}, status.HTTP_400_BAD_REQUEST)
    
    except IMUser.DoesNotExist:
        return Response({"detail": "Username does not exist"}, status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@permission_classes([AllowAny])
#Respond to the user's request
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                user.temporal_login_fail = 0
                user.save()
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Your account is inactive.'}, status=403)
        else:
            user = IMUser.objects.get(username=username)
            user.temporal_login_failed += 1
            user.permanent_login_fail += 1
            user.save()
            return JsonResponse({'error': 'Invalid username or password.'}, status=401)
        

class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        #1. receive the username (email)
        username = request.data.get("username")
        if not username:
            return generate_400_response("Please provide valid username")
        #2. Check if the user exists
        try:
            user = IMUser.objects.get(username=username)
            otp_code = generate_unique_code()
        #3. send OTP code
            user.unique_code = otp_code
            user.save()
            #send email or sms at this point

        #4. Respond to the user
            return Response({"detail": "Please check your email for an OTP code"}, status.HTTP_200_OK)
        
        
        except IMUser.DoesNotExist:
            return generate_400_response("Username does not exist")
    

class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        unique_code = generate_unique_code()
        new_password = request.data.get('new_password')

        if not username or not unique_code or not new_password:
            return Response({'error': 'Username, unique code, and new password are required.'}, status.HTTP_400_BAD_REQUEST)

        try:
            myuser = IMUser.objects.get(username=username, unique_code=unique_code)
            myuser.unique_code= ""
            myuser.temporal_login_failed = 0
            myuser.permanent_login_fail = 0
            myuser.set_password(new_password)
            myuser.is_active = True
            myuser.is_blocked = False
            

            user = AuthSerializer(myuser, context={'request': request})
            return Response()

            
            if user.unique_code != unique_code:
                return generate_400_response("Invalid code")
            
            
            myuser.save()
            return Response({'message': 'Password reset successful.'}, status.HTTP_200_OK)
        
        except IMUser.DoesNotExist:
            return generate_400_response("Username does not exist")
        
class CurrentUserProfileAPIView(APIView):
    permission_classes = [AllowAny]

    # fetches a user's profile

    def get(self, request, *args, **kwargs):
        user = UserSerializer(request.user, many=False, context={'request': request})
        return Response({'results': user.data, 'response_code': '100'}, status=200)       

    def put(self, request, *args, **kwargs):
        user = request.user
        profile = request.data

        


class ChangePasswordAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        username = request.user.username
        
        if old_password is None:
            return Response({'detail': 'Please provide old password', 'response_code': '101'}, status=400)

        if new_password is None:
            return Response({'detail': 'Please provide new password', 'response_code': '101'}, status=400)


        if old_password == new_password:
            return Response({'detail': "Old password and new password must not be the same", 'response_code': '101'}, status.HTTP_400_BAD_REQUEST)

        if not old_password or not new_password:
            return Response({'error': 'Old password and new password are required.'}, status.HTTP_400_BAD_REQUEST)

        user = request.user

        if not user.check_password(old_password):
            return Response({'error': 'Incorrect old password.'}, status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'}, status.HTTP_200_OK) 