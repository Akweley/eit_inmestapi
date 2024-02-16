from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View

from users.models import IMUser


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
    

