import os, sys,nltk
from flask import Flask, request
from pymessenger import Bot
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAQK7iKhrlkBAGRpsEFFpC1nPNQTXHZAs7gNBIbWW82N3o8u6naEUv6EhBMBCg73Nz7BVRkklgMrbvyhpcHZBe4r3AVgZCAgBMfbJlGXXStWqIjNn5pChO5jlp1GVGs3vh30xg3ZAe71TSGBjzqELIVQbz9TgYPn6yKHqdX8P1Q68eOZA2jLT"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

def appenTo_file(message):
	with open("learn.txt", "a") as myfile:
		myfile.write(message+"\n")

def get_answer(number):
	with open("reply.txt", "r") as file:
		lines = file.readlines()
		return lines[number].split("|")[1]

def process(message):
	topic_found = False
	matchedKey = "None"
	message = message.lower()
	words = word_tokenize(message)
	tagged_words = nltk.pos_tag(words)
	for word in words:
		words[words.index(word)] = WordNetLemmatizer().lemmatize(word,'v')
	print("after lemmatizing")
	print(words)
	#words = message.split()
	with open("similar_words.txt", "r") as file:
    		for line in file:
	    			similar_words = line.split("|")[0]
		    		base_word = line.split("|")[1]
		    		similar_splited_words = similar_words.split(",")
		    		print(similar_words)
		    		print(base_word)
		    		for word in words:
		    			if word in similar_splited_words:
		    				words[words.index(word)] = similar_splited_words[0]
		    		print("after replace:")
		    		print(words)
	with open("questions.txt", "r") as file1:

		for line in file1:
			print("\n\n")
			keywords = line.split("|")[0].split(",")
			print("keywords")
			print(keywords)
			mainKeywords = line.split("|")[1].split(",")
			print("main keywords")
			print(mainKeywords)
			precision = float(line.split("|")[2].split(",")[0])
			print("precision:")
			print(precision)
			answer = line.split("|")[3]
			print("answer:"+answer)
			matching_with_keywords = len(list(set(keywords).intersection(words)))
			print("common")
			print(matching_with_keywords)
			calculated_precision = matching_with_keywords/len(keywords)
			print("calculated_precision:")
			print(calculated_precision)
			print("contains")
			print(words)
			print(mainKeywords)
			isContainMainKeywords = all(elem in words for elem in mainKeywords)
			print(isContainMainKeywords)
			if isContainMainKeywords:
				topic_found = True
				matchedKey = mainKeywords[0]
			if isContainMainKeywords and (calculated_precision >= precision):
				print("found answer:"+answer)
				return get_answer(int(answer)-1)
	appenTo_file(message)
	if topic_found:
		return "you are telling something about "+matchedKey+".But I am not clear."
	return "I don't know. But I will learn about this soon"


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
						messaging_text = 'I do not know non-text messages'

					# Echo
					response = process(messaging_text)
					bot.send_text_message(sender_id, response)

	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)