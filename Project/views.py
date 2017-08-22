rom django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from Project.models import Customer,historical_data,shares,Transaction
import hashlib

# Create your views here.
def about(request):
    return render_to_response("about.html")

def contact(request):
    return render_to_response("contact.html")

def equity(request):
    return render_to_response("equity.html")

def index(request):
    return render_to_response("index.html")

def login(request):
    return render_to_response("login.html")

def news(request):
    return render_to_response("news.html")

def portfolio(request):
    return render_to_response("portfolio.html")

def products(request):
    return render_to_response("products.html")

def services(request):
    return render_to_response("service.html")

def signup(request):
    return render_to_response("sign-up.html")

def single(request):
    return render_to_response("single.html")

def sitemap(request):
    return render_to_response("sitemap.html")

def dashboard(request):
    return render_to_response("dashboard.html")

@csrf_exempt
def auth(request):
    if request.method == 'POST':
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        hashed_password = hashlib.sha256(password.encode('utf-8'))

        try :
            res = Customer.objects.get(email=username)
            obj = Customer.objects.filter(email=username,password=hashed_password.hexdigest())
            print(len(obj))
            if len(obj) == 1:
                return HttpResponseRedirect("/dashboard/")
            else :
                return HttpResponseRedirect("/login-wrong-password/")
        except Customer.DoesNotExist:
            return HttpResponseRedirect("/signup-unregistered/")
    else :
        return HttpResponseRedirect("/login-required/")

def user(request):
    return render_to_response("user.html")

def pasttransaction(request):
    return render_to_response("pasttransaction.html")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        name = str(request.POST['name'])
        email = str(request.POST['email'])
        number = int(request.POST['number'])
        password = str(request.POST['password'])
        hashed_password = hashlib.sha256(password.encode('utf-8'))

        print(number)
        try :
            res = Customer.objects.get(email=email)
            return HttpResponseRedirect("/signup-registered/")
        except Customer.DoesNotExist:
            user = Customer(name=name,email=email,password=hashed_password.hexdigest(),phonenumber=number)
            user.save()
            return render_to_response("index.html")
    else:
        return HttpResponseRedirect("/home/")