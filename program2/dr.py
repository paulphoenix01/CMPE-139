import pickle
from sklearn.tree import DecisionTreeClassifier


train_items = []
test_items = []
with open('train_parsed.json','rb') as infile:
	train_items = pickle.load(infile)

#test_file = open('test.dat', 'r')
#test_items = test_file.read().splitlines()

train_buckets = []
test_buckets = [] 


counter = 0

#Adding into a double array
for item in train_items:
	print "train",counter
	counter+=1
	dataset = item['data'].split(" ")

	buckets = get_buckets(dataset)

	new_json = {
		'label': item['label'],
		'data_buckets_count': buckets	
	}
	train_buckets.append(new_json)

with open('train_buckets.json','wb') as outfile:
	pickle.dump(train_buckets, outfile)

with open('test_buckets.json', 'wb') as outfile:
	pickle.dump(test_buckets, outfile)
#print train_buckets[0]
#print len(train_buckets[0]['data_buckets_count'])
