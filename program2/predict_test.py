import pickle,math,operator

train_items = []
test_items = [ ] 
with open('train_buckets.json','rb') as infile:
        train_items = pickle.load(infile)

with open('test_buckets.json','rb') as infile:
	test_items = pickle.load(infile)

result = [ ] 

print train_items[0]

def find_euc_distance(vector1, vector2):
	dist = math.sqrt(sum([(a - b)**2 for a, b in zip(vector1, vector2)]))
	return dist


counter = 0
for test_item in test_items:
	print counter
	counter+=1

	euc_dist_list = [ ]

	for train_item in train_items:
		test_vector = test_item['data_buckets_count']
		train_vector = train_item['data_buckets_count']

		euc_dist = find_euc_distance(test_vector, train_vector)
 		euc_dist_list.append((euc_dist, train_item['label']))
	
	euc_dist_list.sort(key=operator.itemgetter(0))
	
	active = 0
	inactive = 0 

	for neighbor in euc_dist_list[:50]:
		if neighbor[1] == '0':
			inactive += 1
		elif neighbor[1] == '1':
			active += 1
	
	if active > inactive * 4:
		result.append('1')

	else:
		result.append('0')

	print "Count: %s, Result: %s, Pos #: %s, Neg #: %s" %(counter, result[counter-1],active, inactive)


with open('result.txt', 'w') as fp:
	for item in result:
		fp.write(item + '\n')

