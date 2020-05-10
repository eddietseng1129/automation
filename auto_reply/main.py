import time
from Talk_Automation import Talk_Automation

url = r"https://knock.tw"
MAX_PEOPLE = int(input("How many people you want to meet? "))
MAX_TIME = int(input("How much time you're willing to wait when not responding (mins)? "))
START_MESSAGE = input("Enter your starting message: ")

print("Starting...")
count = 1
prev_message = []
time_not_response = 0
talk = Talk_Automation(url, count, prev_message, time_not_response)
time.sleep(5)

# Start Application
try:
	talk.start()
except:
	print("Starting Error!!")
	talk.close()
time.sleep(5)

# Setting name
try:
	talk.set_name(START_MESSAGE)
except:
	print("Setting Starter Message Error!!")
	talk.close()

print("All set!")

while True:
	# Exit when meet MAX_PEOPLE
	if talk.count > MAX_PEOPLE:
		print("Reached maximun number: ", MAX_PEOPLE)
		talk.close()
	
	# If someone says goodbye
	talk.other_leave()

	time.sleep(10)

	# If someone isn't responding
	talk.check_respond(MAX_TIME)

	# Check for edge cases
	try:
		talk.start()
	except:
		pass
