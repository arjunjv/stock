from nsetools import Nse
from pprint import pprint # just for neatness of display


nse = Nse()
print nse
#while(1):
q = nse.get_quote('') # it's ok to use both upper or lower case for codes.
pprint.pprint(q)
print(q['lastPrice'])
