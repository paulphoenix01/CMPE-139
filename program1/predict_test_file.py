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

#Open Test.dat file
test_file = open('test.dat', 'r')
test_lines = test_file.read().splitlines()

#Get the positive negative word count database from analyze_train.py
positive_db = { }
negative_db = { } 

with open('negative_word_count.json') as infile:
	negative_db = json.load(infile)


with open('positive_word_count.json') as infile:
        positive_db = json.load(infile)


result = [ ] 

#Function for finding cosine similarity
def find_cos_sim(q,p):
	result = dot(q,p) / (norm(q) * norm(p))
	return result

#Traverse thru the test.dat review list
counter = 0
for review in test_lines:
	counter += 1
	print counter
	
	### Cleaning the review 
	theString = review
        #Remove words with < 3 item
        cleanString = re.sub(r'\b\w{1,3}\b', '', theString)
        #Remove unicode and dash
        cleanString = re.sub(r'[^\x00-\x7F]+','', cleanString)
        cleanString = re.sub(r'[-]+','',cleanString)
        list_of_words = [i.lower() for i in wordpunct_tokenize(cleanString) if i.lower() not in stop_words]
	
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
		else:
			pos_vector.append(0)
			q_pos_vector.append(counter_dict[word])

		if word in negative_db:
			neg_vector.append(negative_db[word])
			q_neg_vector.append(counter_dict[word])
		else:
			neg_vector.append(0)
			q_neg_vector.append(counter_dict[word])

	for word in positive_db:
		if word not in counter_dict:
			pos_vector.append(positive_db[word])
			q_pos_vector.append(0)

	for word in negative_db:
		if word not in counter_dict:
			neg_vector.append(negative_db[word])
			q_neg_vector.append(0)

	
	# Calculating
	positive_cos = find_cos_sim(pos_vector, q_pos_vector)
	negative_cos = find_cos_sim(neg_vector, q_neg_vector)
	
	#Make predict on the positive/negative 
	if positive_cos >= negative_cos:
		result.append("+1")
	elif negative_cos >  positive_cos:
		result.append("-1")
	else:
		result.append("+1")

#Write the predict as result
with open('result.txt', 'w') as fp:
	for item in result:
		fp.write(item + '\n')

		
