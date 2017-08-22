from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from Project.models import Customer,historical_data,shares,Transaction
import hashlib

# Create your views here.
def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def equity(request):
    return render(request,"equity.html")

def index(request):
    return render(request,"index.html")

def login(request):
    if 'user-trade' in request.COOKIES:
        return HttpResponseRedirect("/dashboard/")
    return render(request,"login.html")

def news(request):
    return render(request,"news.html")

def portfolio(request):
    return render(request,"portfolio.html")

def products(request):
    return render(request,"products.html")

def services(request):
    return render(request,"service.html")

def signup(request):
    return render(request,"sign-up.html")

def single(request):
    return render(request,"single.html")

def sitemap(request):
    return render(request,"sitemap.html")

@csrf_exempt
def dashboard(request):
    if 'user-trade' in request.COOKIES:
        return render_to_response("dashboard.html")
    if request.method == 'POST':
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        hashed_password = hashlib.sha256(password.encode('utf-8'))
        response = HttpResponseRedirect("/dashboard/")
        try :
            res = Customer.objects.get(email=username)
            obj = Customer.objects.filter(email=username,password=hashed_password.hexdigest())
            print(len(obj))
            if len(obj) == 1:
                response.set_cookie('user-trade',username)
                return response
            else :
                return HttpResponseRedirect("/login-wrong-password/")
        except Customer.DoesNotExist:
            return HttpResponseRedirect("/signup-unregistered/")
    else:
        return HttpResponseRedirect("/login-required/")


def user(request):
    if not 'user-trade' in request.COOKIES:
        print(request.COOKIES['user-trade'])
        return HttpResponseRedirect("/login-required/")
    return render_to_response("user.html")

def pasttransaction(request):
    if not 'user-trade' in request.COOKIES:
        print(request.COOKIES['user-trade'])
        return HttpResponseRedirect("/login-required/")
    return render_to_response("pasttransaction.html")

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        name = str(request.POST['name'])
        email = str(request.POST['email'])
        number = int(request.POST['number'])
        password = str(request.POST['password'])
        hashed_password = hashlib.sha256(password.encode('utf-8'))
        try :
            res = Customer.objects.get(email=email)
            return HttpResponseRedirect("/signup-registered/")
        except Customer.DoesNotExist:
            user = Customer(name=name,email=email,password=hashed_password.hexdigest(),phonenumber=number)
            user.save()
            return render(request,"index.html")
    else:
        return HttpResponseRedirect("/home/")

def logout(request):
    response = HttpResponseRedirect('/home/')
    response.delete_cookie('user-trade')
    return response