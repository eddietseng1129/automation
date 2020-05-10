import requests

"""
Create your own token from: https://notify-bot.line.me/en/
Save it to token.txt or just set token variable to the string value
"""
token = open("token.txt", "r").read()

# LINE PUSH
def lineNotifyMessage(token, msg):
	headers = {
	"Authorization": "Bearer " + token, 
	"Content-Type" : "application/x-www-form-urlencoded"
	}

	payload = {'message': msg}
	r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
	return r.status_code
