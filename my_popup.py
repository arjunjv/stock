#!/usr/bin/env python3

import requests
import json
import tkinter
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
print(page)
print (type(page))
string = json.loads(str(page.text))


time = string['Meta Data']['3. Last Refreshed']
final = string['Time Series (60min)'][time]['4. close']
final = float(final)
print (type(final))
print (final)



while(final <= 816.5) :

	time = string['Meta Data']['3. Last Refreshed']
	final = string['Time Series (60min)'][time]['4. close']
	final = float(final)
	print (final)


top = tkinter.Tk()


