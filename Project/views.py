from django.shortcuts import render
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from Project.models import customer,historical_data,shares,buy_transaction,sell_transaction
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pylab import rcParams
import hashlib
import os
import Project.LiveData
from django.core.mail import send_mail
from random import randint
import Project.LiveGraph
import dateutil

# Create your views here.
def about(request):
    return render_to_response("about.html")

def contact(request):
    return render_to_response("contact.html")

def equity(request):
    data = Project.LiveData.get_data_csv()
    return render_to_response("equity.html", {'data' : data})

def home(request):
    return render_to_response("index.html")

def login(request):
    if 'user-trade' in request.COOKIES and 'email' in request.session:
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
    # Delete old graph
    original_dir = os.getcwd()
    os.chdir('Project/static/images/')
    if os._exists("graph.png"):
        os.remove("graph.png")
    os.chdir(original_dir)

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
        stock_basic = (shares.objects.values_list('ceo_name','comp_desc').get(sid=selected_share))
        stock_CEO = stock_basic[0]
        stock_desc = stock_basic[1]
        duration = 0
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
        max_price = max(price_list) + 5
        min_price = min(price_list) - 5


        # increase the size of the graph as we are displaying it on website
        # plt.figure(figsize=(8.0, 5.0))

        # set format of date on 'x' axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

        # set 'x' axis ticks for according to the content size
        if len(date_list) <= 29:
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
        stocks['CEO'] = stock_CEO
        stocks['desc'] = stock_desc
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
    if 'user-trade' in request.COOKIES and 'email' in request.session:
        return render_to_response("dashboard.html")
    if request.method == 'POST':
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        hashed_password = hashlib.sha256(password.encode('utf-8'))
        response = HttpResponseRedirect("/dashboard/")
        try :
            res = customer.objects.get(email=username)
            two_step_check = list(customer.objects.values_list('two_step_validation',flat=True).filter(email=username,password=hashed_password.hexdigest()))
            obj = customer.objects.filter(email=username,password=hashed_password.hexdigest())
            if len(obj) == 1 and (two_step_check[0] == False):
                response.set_cookie('user-trade',username)
                request.session['email'] = username
                return response
            elif len(obj) == 1 and (two_step_check[0] == True):
                request.session['email'] = username
                return HttpResponseRedirect("/two_step_validation/")
            else:
                return HttpResponseRedirect("/login-wrong-password/")
        except customer.DoesNotExist:
            return HttpResponseRedirect("/signup-unregistered/")
    else:
        return HttpResponseRedirect("/login-required/")


def user(request):
    if 'user-trade' in request.COOKIES and 'email' in request.session:
        username = request.session['email']
        details = list(customer.objects.values_list().filter(email=username))[0]
        details = list(details)
        return render_to_response("user.html", {'details': details})
    else:
        return HttpResponseRedirect("/login-required/")

def pasttransaction(request):
    if 'user-trade' in request.COOKIES and 'email' in request.session:
        return render_to_response("pasttransaction.html")
    else:
        return HttpResponseRedirect("/login-required/")


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        name = str(request.POST['name'])
        email = str(request.POST['email'])
        number = int(request.POST['number'])
        password = str(request.POST['password'])
        hashed_password = hashlib.sha256(password.encode('utf-8'))
        try :
            res = customer.objects.get(email=email)
            return HttpResponseRedirect("/signup-registered/")
        except customer.DoesNotExist:
            user = customer(name=name,email=email,password=hashed_password.hexdigest(),phonenumber=number)
            user.save()
            return render(request,"index.html")
    else:
        return HttpResponseRedirect("/home/")

def logout(request):
    response = HttpResponseRedirect('/home/')
    response.delete_cookie('user-trade')
    if 'email' in request.session:
        del request.session['email']
    return response

def two_step_validation(request):
    OTP = randint(100000, 999999)
    if 'email' in request.session and 'OTP' not in request.POST:
        user = [str(request.session['email'])]
        request.session['OTP'] = OTP
        send_mail("OTP for Login", "The login OTP for 2 step Validation is : "+str(OTP),"admin@trademarket.com",user)
        return render_to_response("two-step-validation.html")
    else:
        return HttpResponseRedirect("/login-required/")

