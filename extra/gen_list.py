# generate image from csv word list
import sys
import pydot
import ConfigParser


def is_grandparent(parent, child_dict):
	for child in child_dict[parent]:
		if len(child_dict[child]) > 0:
			return True
	return False

def draw_node_recursive(parent, child_dict, config):
	config.set('TREE', parent, (" ".join(child_dict[parent]).lower()))
	for child in child_dict[parent]:
		if len(child_dict[child]) > 0:
			config.set('TREE', child, (" ".join(child_dict[child]).lower()))

filein = open(sys.argv[1], 'r')
filout = open(sys.argv[2], 'w')

child_dict = {}
phrase_list = []

config = ConfigParser.ConfigParser()
config.add_section("TREE")
line_count = 0
for line in filein:
	#if line_count > 10000:
	#	break
	csv_list = line.split(',')
	phrase = csv_list[0]
	if "[" in phrase or "]" in phrase or "-" in phrase:
		continue
	phrase_list.append(phrase.split('_'))
	line_count += 1

total = len(phrase_list)
count = 0

percen = 0
lastp = 0

for phrase_words in phrase_list:
	phrase = "_".join(phrase_words)
	count += 1
	lastp = percen
	percen = 100 * count / total
	if percen != lastp:
		print (str(100 * count / total) + "%")
	child_dict[phrase] = []
	for child_words in phrase_list:
		#if child_words != phrase_words and all(word in child_words for word in phrase_words):
		#	child_dict[phrase].append("_".join(child_words))
		if len(child_words) > len(phrase_words) and phrase_words == child_words[-1*len(phrase_words):]:
			child_dict[phrase].append("_".join(child_words))

for parent in child_dict:
	#if "=" not in parent and len(child_dict[parent]) > 1:
	#	config.set('TREE', parent.upper(), " ".join(child_dict[parent]))
	if "=" not in parent and is_grandparent(parent, child_dict):
		draw_node_recursive(parent, child_dict, config)
config.write(filout)
filout.close()
filein.close()