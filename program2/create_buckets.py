import pickle

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
	buckets.append(0)
	index = 0

	for data in dataset[:-1]:
		data = int(data)
		start = index*100
		end = (index+1) * 100

		if data >= start and data < end:
			buckets[index] += 1
		if data >= end:
			index+=1
			buckets.append(0)

	return buckets

for item in test_items:
	dataset = item.split(" ")
	#print dataset	
	buckets = get_buckets(dataset)
	
	new_json = {
		'label': '-1',
		'data_buckets_count': buckets
	}
	test_buckets.append(new_json)

for item in train_items:
#	print item
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
