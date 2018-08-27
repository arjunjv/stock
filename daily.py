#!/usr/bin/env python3

import requests
import json
import pprint

url = "https://www.alphavantage.co/query"
function = "TIME_SERIES_DAILY"
symbol = "TATAGLOBAL"
api_key = "Q7DW5F7WK48Z7YRR" #   <-- goes here your API KEY

data = { "function": function,
         "symbol": symbol,
         "apikey": api_key }

page = requests.get(url, params = data)
pprint.pprint(page.json())
print (page.url)
string = json.loads(str(page.text))
#string['Meta Data']

#dict = string['Meta Data']

#print(dict[ '4. Output Size'])



