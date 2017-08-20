from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render_to_response

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
