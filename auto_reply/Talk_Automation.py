import bs4
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
from selenium.webdriver.common.keys import Keys

class Talk_Automation():
	def __init__(self, url, count, prev_message, time_not_response):
		self.browser = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver')
		self.browser.get(url)
		self.count = count
		self.prev_message = prev_message
		self.time_not_response = time_not_response
	
	def start(self):
		self.browser.find_element_by_css_selector('.start').click()

	def set_name(self, start_message):
		self.browser.find_element_by_css_selector('.tool-button.normal-tool-button.show-command').click()
		self.pause()
		self.browser.find_element_by_css_selector('.command-name').click()
		self.pause()
		inputElement = self.browser.find_element_by_xpath('//input[@type="text"]')
		inputElement.send_keys(start_message)
		inputElement.send_keys(Keys.ENTER)

	def other_leave(self):
		try:
			someone_leave = self.browser.find_element_by_css_selector('.message.alert')
			if someone_leave.find_element_by_css_selector('.message-content').text == '對話已結束，請點我重新配對聊天':
				someone_leave.find_element_by_css_selector('.message-content').click()
				print("She/He just leave, finding new one......")
				print(self.count)
			self.count += 1
			self.time_not_response = 0
			self.prev_message = []
		except:
			print("Checking status......")

	def check_respond(self, max_time):
		try: 
			content = self.browser.find_elements_by_css_selector('.message.user.other')
			if len(self.prev_message) == 0:
				self.prev_message.append(content[-1].text)
			elif content[-1].text == self.prev_message[-1]:
				self.time_not_response += 1
				if self.time_not_response > 3:
					print("Not respoding for " + str(self.time_not_response*10) + " seconds")
			else:
				self.prev_message.append(content[-1].text)
				self.time_not_response = 0
		except:
			if len(self.prev_message) == 0:
				self.time_not_response += 1
				if self.time_not_response > 3:
					print("Not respoding for " + str(self.time_not_response*10) + " seconds")

		if self.time_not_response >= max_time * 60 // 10:
			print("Another person not respoding for " + str(self.time_not_response*10//60) + " mins.")
			print("Start finding new person......")
			try:
				self.browser.find_element_by_css_selector('.tool-button.leave-chat').click()
				self.pause()
				self.browser.find_element_by_css_selector('.modal-default-button.confirm').click()
				self.pause()
				self.start()
			except:
				self.start()
			self.time_not_response = 0
			self.prev_message = []
			self.count += 1

	def pause(self):
		time.sleep(3)

	def close(self):
		print("Closing...")
		self.browser.quit()
		exit()