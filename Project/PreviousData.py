import quandl
import csv
import authKey

quandl.ApiConfig.api_key = authKey.QuandlKey
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
    with open('NSE-datasets-codes.csv', newline='') as csvfile :
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
    stock_list.append(d.copy())

def history():
    for items in stock_list:
        name = str(items['stock_code'])
        data = quandl.get([name.__add__(".1"),name.__add__(".5"),name.__add__(".2"),name.__add__(".3")], start_date="2017-04-01", end_date="2017-04-30")
        print(data)
        data = quandl.get([name.__add__(".1"),name.__add__(".5"),name.__add__(".2"),name.__add__(".3")], start_date="2017-05-01", end_date="2017-05-31")
        print(data)
# todo : choose top 50 with longest duration of data
# todo : Format the data as per the needs.
# todo : Insert data into database

dataFetcher()