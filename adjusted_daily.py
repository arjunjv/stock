#!/usr/bin/env python3

import requests
import json
import pprint

url = "https://www.alphavantage.co/query"
function = "TIME_SERIES_DAILY_ADJUSTED"
symbol = "NSE:TATAGLOBAL"
interval = "60min"
outputsize = "compast"
api_key = "Q7DW5F7WK48Z7YRR" #   <-- goes here your API KEY

data = { "function": function,
         "symbol": symbol,
	 "interval": interval,
	 "outputsize": outputsize,
         "apikey": api_key }

page = requests.get(url, params = data)
#pprint.pprint(page.json())
#print (page.url)
#print (data)
string = json.loads(str(page.text))

#dict = string['Meta Data']

#print(dict[ '4. Output Size'])
#print(string['Time Series (Daily)']

date = string['Meta Data']['3. Last Refreshed']

final = string['Time Series (Daily)'][date]['5. adjusted close']
day_start  = string['Time Series (Daily)'][date]['1. open']
print(day_start)
print(final)
percentile_change = ((float(final)-float(day_start))/float(day_start))*100
percentile_change = (int(percentile_change*100))/100
print ("The Price of %s on %s is %s, the day cahnge is %s"%(symbol,date,final,percentile_change))




