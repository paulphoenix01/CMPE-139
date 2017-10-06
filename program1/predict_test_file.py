from collections import Counter
import json,re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from pprint import pprint
from numpy import dot
from numpy.linalg import norm



#Set stop word in english and add punctations
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])


test_file = open('test.dat', 'r')
test_lines = test_file.read().splitlines()

positive_db = { }
negative_db = { } 

with open('negative_word_count.json') as infile:
	negative_db = json.load(infile)


with open('positive_word_count.json') as infile:
        positive_db = json.load(infile)


result = [ ] 

for review in test_lines:

	### Cleaning the review 
	theString = review
        #Remove words with < 3 item
        cleanString = re.sub(r'\b\w{1,3}\b', '', theString)
        #Remove unicode and dash
        cleanString = re.sub(r'[^\x00-\x7F]+','', cleanString)
        cleanString = re.sub(r'[-]+','',cleanString)
        list_of_words = [i.lower() for i in wordpunct_tokenize(cleanString) if i.lower() not in stop_words]
	
	### Getting prediction if Positive or Negative ### 
	positive_cos = 0
	negative_cos = 0 
			
	c = Counter(cleanString.split())
	counter_dict = dict(c)
	
	#Vector for Cosine similarity
	pos_vector = [ ]
	q_pos_vector = [ ]
	
	q_neg_vector = [ ] 
	neg_vector = [ ]

	# Finding vector
	for word in counter_dict:		
		if word in positive_db:
			pos_vector.append(positive_db[word])
			q_pos_vector.append(counter_dict[word])
		if word in negative_db:
			neg_vector.append(negative_db[word])
			q_neg_vector.append(counter_dict[word])
	
	# Calculating
	positive_cos = dot(q_pos_vector, pos_vector)/(norm(q_pos_vector)*norm(pos_vector))
	negative_cos = dot(q_neg_vector, neg_vector) / (norm(q_neg_vector) * norm(neg_vector))
	

	if positive_cos >= negative_cos:
		result.append("+1")
	elif negative_cos >  positive_cos:
		result.append("-1")
	else:
		result.append("+1")

with open('result.txt', 'w') as fp:
	for item in result:
		fp.write(item + '\n')

		
