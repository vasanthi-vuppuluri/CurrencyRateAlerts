import urllib
import xml.etree.ElementTree as ET
import time

class Parser:
	"""Class for obtaining XML data from URL and parse it into dictionary"""

	def __init__(self, url):
		self.rate_map = {}
		self.url = url
		self.rates_data = None
	
	def request(self):
		response = urllib.urlopen(self.url)
		self.rates_data = ET.parse(response)

	def parse(self):
		root = self.rates_data.getroot()
		for child in root:
			self.rate_map[child.get("Symbol")] = [child.find('Bid').text, child.find('Direction').text]
        
	def get_rate_map(self):
		return self.rate_map


class RateAlert:
	"""Class for creating Alert Type Object stored here"""
	def __init__(self, symbol, target_rate, is_done = False):
		self.symbol = symbol
		self.target_rate = target_rate
		self.is_done = False

class CurrencyRateAlerts:
 	"""Class for processing all other Objects"""
 	def __init__(self, url):
 		self.alert_list = []
 		self.url = url

 	def validate_symbol(self, symbol):
 		symbol_data = Parser(self.url)
 		symbol_data.request()
 		symbol_data.parse()
 		return symbol in symbol_data.get_rate_map().keys()

 	def get_user_input(self):
 		while True: 		
 			symbol = raw_input("Enter the Symbol: ")
 			if self.validate_symbol(symbol) == True:
 				break
 		target_rate = raw_input("Enter the Target Rate: ")
 		self.alert_list.append(RateAlert(symbol, target_rate))

 	def send_alert(self, symbol):
 		print "Your Target value for ",symbol," is reached"


 	def check_alerts(self):
 		alert_check = Parser(self.url)
 		alert_check.request()
 		alert_check.parse()
 		data_list = alert_check.get_rate_map()
 		for alert in self.alert_list:
 			if(alert.is_done == False):
 				if(alert.target_rate <= data_list[alert.symbol][0]):
 					self.send_alert(alert.symbol)
 					self.alert_list.remove(alert)


cra_object = CurrencyRateAlerts("http://rates.fxcm.com/RatesXML")

while True:
 	cra_object.get_user_input()
 	yn = raw_input("Do you want to enter more? (Y|N)") 
 	if yn == 'n' or yn =='N' :
 		break

while True:
	cra_object.check_alerts()
	if len(cra_object.alert_list) == 0:
		break
	time.sleep(10)
