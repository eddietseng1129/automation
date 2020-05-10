# LINE push notification for stock price

import os
import time
import stock_scrapper
import line_notify as ln
import pandas as pd
from datetime import datetime

# save stock price
# if not os.path.exists(csv_path):
# 	stock_price = {'Name': ['MSFT', 'DIS', 'TSM', 'TWTR', 'XOP', 'T'], 
# 				   'Price': [175.00, 105.82, 54.00, 33.50, 55.42, 30.00],
# 				   'Shares': [1, 1, 2, 1, 4, 1]}
# 	df = pd.DataFrame(stock_price, columns= ['Name', 'Price', 'Shares'])
# 	df.to_csv(csv_path, index = False, header=True)
# else:
# 	df = pd.read_csv(csv_path)

###### Please create your own stock information ######
csv_path = r'stock_data.csv'

df = pd.read_csv(csv_path)
stocks = df['Name'].values

UPPER = 5
LOWER = -5
	
###### main ######
while True:
	print(datetime.now())
	for stock in stocks:
		name, price, openPrice = stock_scrapper.parsePrice(stock)
		share = df.loc[df['Name'] == stock, 'Shares'].values[0]
		cost = round(float(df.loc[df['Name'] == stock, 'Price'].values[0]), 2)
		diff = round(float(price) - cost, 2)
		today_diff = round(float(price) - float(openPrice), 2)
		percent = round(diff / cost * 100, 2)
		today_percent = round(today_diff / openPrice * 100, 2)
		# Today's open price
		# If it is up for UPPER percent or down for LOWER percnt
		if today_percent >= UPPER or today_percent <= LOWER:
			message = ('\n' + str(name) + "\n Today's Opening Price: " + str(openPrice) + 
					   "\n Current Price: " + str(price) + "\n Difference: " + str(today_diff) + 
					   ' (' + str(today_percent) + '%)' + "\n Shares: " + str(share) +
					   "\n Cost: " + str(cost) + "\n Return: " + str(diff * share) + 
					   ' (' + str(percent) + '%)')
			print('Sending ' + str(name) + ' information...')
			ln.lineNotifyMessage(token, message)
		
		###### Comparing for total return ######
		# Total Returns
		# if percent >= UPPER: # or percent <= LOWER:
		# 	message = ('\n' + str(name) + "\n Shares: " + str(share) + 
		# 			   "\n Cost: " + str(cost) + "\n Current Value: " + str(price) + 
		# 			   "\n Return: " + str(diff * share) + ' (' + str(percent) + '%)')
		# 	print('Sending ' + str(name) + ' information...')
		# 	ln.lineNotifyMessage(token, message)
		
	# run every 60 sec
	time.sleep(60)