@csrf_exempt
def validate_second_stage(request):
    EnteredOTP = str(request.POST['OTP'])
    SentOTP = str(request.session['OTP'])
    Email = str(request.session['email'])
    if 'OTP' in request.POST and 'OTP' in request.session:
        if EnteredOTP == SentOTP:
            response = HttpResponseRedirect("/dashboard/")
            response.set_cookie('user-trade',request.session['email'])
            return response
        else:
            print(SentOTP, EnteredOTP, Email)
            del request.session['email']
            return HttpResponseRedirect("/login-wrong-password/")
    else:
        del request.session['email']
        return HttpResponseRedirect("/login-required/")

@csrf_exempt
def add_bal(request):
    if 'user-trade' not in request.COOKIES and 'email' not in request.session:
        return HttpResponseRedirect("/login-required/")
    return render_to_response("add-balance.html")

@csrf_exempt
def balance_check(request):
    if 'user-trade' not in request.COOKIES and 'email' not in request.session:
        return HttpResponseRedirect("/login-required/")
    if request.method == 'POST':
        page_response = []
        page_response.append(str(request.session['email']))
        page_response.append(int(request.POST['Amount']))
        old_bal = list(customer.objects.values_list('balance',flat=True).filter(email=page_response[0]))
        customer.objects.filter(email=page_response[0]).update(balance = old_bal[0]+float(page_response[1]))
        return HttpResponseRedirect("/dashboard/")

@csrf_exempt
def update_details(request):
    if 'user-trade' not in request.COOKIES and 'email' not in request.session:
        return HttpResponseRedirect("/login-required/")
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        two_step = True
        if 'fancy-checkbox-primary' in request.POST:
            two_step = True
        else:
            two_step = False
        email = request.session['email']
        customer.objects.filter(email=email).update(name = name, phonenumber = number, two_step_validation = two_step)
        return render_to_response('dashboard.html',{'message':True})


def live(request):
    time_data = Project.LiveGraph.time_analysis()

    # Convert interval into seconds
    interval = time_data['TimeInterval']*60

    # to get the stock ID of the stock selected by the user
    share_id_from_url = request.get_full_path()
    temp_variable  = share_id_from_url.rfind('/')
    share_id_from_url = share_id_from_url[temp_variable+1:]
    if int(share_id_from_url)>50 or int(share_id_from_url)<1:
        return HttpResponseRedirect("/equity/")

    # Code for sending request to google finance
    code = list(shares.objects.filter(sid=share_id_from_url).values_list('stock_code', flat=True))
    # to remove  NSE/ from the fetched value
    code = str(code[0])[4:]

    # take high price for every interval
    url = "https://finance.google.com/finance/getprices?q="+code+"&x=NSE&p=1d&f=h&i="+str(interval)
    rate_list, date_list = Project.LiveGraph.fetch_query(url,time_data['TimeInterval'])
    dates = [dateutil.parser.parse(s) for s in date_list]
    # graph related stuff starts here
    ax = plt.gca()
    ax.set_xticks(dates)

    xfmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[15,30,45]))
    plt.plot(dates, rate_list, color="#ff5000")
    plt.gcf().set_size_inches(16,6)
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel("Price")
    share_name = list(shares.objects.values_list('stock_name', flat=True).filter(sid=share_id_from_url))
    plt.title(str(share_name[0]))
    original_dir = os.getcwd()
    os.chdir('Project/static/images/')
    if os._exists("graphLive.png"):
        os.remove("graphLive.png")
    plt.savefig("graphLive.png")
    os.chdir(original_dir)
    plt.clf()
    plt.close()
    # graph related work ends here

    # get individual stock's ratio and other useful information
    # fetch ID which is supported by google
    google_id = list(shares.objects.filter(sid=share_id_from_url).values_list('google_id', flat=True))
    google_id = google_id[0]

    details = Project.LiveGraph.get_detailed_info(google_id)
    # TODO : To display these details with appropriate info in webpage

    return render_to_response("Live.html", {'data':details})