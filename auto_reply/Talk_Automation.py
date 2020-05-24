import bs4
import time
import requests
import collections
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from create_chatbot import create_chatbot

class Talk_Automation():
	def __init__(self, url, count, prev_message, time_not_response, max_people, set_robot=True):
		self.browser = webdriver.Chrome(executable_path=r'/usr/local/bin/chromedriver')
		self.browser.get(url)
		self.count = count
		self.max_people = max_people
		self.prev_message = prev_message
		self.dialog = collections.defaultdict(set)
		self.time_not_response = time_not_response
		self.set_robot = set_robot
		if self.set_robot:
			self.robot = create_chatbot('conversations') 
	
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
				print(str(self.count) + ' / ' + str(self.max_people))
			self.count += 1
			self.time_not_response = 0
			self.prev_message = []
		except:
			print("Checking status......")

	def check_respond(self, max_time):
		try: 
			content = self.browser.find_elements_by_css_selector('.message.user.other')
			last_content = content[-1].text.splitlines()[-1]
			isResponsed = False
			if len(self.prev_message) == 0:
				if last_content != '對方正在輸入...':
					self.prev_message.append(last_content)
				say_hi = self.browser.find_element_by_css_selector('.main-input')
				say_hi.send_keys('Hi')
				say_hi.send_keys(Keys.ENTER)
			elif last_content == self.prev_message[-1]:
				self.time_not_response += 1
				if self.time_not_response > 3:
					print("Not respoding for " + str(self.time_not_response*10) + " seconds")
			else:
				if last_content != '對方正在輸入...':
					self.prev_message.append(last_content)
					isResponsed = True
				self.time_not_response = 0
			if isResponsed and self.set_robot:
				print(self.prev_message)
				response_content = self.robot.get_response(self.prev_message[-1]).text
				response = self.browser.find_element_by_css_selector('.main-input')
				response.send_keys(response_content)
				response.send_keys(Keys.ENTER)
				print(response_content)
				self.dialog[self.prev_message[-1]].add(response)
				time.sleep(1)
		except:
			if len(self.prev_message) == 0:
				self.time_not_response += 1
				if self.time_not_response > 3:
					print("Not respoding for " + str(self.time_not_response*10) + " seconds")

		if self.time_not_response >= max_time * 60 // 10:
			print("Another person not respoding for " + str(self.time_not_response*10//60) + " mins.")
			print("Start finding new person......")
			print(str(self.count) + ' / ' + str(self.max_people))
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

	def check_comaand(self):
		try:
			content = self.browser.find_elements_by_css_selector('.message.user.me')[-1].text.splitlines()[-1]
			if content == 'CLOSE':
				self.close()
			elif content == 'STOP':
				self.set_robot = False
			elif content == 'CHANGE':
				try:
					self.browser.find_element_by_css_selector('.message.user.me').click()
					time.sleep(1)
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
		except:
			pass

	def pause(self):
		time.sleep(3)

	def close(self):
		print("Closing...")
		self.browser.quit()
		time.sleep(1)
		exit()