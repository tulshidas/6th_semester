import os, sys
from flask import Flask, request
#from pymessenger import Bot

app = Flask(__name__)

# PAGE_ACCESS_TOKEN = "EAAQK7iKhrlkBAGRpsEFFpC1nPNQTXHZAs7gNBIbWW82N3o8u6naEUv6EhBMBCg73Nz7BVRkklgMrbvyhpcHZBe4r3AVgZCAgBMfbJlGXXStWqIjNn5pChO5jlp1GVGs3vh30xg3ZAe71TSGBjzqELIVQbz9TgYPn6yKHqdX8P1Q68eOZA2jLT"

# bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

'''
@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					# Echo
					response = messaging_text
					bot.send_text_message(sender_id, response)

	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()
'''

if __name__ == "__main__":
	app.run(debug = True, port = 81)