from nltk.chunk.regexp import RegexpParser
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import nltk.tag
from nltk.corpus import brown

while True:
	traindata = brown.tagged_sents(categories=['editorial'])
	t0 = nltk.DefaultTagger('NN')
	t1 = nltk.UnigramTagger(traindata, backoff=t0)
	t2 = nltk.BigramTagger(traindata, backoff=t1)
	nodetext = raw_input(">> ")
	grammar = "NP: {<JJ>*<NN>+}"
	phrases = []
	#tag_list = pos_tag(word_tokenize(nodetext))
	tag_list = t2.tag(word_tokenize(nodetext))
	#parser = RegexpParser(grammar)
	#result = parser.parse(tag_list)
	print tag_list