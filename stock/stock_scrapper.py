# Stock
import bs4
import requests
import pandas_datareader as web
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime

def parsePrice(stock_name):
	today = datetime.now().strftime("%Y-%m-%d")
	url = 'https://finance.yahoo.com/quote/' + stock_name + '?p=' + stock_name
	quote = web.DataReader(stock_name, data_source='yahoo', start=today, end=today)
	try:
	 url = urlopen(url)
	except:
	 print("Error opening the URL")
	soup = bs4.BeautifulSoup(url, "html.parser")
	name = soup.find_all('h1', {'class': 'D(ib)'})[0].text.strip()
	price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
	openPrice = round(quote['Open'].values[0], 2)
	return name, price, openPrice

