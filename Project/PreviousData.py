import quandl
import csv
import Project.authKey
import datetime
from Project.models import shares,historical_data
quandl.ApiConfig.api_key = Project.authKey.QuandlKey
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
        data = csv.reader(csvfile, delimiter = "\n", quotechar="|")
        for rows in data:
            apiMaker(rows)

    history()

def apiMaker(rows):
    temp_list = rows[0].split(',')
    d = {
        'stock_code' : temp_list[0],
        'stock_name' : temp_list[1]
    }
    try:
        obj = shares.objects.get(stock_code=d['stock_code'])
    except shares.DoesNotExist:
        create = shares(stock_code=d['stock_code'], stock_name=d['stock_name'])
        create.save()
    stock_list.append(d.copy())

def history():
    prev_day = str(datetime.date.today() - datetime.timedelta(1))

    for items in stock_list:
        name = str(items['stock_code'])
        sid = shares.objects.values_list('sid',flat=True).get(stock_code=name)
        try :
            last_date_of_data_available = historical_data.objects.filter(sid = sid).values_list('date',flat=True).latest('date')
            print(last_date_of_data_available)
            if last_date_of_data_available != prev_day:
                db_insertion(name,'2017-04-01',prev_day)
            else:
                print("Not inserting data for " , name)
        except historical_data.DoesNotExist:
            db_insertion(name, '2017-04-01', prev_day)

def db_insertion(name,start_date,end_date):
    # get Stock ID from share table
    stock_id = shares.objects.values_list('sid', flat=True).get(stock_code=name)
    print("Stock ID", stock_id)
    print("Stock ", name)
    data = quandl.get([name.__add__(".1"), name.__add__(".5"), name.__add__(".2"), name.__add__(".3")],
                      start_date=start_date, end_date=end_date,collapse='daily')
    # to get list of dates we have data for.
    dates = (list(data[name + ' - Open'].keys()))
    stock_date = []
    for value in dates:
        tempdate = str(value)

        # to remove time from time-stamp and keep only date
        tempdate = tempdate.replace(' 00:00:00', '')
        stock_date.append(tempdate)

    # to get Opening price of stock
    stock_open = []
    for opening in data[name + ' - Open']:
        stock_open.append(opening)

    # to get Closing price of stock
    stock_close = []
    for closing in data[name + ' - Close']:
        stock_close.append(closing)

    # to get Highest price of stock
    stock_high = []
    for highest in data[name + ' - High']:
        stock_high.append(highest)

    # to get Lowest price of stock
    stock_low = []
    for lowest in data[name + ' - Low']:
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

