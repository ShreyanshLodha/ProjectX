import quandl
import csv
import Project.authKey
import datetime
from Project.models import shares,historical_data
quandl.ApiConfig.api_key = Project.authKey.QuandlKey
import time

# Output format from Quandl is as follows
'''
    Open
    High
    Low
    Close
    Total Trade Quantity
    Turnover (Lacs)
'''
stock_list = []
stock_dict = {}
def dataFetcher():
    print("INIT")
    with open('Project/NSE-datasets-codes.csv', newline='') as csvfile :
        data = csv.reader(csvfile, delimiter = "\n")
        for rows in data:
            apiMaker(rows)

    history()

def apiMaker(rows):
    temp_list = rows[0].split('|')
    d = {
        'stock_code': temp_list[0],
        'stock_name': temp_list[1],
        'ceo': temp_list[2],
        'desc': temp_list[3],
        'google_id': temp_list[4]
    }
    try:
        obj = shares.objects.get(stock_code=d['stock_code'])
    except shares.DoesNotExist:
        create = shares(google_id=d['google_id'], stock_code=d['stock_code'], stock_name=d['stock_name'], ceo_name=d['ceo'], comp_desc=d['desc'])
        create.save()
    stock_list.append(d.copy())

def history():
    prev_day = str(datetime.date.today() - datetime.timedelta(3))

    for items in stock_list:
        name = str(items['stock_code'])
        sid = shares.objects.values_list('sid',flat=True).get(stock_code=name)
        try :
            last_date_of_data_available = historical_data.objects.filter(sid = sid).values_list('date',flat=True).latest('date')
            if str(last_date_of_data_available) != str(prev_day):
                last_date_of_data_available += datetime.timedelta(days=1)
                flag = None
                while flag is None:
                    try:
                        db_insertion(name,last_date_of_data_available,prev_day)
                        flag = 2
                    except:
                        time.sleep(1)
                        print("Retry for stock ",name)

            else:
                print("Data is up-to date for Stock", name)
        except historical_data.DoesNotExist:
            flag = None
            while flag is None:
                try:
                    db_insertion(name, '2017-04-01', prev_day)
                    flag = 1
                except :
                    pass

def db_insertion(name,start_date,end_date):
    # get Stock ID from share table
    stock_id = shares.objects.values_list('sid', flat=True).get(stock_code=name)
    print("Stock ID", stock_id, "Stock ", name)
    data = quandl.get(name,
                      start_date=start_date, end_date=end_date,collapse='daily')
    # to get list of dates we have data for.
    dates = (list(data['Open'].keys()))
    stock_date = []
    for value in dates:
        tempdate = str(value)

        # to remove time from time-stamp and keep only date
        tempdate = tempdate.replace(' 00:00:00', '')
        stock_date.append(tempdate)

    # to get Opening price of stock
    stock_open = []
    for opening in data['Open']:
        stock_open.append(opening)

    # to get Closing price of stock
    stock_close = []
    for closing in data['Close']:
        stock_close.append(closing)

    # to get Highest price of stock
    stock_high = []
    for highest in data['High']:
        stock_high.append(highest)

    # to get Lowest price of stock
    stock_low = []
    for lowest in data['Low']:
        stock_low.append(lowest)

    counter = 0
    for value in stock_date:
        if stock_open[counter] is None:
            continue
        # insert data
        row_insert = historical_data(date=value,
                                     open_price=stock_open[counter],
                                     close_price=stock_close[counter],
                                     highest_p=stock_high[counter],
                                     lowest_p=stock_low[counter],
                                     sid=shares.objects.get(sid=stock_id))
        counter += 1
        row_insert.save()

