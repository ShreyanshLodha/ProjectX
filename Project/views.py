from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from Project.models import Customer,historical_data,shares,Transaction
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import hashlib
import os

# Create your views here.
def about(request):
    return render_to_response("about.html")

def contact(request):
    return render_to_response("contact.html")

def equity(request):
    return render_to_response("equity.html")

def home(request):
    return render_to_response("index.html")

def login(request):
    if 'user-trade' in request.COOKIES:
        return HttpResponseRedirect("/dashboard/")
    return render(request,"login.html")

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
@csrf_exempt
def single(request):
    # Show data in drop down menu of the Page
    stock_id = list(shares.objects.values_list('sid',flat=True))
    stock_name = list(shares.objects.values_list('stock_name', flat=True))
    stocks = {}
    stocks['id'] = stock_id
    stocks['names'] = stock_name
    stocks['i'] = zip(stocks['id'], stocks['names'])


    if request.method == "POST" and 'share' in request.POST:
        selected_share = int(request.POST['share'])
        price_list = []
        date_list = []

        duration = 0
        original_dir = os.getcwd()
        os.chdir('Project/static/images/')
        if os._exists("graph.png"):
            os.remove("graph.png")
        os.chdir(original_dir)
        # For 7 days
        if 'days7' in request.POST:
            duration = 7
            price_list = list(historical_data.objects.values_list('close_price', flat=True).filter(sid_id=selected_share).order_by('-date')[:7])
            price_list.reverse()
            date_list = list(historical_data.objects.values_list('date', flat=True).filter(sid_id=selected_share).order_by('-date')[:7])
            date_list.reverse()
        elif 'days30' in request.POST:
            duration = 30
            price_list = list(historical_data.objects.values_list('close_price', flat=True).filter(sid_id=selected_share).order_by('-date')[:30])
            price_list.reverse()
            date_list = list(
                historical_data.objects.values_list('date', flat=True).filter(sid_id=selected_share).order_by('-date')[
                :30])
            date_list.reverse()
        elif 'days90' in request.POST:
            duration = 90
            price_list = list(historical_data.objects.values_list('close_price', flat=True).filter(sid_id=selected_share).order_by('-date')[:90])
            price_list.reverse()
            date_list = list(
                historical_data.objects.values_list('date', flat=True).filter(sid_id=selected_share).order_by('-date')[
                :90])
            date_list.reverse()
        else:
            duration = 100
            price_list = list(historical_data.objects.values_list('close_price', flat=True).filter(sid_id=selected_share).order_by('date'))
            date_list = list(historical_data.objects.values_list('date', flat=True).filter(sid_id=selected_share).order_by('date'))

        # to make sure the graph doesnt touch floor and ceil
        max_price = max(price_list) + 10
        min_price = min(price_list) - 10

        # increase the size of the graph as we are displaying it on website
        # plt.figure(figsize=(8.0, 5.0))

        # set format of date on 'x' axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

        # set 'x' axis ticks for according to the content size
        if len(date_list) <= 30:
            plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
        else:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            plt.gca().xaxis.set_minor_locator(mdates.WeekdayLocator())

        # set fill and fill color according to the template color
        plt.gca().fill_between(date_list,0,price_list,facecolors="#ff5000")
        plt.plot(date_list,price_list, color='#000000')
        plt.ylim(min_price,max_price)
        plt.gcf().autofmt_xdate()

        # Basic Enhancements to graph
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title(str(stock_name[selected_share-1]))

        # save in static/image folder
        os.chdir('Project/static/images/')
        plt.savefig("graph.png")
        os.chdir(original_dir)

        # clean graph and close graph content
        plt.clf()
        # set 4 values required by content
        max_value = max(price_list)
        max_value_date = date_list[price_list.index(max(price_list))]
        min_value = min(price_list)
        min_value_date = date_list[price_list.index(min(price_list))]
        stocks['max_value'] = max_value
        stocks['max_value_date'] = max_value_date
        stocks['min_value'] = min_value
        stocks['min_value_date'] = min_value_date
        response = render_to_response("single.html", stocks)
        # set cookie
        response.set_cookie('share-selected', selected_share)
        response.set_cookie('share-duration', duration)
        return response
    else:
        response = render_to_response("single.html", stocks)
        return response

def sitemap(request):
    return render_to_response("sitemap.html")

def typography(request):
    return render_to_response("typography.html")

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
        return HttpResponseRedirect("/login-required/")
    return render_to_response("user.html")

def pasttransaction(request):
    if not 'user-trade' in request.COOKIES:
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