#!/usr/bin/env python3

import requests
import json
import pprint

url = "https://www.alphavantage.co/query"
function = "TIME_SERIES_INTRADAY"
symbol = "TITAN"
interval = "60min"
outputsize = "full"
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
#string['Meta Data']

time = string['Meta Data']['3. Last Refreshed']
print(string['Time Series (60min)'][time]['4. close'])



