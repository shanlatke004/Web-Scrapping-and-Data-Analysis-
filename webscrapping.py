import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def real_time_price(stock_code):
    url = 'https://ca.finance.yahoo.com/quote/' + stock_code + '?.tsrc=fin-srch'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text,'lxml')
        # texts = web_content_div(web_content,'My(6px) Pos(r) smartphone_Mt(6px)')
        price = web_content.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
        change = web_content.find('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text

    except ConnectionError:
        price, change = []
    return price, change

def save_to_csv(data, file_name='stock_prices.csv'):
    df = pd.DataFrame(data)
    df.to_csv(file_name, mode='a', header=not pd.DataFrame().append(data).isin(pd.read_csv(file_name)).all().all(), index=False)

# Stock = ['RY.TO', 'BNS.TO', 'TD.TO', 'TRP.TO']
# for stock_code in Stock:
#     price, change = real_time_price(stock_code)
#     print(f"{stock_code}: Price = {price}, Change = $ {change}")

Stock = ['RY.TO', 'BNS.TO', 'TD.TO', 'TRP.TO']
data = {'Date': [],'Stock Code': [], 'Price': [], 'Change': []}

for stock_code in Stock:
    price, change = real_time_price(stock_code)
    now = datetime.datetime.now()
    data['Date'].append(now.strftime('%Y-%m-%d'))
    data['Stock Code'].append(stock_code)
    data['Price'].append(price)
    data['Change'].append(change)

save_to_csv(data)
print("Data written to stock_prices.csv")

