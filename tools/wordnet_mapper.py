from nltk.corpus import wordnet as wn
import ConfigParser
import sys

fileinpath = sys.argv[1]
fileoutpath = sys.argv[2]

filein = open(fileinpath, "r")

wordlistraw = filein.read()
wordlist = wordlistraw.split(',')

wordclosure = {}
wordchildren = {}

hyper = lambda s : s.hypernyms()

for word in wordlist:
	#add to word dict
	#find closure of hypernyms
	try:
		word_sense = wn.synsets(word)[0]
	except IndexError:
		continue
	wordvalue = word_sense.name
	wordclosure[wordvalue] = [node.name for node in list(word_sense.closure(hyper))]
	wordchildren[wordvalue] = []

for node in wordclosure:
	for potential_parent in wordclosure:
		if node != potential_parent:
			if potential_parent in wordclosure[node]:
				#potential_parent is a parent of node
				wordchildren[potential_parent].append(node)

fileout = open(fileoutpath, "w")
parser = ConfigParser.ConfigParser()
parser.optionxform=str
parser.add_section("TREE")
for parent in wordchildren:
	parser.set("TREE", parent, " ".join(wordchildren[parent]))

parser.write(fileout)
fileout.close()