#Author Linh Phan

from collections import Counter
import pickle, re, json
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from pprint import pprint

#Set stop word in english and add punctations
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) 

#List of negative word and positive word from Lexicon study
neg_list = []
pos_list = []

def getTrainList():
        with open('train_json.txt','rb') as infile:
                list = pickle.load(infile)
                return list


with open('lexicon_negative.txt') as f:
    neg_list = f.read().splitlines()

with open('lexicon_positive.txt') as f:
    pos_list = f.read().splitlines()


#Json file that store word count or positive and negative reviews
positive_counter_db = { }
negative_counter_db = { } 
list = getTrainList()

#Train.dat wordcount for each review
train_wc = [ ]

# Traverse thru list
counter = 0
for item in list:
	counter += 1
	print counter

	theString = item['review']
	#Remove noise words with < 3 item
	cleanString = re.sub(r'\b\w{1,3}\b', '', theString)
	#Remove unicode and dash
	cleanString = re.sub(r'[^\x00-\x7F]+','', cleanString)
	cleanString = re.sub(r'[-]+','',cleanString)
	cleanString = re.sub('[^a-zA-Z ]+', '', cleanString)
	
	#List of words that are not noise
	list_of_words = [i.lower() for i in wordpunct_tokenize(cleanString) if i.lower() not in stop_words]
	
	c = Counter(cleanString.split())
	
	#Sort list by most_common and return as dict
	counter_dict = dict(c.most_common())

	#Remove items that are not actual word
	for word in counter_dict.keys():
		if word not in list_of_words:
			counter_dict.pop(word)
	
		
	review = {
		'rate': item['rate'],
		'word_count': counter_dict
	}	

	train_wc.append(review)

with open('train_word_count.json','w') as outfile:
	json.dump(train_wc,outfile)


#print negative_counter_db[:100]

#print "The POSITIVE ( +++ ) COUNTER DATABASE has : %d items" % (len(positive_counter_db))
#print dict(positive_counter_db[:3000])

#print "The NEGATIVE ( --- ) COUNTER DATABASE has : %d items" % (len(negative_counter_db))
#print dict(negative_counter_db[:100])
