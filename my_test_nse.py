#!/usr/bin/env python3
from __future__ import print_function

import json
import requests
import csv
#import pprint




url = 'https://www.nseindia.com/content/equities/EQUITY_L.csv'

def get_stock_codes(self, cached=True, as_json=False):
        """
        returns a dictionary with key as stock code and value as stock name.
        It also implements cache functionality and hits the server only
        if user insists or cache is empty
        :return: dict
        """
        req = requests.get(url)
        res_dict = {}
        
	# raises HTTPError and URLError
        res = self.opener.open(req)
        if res is not None:
             # for py3 compat covert byte file like object to
             # string file like object
          res = byte_adaptor(res)
          for line in res.read().split('\n'):
           if line != '' and re.search(',', line):
            (code, name) = line.split(',')[0:2]
            res_dict[code] = name
                    # else just skip the evaluation, line may not be a valid csv
        else:
         raise Exception('no response received')
        print(res_dict)
        return res_dict



if __name__ == __mian__():
	get_stock_codes()









"""

page = requests.get(url)

csvfile = 'EQUITY_L.csv'
with open(csvfile, 'w') as f:
    writer = csv.writer(f)
    reader = csv.reader(page.text.splitlines())

    for row in reader:
        writer.writerow(row)

 
reader = csv.reader(csvfile, delimiter=' ')
       included_cols = [1,2]

    for row in reader:
            content = list(row[i] for i in included_cols)
            print content

"""
	
