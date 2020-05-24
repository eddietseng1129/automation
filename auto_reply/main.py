import time
from Talk_Automation import Talk_Automation

url = r"https://knock.tw"
MAX_PEOPLE = int(input("How many people you want to meet? "))
MAX_TIME = int(input("How much time you're willing to wait when not responding (mins)? "))
START_MESSAGE = input("Enter your starting message: ")
NEED_ROBOT = input("Need Robot (True/False)? ")
MAX_ERROR = 5

if NEED_ROBOT.lower() in ['true', 'yes', 'y', 'yeah', 'yup', '1']:
	NEED_ROBOT = True
else:
	NEED_ROBOT = False

print("")
print("--------------------------------------------")
print("Number of people you want to meet: {}".format(MAX_PEOPLE))
print("Time you willing to wait for each person: {} min(s)".format(MAX_TIME))
print("Enable Robot: {}".format(str(NEED_ROBOT)))
print("--------------------------------------------")
print("Basic command")
print("CHANGE - find another person")
print("CLOSE - close the browser")
print("STOP - stop Robot")
print("--------------------------------------------")

print("Starting...")
people_count = 1
error_count = 1
prev_message = []
time_not_response = 0 
talk = Talk_Automation(url, people_count, prev_message, time_not_response, MAX_PEOPLE, set_robot=NEED_ROBOT)
time.sleep(5)


# Start Application
start = False
while not start:
	try:
		talk.start()
		start = True
	except:
		print("Starting Error!!")
		error_count += 1
		time.sleep(2)
		if error_count == MAX_ERROR:
			talk.close()
time.sleep(5)

# Setting name
insert_start = False
while not insert_start:
	try:
		talk.set_name(START_MESSAGE)
		insert_start = True
	except:
		print("Setting Starter Message Error!!")
		error_count += 1
		time.sleep(2*error_count)
		if error_count == MAX_ERROR:
			talk.close()

print("All set!")

while True:
	# Exit when meet MAX_PEOPLE
	if talk.count > MAX_PEOPLE:
		print("Reached maximun number: ", MAX_PEOPLE)
		talk.close()
	
	# If someone says goodbye
	talk.other_leave()

	time.sleep(5)

	# If someone isn't responding
	talk.check_respond(MAX_TIME)

	time.sleep(1)

	# Check command
	talk.check_comaand()

	# Check for edge cases
	try:
		talk.start()
	except:
		pass