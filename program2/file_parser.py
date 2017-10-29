#Author: Linh Phan

import pickle,io
import random
#Open Train.dat file and put as list
train_file = open('train.dat', 'r')
train_lines = train_file.read().splitlines()

train_json_list = []

# Start Parsing for each lines in the file
for line in train_lines:
	# File is format as: Rate \t Review => Split into rate and review
	the_line = line.split("\t")
	label = the_line[0]

	# Clean raw review with html and backslash
	data = the_line[1]
	#review = BeautifulSoup(review).text
	data = data.replace("\\", "")
	
	# Put into json file
	train_json = {
		'label' : label,
		'data' : data
	}
	if label == "1":
		counter = 0
		while counter < 9:
			train_json_list.append(train_json)
			counter+=1
	# Add to list
	train_json_list.append(train_json)


random.shuffle(train_json_list)
print len(train_json_list)
#Write to file
with open('train_parsed.json', 'wb') as file:
	pickle.dump(train_json_list, file)

# Opening file
#def getTrainList():
#	with open('train_parsed.json','rb') as infile:
#		list = pickle.load(infile)
#		return list
	#print list[:2]

