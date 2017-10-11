from collections import Counter
import json,re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from pprint import pprint
from numpy import dot
from numpy.linalg import norm
import math, operator


#Set stop word in english and add punctations
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])

#Open Test.dat file
test_file = open('test.dat', 'r')
test_lines = test_file.read().splitlines()

#Get the positive negative word count database from analyze_train.py
train_db = [ ] 



with open('train_word_count.json') as infile:
        train_db = json.load(infile)


result = [ ] 

#Find euclidean distance
def find_euc_distance(vector1, vector2):
	dist = math.sqrt(sum([(a - b)**2 for a, b in zip(vector1, vector2)]))
	return dist

#Traverse thru the test.dat review list
counter = 0
for review in test_lines[0:2000]:
	counter += 1
	#print counter
	
	### Cleaning the review 
	theString = review
        #Remove words with < 3 item
        cleanString = re.sub(r'\b\w{1,3}\b', '', theString)
        #Remove unicode and dash
        cleanString = re.sub(r'[^\x00-\x7F]+','', cleanString)
        cleanString = re.sub(r'[-]+','',cleanString)
        list_of_words = [i.lower() for i in wordpunct_tokenize(cleanString) if i.lower() not in stop_words]
	
			
	c = Counter(cleanString.split())
	counter_dict = dict(c)
	
	euc_dist_list = [ ]
		
	for train_item in train_db:
		train_word_count = train_item['word_count']
		
		#Current Item vector
		train_vector = [ ]
		test_vector = [ ]
		
		#Traverse to get word frequency count as vector. Zero if not in the list
		for word in counter_dict:
			if word in train_word_count:
				train_vector.append(train_word_count[word])	
				test_vector.append(counter_dict[word])
			elif word not in train_word_count:
				train_vector.append(0)
				test_vector.append(counter_dict[word])

		for word in train_word_count:
			if word not in counter_dict:
				train_vector.append(train_word_count[word])
				test_vector.append(0)

		
		euc_dist = find_euc_distance(test_vector, train_vector)
 		euc_dist_list.append((euc_dist, train_item['rate']))
		#if train_item['rate'] == "-1":
		#	print "-1" 		
	euc_dist_list.sort(key=operator.itemgetter(0))

	pos = 0
	neg = 0
	for neighbor in euc_dist_list[:100]:
		if neighbor[1] == "+1":
			pos += 1
		elif neighbor[1] == "-1":
			neg += 1

	if pos >= neg:
		result.append("+1")
	elif pos < neg:
		result.append("-1")	
		
	
	print "Count: %s, Result: %s, Pos #: %s, Neg #: %s" %(counter, result[counter-1],pos, neg)
	

#Write the predict as result
with open('result0-1999.txt', 'w') as fp:
	for item in result:
		fp.write(item + '\n')

		
