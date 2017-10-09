from collections import Counter
import pickle, re, json
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from pprint import pprint

#Set stop word in english and add punctations
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) 

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


positive_counter_db = { }
negative_counter_db = { } 
list = getTrainList()

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

	counter_dict = dict(c.most_common())

	for word in counter_dict.keys():
		if word not in list_of_words:
			counter_dict.pop(word)
		

	for word in counter_dict:
		if item['rate'] == '+1' and word in pos_list:
			positive_counter_db[word] = positive_counter_db[word] + 1 if word in positive_counter_db else 1
		elif item['rate'] == '-1' and word in neg_list:
			negative_counter_db[word] = negative_counter_db[word] + 1 if word in negative_counter_db else 1
	#print counter_dict

# Remove most 3 common and 3 least common words
for i in range(3):
	del positive_counter_db[max(positive_counter_db, key=positive_counter_db.get)]
	del negative_counter_db[max(negative_counter_db, key=negative_counter_db.get)]

for item in positive_counter_db.keys():
	if positive_counter_db[item] <= 3:
		positive_counter_db.pop(item)

for item in negative_counter_db.keys():
	if negative_counter_db[item] <= 3:
		negative_counter_db.pop(item)


## Sorted as tuple
positive_counter_db =  positive_counter_db.items()
positive_counter_db = sorted(positive_counter_db, key=lambda x: x[1],  reverse=True)


negative_counter_db =  negative_counter_db.items()
negative_counter_db = sorted(negative_counter_db, key=lambda x: x[1],  reverse=True)

## Write to file as JSON
with open('positive_word_count.json','w') as outfile:
	json.dump(dict(positive_counter_db),outfile)

with open('negative_word_count.json','w') as outfile:
	json.dump(dict(negative_counter_db), outfile)

#print negative_counter_db[:100]

#print "The POSITIVE ( +++ ) COUNTER DATABASE has : %d items" % (len(positive_counter_db))
print dict(positive_counter_db[:3000])

#print "The NEGATIVE ( --- ) COUNTER DATABASE has : %d items" % (len(negative_counter_db))
#print dict(negative_counter_db[:100])
