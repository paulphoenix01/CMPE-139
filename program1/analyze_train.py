from collections import Counter
import pickle, re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from pprint import pprint

#Set stop word in english and add punctations
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) 

def getTrainList():
        with open('train_json.txt','rb') as infile:
                list = pickle.load(infile)
                return list

positive_counter_db = { }
negative_counter_db = { } 
list = getTrainList()

for item in list:
	theString = item['review']
	#Remove words with < 3 item
	cleanString = re.sub(r'\b\w{1,3}\b', '', theString)
	#Remove unicode and dash
	cleanString = re.sub(r'[^\x00-\x7F]+','', cleanString)
	cleanString = re.sub(r'[-]+','',cleanString)
	list_of_words = [i.lower() for i in wordpunct_tokenize(cleanString) if i.lower() not in stop_words]
	c = Counter(cleanString.split())

	counter_dict = dict(c.most_common(100))

	for word in counter_dict.keys():
		if word not in list_of_words:
			counter_dict.pop(word)
		

	for word in counter_dict:
		if item['rate'] == '+1':
			positive_counter_db[word] = positive_counter_db.get(word, 0) + counter_dict[word]
		elif item['rate'] == '-1':
			negative_counter_db[word] = negative_counter_db.get(word, 0) + counter_dict[word]
	#print counter_dict


positive_counter_db =  positive_counter_db.items()
positive_counter_db = sorted(positive_counter_db, key=lambda x: x[1],  reverse=True)


negative_counter_db =  negative_counter_db.items()
negative_counter_db = sorted(negative_counter_db, key=lambda x: x[1],  reverse=True)

print "The POSITIVE ( +++ ) COUNTER DATABASE has : %d items" % (len(positive_counter_db))
print positive_counter_db[:100]

print "The NEGATIVE ( --- ) COUNTER DATABASE has : %d items" % (len(negative_counter_db))
print positive_counter_db[:100]
