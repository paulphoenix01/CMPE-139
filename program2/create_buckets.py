import pickle
from sklearn.tree import DecisionTreeClassifier


train_items = []
test_items = []
with open('train_parsed.json','rb') as infile:
	train_items = pickle.load(infile)

test_file = open('test.dat', 'r')
test_items = test_file.read().splitlines()

train_buckets = []
test_buckets = [] 

def get_buckets(dataset):
	buckets = [ ]
	bucket_size = 20
	buckets.append(0)

	index = 0
	start = index * bucket_size
	end = (index+1) * bucket_size	
		
	while(end<=100000):
		for data in dataset[:-1]:
			data = int(data)
			if data < end and data >= start:
				buckets[index] += 1
	
		
		buckets.append(0)
		index+=1
		start = index * bucket_size
		end = (index+1)*bucket_size
		

	return buckets

counter = 0
for item in test_items:
	print "test", counter
	counter += 1
	dataset = item.split(" ")
	#print dataset	
	buckets = get_buckets(dataset)
	
	new_json = {
		'label': '-1',
		'data_buckets_count': buckets
	}
	test_buckets.append(new_json)

counter = 0
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
