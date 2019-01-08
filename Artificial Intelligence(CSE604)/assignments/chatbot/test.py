import sys,nltk
from nltk.tokenize import word_tokenize
sentence = "hello world?"
word = word_tokenize(sentence)
tagged = nltk.pos_tag(word)
for item in tagged:
	print(item)
'''	
your_string = "hello , world?"
new_str = re.sub(r'\W+', '', your_string)
print(new_str)
'''