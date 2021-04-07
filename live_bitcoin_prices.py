import requests
import json
from datetime import datetime, timedelta
import sys

file_path = sys.argv[1]
raw_data=requests.get('https://api.coinranking.com/v1/public/coin/1/history/30d')
raw_data_json=raw_data.json()

coinranking_data=raw_data_json["data"]["history"]

bitcoin_prices={}
result_list=[]

for obj in coinranking_data:
	date=datetime.fromtimestamp(obj["timestamp"]/1000).strftime('%d-%m-%yT%H:%M:%S')
	time=datetime.fromtimestamp(obj["timestamp"]/1000).strftime('%H:%M:%S')
	if time=='00:00:00':
		bitcoin_prices[date]=obj

mx = 0
mn = 0

for current_date in bitcoin_prices.keys():
		
	current_price=float(bitcoin_prices[current_date]["price"])

	obj = bitcoin_prices[current_date]
	d = datetime.fromtimestamp(obj["timestamp"]/1000) - timedelta(days=1)	
	previous_date=d.strftime('%d-%m-%yT%H:%M:%S')
	day_of_week=datetime.fromtimestamp(obj["timestamp"]/1000).strftime("%A")

	if previous_date in bitcoin_prices:
		previous_price=float(bitcoin_prices[previous_date]["price"])
		mx = max(previous_price, mx)
		mn = min(previous_price, mn)

		high_since_start = False
		low_since_start = False

		if current_price > mx:
			high_since_start = True

		if current_price < mn:
			low_since_start = True

		direction_of_price=""
		
		if current_price>previous_price:
			direction_of_price="up"
		elif current_price<previous_price:
			direction_of_price="down"
		else:
			direction_of_price="same"

		change_in_price=current_price-previous_price
		

		result={"date":current_date, "price":current_price,"direction":direction_of_price,
				"change":abs(change_in_price),"dayOfWeek":day_of_week,
				"highSinceStart":high_since_start,"lowSinceStart":low_since_start}
		result_list.append(result)

	else:
		result={"date":current_date,"price":current_price,"direction":"na","change":"na",
				"dayOfWeek":day_of_week}
		result_list.append(result)

with open('output.json', 'w', encoding='utf-8') as f:
	json.dump(result_list, f, ensure_ascii=False, indent=4)




			

	
	

	
	
	

	

		
		















