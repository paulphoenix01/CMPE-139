#Author: Linh Phan

import pickle,io
from bs4 import BeautifulSoup

#Open Train.dat file and put as list
train_file = open('train.dat', 'r')
train_lines = train_file.read().splitlines()

train_json_list = []

# Start Parsing for each lines in the file
for line in train_lines:
	# File is format as: Rate \t Review => Split into rate and review
	the_line = line.split("\t")
	rate = the_line[0]

	# Clean raw review with html and backslash
	review = the_line[1]
	review = BeautifulSoup(review).text
	review = review.replace("\\", "")

	# Put into json file
	train_json = {
		'review' : review,
		'rate' : rate
	}
	
	# Add to list
	train_json_list.append(train_json)

#Write to file
with open('train_json.txt', 'wb') as file:
	pickle.dump(train_json_list, file)

# Opening file
def getTrainList():
	with open('train_json.txt','rb') as infile:
		list = pickle.load(infile)
		return list
	#print list[:2]

