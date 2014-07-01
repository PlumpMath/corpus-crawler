import ConfigParser
import sys
from nltk.corpus import wordnet as wn

parser = ConfigParser.ConfigParser()
parser.optionxform=str
fileout_name = sys.argv[1]
fileout = open(fileout_name, "w")
parser.add_section("TREE")
entity = wn.synset('entity.n.01')
en_child = ""
for node in entity.hyponyms():
	en_child += node.name + " "
	node_child = ""
	for anode in node.hyponyms():
		node_child += anode.name + " "
	parser.set("TREE", node.name, node_child)
parser.set("TREE", entity.name, en_child)
parser.write(fileout)
fileout.close()