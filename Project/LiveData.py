import urllib.request
import time
import csv
import ast
import requests
import re

'''
    format of output expected from google finance is of total 36 columns in those few of them are either empty or unknown.
    
    1. ID, 
    2. Ticker, 
    3. Name, 
    4. Ticker, 
    5. Exchange, 
    6. Currency, 
    7. Price, 
    8. Change, 
    9. Unknown, 
    10. Change%, 
    11. Unknown, 
    12. EPS, 
    13. PE, 
    14. PB, 
    15. PS, 
    16. Cap, 
    17. EntValue, 
    18. Div, 
    19. DivYield, 
    20. CurrRatio, 
    21. LtDebtToAssets, 
    22. TotalDebtToAssets, 
    23. LtDebtToEquity, 
    24. TotalDebtToEquity, 
    25. ReturnOnAvgAssets, 
    26. ReturnOnAvgEquity, 
    27. ReturnOnAvgInvestment, 
    28. Beta, 
    29. NetProfitMargin, 
    30. GrossMargin, 
    31. EBITDMargin, 
    32. OperatingMargin, 
    33. Employees, 
    34. Revenue, 
    35. NetIncome, 
    36. EBITDA
    
    these are the total 36 columns in the sequence of API.
'''
data = []
def get_data_csv():
    stock_name_list = []
    with open('Project/NSE-datasets-codes.csv', newline='') as csvfile :
        data = csv.reader(csvfile, delimiter = "\n")
        for rows in data:
            temp_list = rows[0].split('|')
            stock_name_list.append(temp_list[4])
    data = get_data(stock_name_list)
    return data

def get_data(stock_name_list):
    query_pt1 = 'https://finance.google.com/finance/data?dp=mra&output=json&catid=all&cid='
    query_pt2 = ','.join(stock_name_list)
    query = query_pt1+query_pt2
    tempData = []
    data = requests.get(query)
    data = str(data.text)
    data = re.sub(r'.*rows:','',data)
    data = data.split("],visible")[0]
    data = data[1:-1]
    data = data.split("},{")

    for crap in data :
        crap = re.sub(r'.*values:',"",crap)
        crap = ast.literal_eval(crap)
        tempData.append(crap)

    data = tempData
    return data

get_data_csv()