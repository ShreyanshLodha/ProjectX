import datetime
import requests
import re
import ast

def time_analysis():
    interval = 1
    market_status = True
    # get current date
    curr_time = datetime.datetime.now()
    HH_curr = curr_time.hour
    MM_curr = curr_time.minute

    # Market Opening Time
    _HHOpen = 9
    _MMOpen = 15

    # Market Closing Time
    _HHClose = 15
    _MMClose = 30

    # Decide interval for different times.
    if HH_curr >=_HHClose or HH_curr <= _HHOpen:
        if HH_curr>= _HHOpen and MM_curr >= HH_curr:
            interval = 1
        else:
            interval = 10

    elif HH_curr == 10:
        interval = 2

    elif HH_curr <= 11:
        interval = 4

    elif HH_curr <= 13:
        interval = 6


    # Check if Market is open at current time.
    if HH_curr <=_HHOpen:
        market_status = False
        if HH_curr == _HHOpen and MM_curr >= _MMOpen:
            market_status = True

    elif HH_curr>= _HHClose:
        market_status = False
        if HH_curr == _HHClose and MM_curr <= _MMClose:
            market_status = True

    result = {
        'MarketStatus' : market_status,
        'TimeInterval' : interval
    }
    return result

def fetch_query(url,interval):
    # fetch data from google finanace
    request = requests.get(url)
    # convert the response into text
    data = str(request.text)

    # remove unnecessary data from the text
    data = data.split("TIMEZONE_OFFSET=330")
    data = data[1]
    data = data.split('\n')
    data = data[1:-1]

    # dealing with time
    curr_time = datetime.datetime.now()
    opening_time = curr_time.replace(hour=9,minute=15,second=00)
    length = len(data)
    time_list = []

    # Create time string for all the items available
    for x in range(0,length):
        time_list.append(opening_time)
        opening_time = opening_time + datetime.timedelta(minutes=interval)

    time_list_string = []
    # Converting datetime to string
    for items in time_list:
        time_list_string.append(str(items))

    time_list = time_list_string

    return data, time_list

def get_detailed_info(id):
    # send request for the stocks available
    query = 'https://finance.google.com/finance/data?dp=mra&output=json&catid=all&cid='+str(id)
    data = requests.get(query)
    data = str(data.text)

    # Purify response and keep relevant content
    data = re.sub(r'.*rows":','',data)
    data = data.split('],"visible')[0]
    data = data[1:-1]
    data = data.split("},{")
    data = data[0]
    data = re.sub(r'.*values":', "", data)
    print(data)

    # convert string like list to actual list

    data = ast.literal_eval(data)
    return data
