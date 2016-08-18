from bs4 import BeautifulSoup as bs
import urllib2
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
import numpy as np

search_term = raw_input('Search term: ')
url = 'http://www.ebay.com/sch/i.html?_nkw=' + search_term.replace(' ', '+')
if (raw_input('Sold only (y/n) ? ') == 'y'):
    url = url + '&LH_Complete=1&LH_Sold=1'

req = urllib2.Request(url, headers=hdr)
page = urllib2.urlopen(req)
soup = bs(page.read(), 'html.parser')
price_raw = soup.find_all('span', {'class':'bold bidsold'})
price_list = []
for p in price_raw:
    price_list.append(float(p.contents[0].replace('$','').replace(',','')))

std_range = int(raw_input('Standard deviations to include (1/2/3): '))
price_mean = np.mean(price_list)
price_std = np.std(price_list)
price_del = []
# for (i, p) in enumerate(price_list.reverse()):
#     if (np.abs(p - price_mean) > std_range*price_std):
#         print p
#         price_del.append(p)
#         price_list[i] = -1
        
i = 0
while (i<len(price_list)):
    p = price_list[i]
    if (np.abs(p - price_mean) > std_range*price_std):
        price_del.append(p)
        del price_list[i]
    else:
        i = i+1 
        
print 'Prices included: ' + repr(price_list)
print 'Prices deleted: ' + repr(price_del)
print 'Average price: ' + repr(sum(price_list)/len(price_list))
print 'Min/max: ' + repr(np.min(price_list)) + '/' + repr(np.max(price_list))