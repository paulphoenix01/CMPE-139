#Author: Linh Phan
from collections import Counter
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import random_projection
import random


#Open Train.dat file and put as list
train_file = open('train.dat', 'r')
test_file = open('test.dat', 'r')

train_items = train_file.read().splitlines()
test_items = test_file.read().splitlines()

active = []
inactive = []
label = [ ]
values = []

# Start Parsing for each lines in the file
for item in train_items:
	item = item.split("\t")
	
	data = item[1].split(" ")
	data = [int(k) for k in data[:-1]]
	
	if int(item[0]) == 0:
		inactive.append(data)
	else:
	#Make active data have same amount as inactive data
		counter = 0
		while (counter<8):
			label.append(int(item[0]))
			values.append(data)
			active.append(data)
			counter+=1
		active.append(data)

	label.append(int(item[0]))
	values.append(data)


indptr = [0]
indices = [ ]
data = [ ]
attributes = { }

for d in values:
    for elem in d:
        index = attributes.setdefault(elem, len(attributes))
        indices.append(index)
        data.append(1)
        indptr.append(len(indices))

print len(inactive)
print len(active)

train_csr = csr_matrix((data, indices, indptr)).toarray()



# Split the train data for testing with 80/20
X_train, X_test, y_train, y_test = train_test_split(final_train, label, test_size=0.3, random_state=42)

svd = TruncatedSVD(n_components=150)
svd.fit(X_train)


X_train_svd = svd.transform(X_train)
X_test_svd = svd.transform(X_test)

start = time.time()
clf.fit(X_train_svd, y_train)
y = clf.predict(X_test_svd)

errors = (y_test != y).sum()
total = X_test_svd.shape[0]
error_rate_with_svd = (errors/float(total)) * 100
print "Error rate with SVD: %d/%d * 100 = %f" % (errors, total, error_rate_with_svd)

end = time.time()
duration_with_svd = end-start
print "Time taken to train a KNN Classifier with SVD: %d seconds" %duration_with_svd


rp = random_projection.SparseRandomProjection(n_components=150, random_state=19)
rp.fit(X_train)

X_train_rp = rp.transform(X_train)
X_test_rp = rp.transform(X_test)

clf.fit(X_train_rp, y_train)
y = clf.predict(X_test_rp)

errors = (y_test != y).sum()
total = X_test_rp.shape[0]
error_rate_with_rp = (errors/float(total)) * 100
print "Random Projection error rate: %d/%d * 100 = %f" % (errors, total, error_rate_with_rp)

#Parse good train file as json
train_json_list = [ ] 
for x, y in X_train_xvd. y_train_svd:
	train_item = { 
		'label' : y,
		'data' : x
	}
	train_json_list.append(train_item)
	
#Write to file
with open('train_list.json', 'wb') as file:
	pickle.dump(train_json_list, file)

#Write test file to JSON for easy parsing
test_json_list = []
for item in test_items:
	dataset = item.split(" ")
	new_json = {
		'label': '-1',
		'data': dataset
	}
	test_json_list.append(new_json)

with open('test_list.json', 'wb') as file:
	pickle.dump(test_json_list, file)

# Opening file
#def getTrainList():
#	with open('train_parsed.json','rb') as infile:
#		list = pickle.load(infile)
#		return list
	#print list[:2]

