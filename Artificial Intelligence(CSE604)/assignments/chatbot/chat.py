

def process(message):
	topic_found = False
	matchedKey = "None"
	message = message.lower()
	words = message.split()
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
				return answer
	if topic_found:
		return "you are telling something about "+matchedKey+".But I am not clear."
	return "I don't know. But I will learn about this soon"

text = input()
while text != "bye":	
	reply = process(text)
	print(reply)
	text = input()
