# Copyright (c) 2014 Jacob Troxel under The MIT License (MIT)
# Full terms and conditions of License available in LICENSE

from corpusdocs import *
from nltk.corpus import *
from nltk.tokenize import RegexpTokenizer as RegexT
from nltk.chunk.regexp import RegexpParser
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import os.path as osp
import os
import nltk.text
import nltk.tree as NLTREE
import xml.etree.ElementTree as ET
import xml
import nltk.tag
from nltk.corpus import brown

class CorpusReader:
	"""Reads a corpus and generates word lists.  Uses the NLTK toolkit."""
	word_list = []

	def __init__(self, corpus_path):
		self.corpus_path = corpus_path
		self._reader = PlaintextCorpusReader(self.corpus_path, ".*")
		self.stopword_list = stopwords.words('english')
		self.clean_word_list(self._reader.words())
		self.text = nltk.Text(self.word_list)

	def fileids(self):
		return self._reader.fileids()

	def print_fileids(self):
		print (self._reader.fileids())

	def clean_word_list(self, word_list):
		self.word_list = []
		for word in word_list:
			if word.lower() not in self.stopword_list:
				self.word_list.append(word.upper())
		self.word_list = list(sorted(set(self.word_list)))

	def get_words(self):
		return self.word_list
#end class def

#helper functions
def LoadXML(path, filename, t2):
	doc = Document(filename)
	try:
		tree = ET.parse(path + filename)
		root = tree.getroot()
		datanode = root.find("dataset")
		abnode = datanode.find("abstract")
		for word in extract_words(abnode.find("para").text, t2, doc, "ABSTRACT"):
			doc.add_word(Word("ABSTRACT",word))
		#extract_words(abnode.find("para").text, t2, doc, "ABSTRACT")

		for keyword in datanode.iter("keyword"):
			for word in extract_words(keyword.text, t2, doc, "KEYWORD"):
				doc.add_word(Word("KEYWORD",word))
			#extract_words(keyword.text, t2, doc, "KEYWORD")

		titlenode = datanode.find("title")
		for word in extract_words(titlenode.text, t2, doc, "TITLE"):
			doc.add_word(Word("TITLE",word))
		#extract_words(titlenode.text, t2, doc, "TITLE")
	except AttributeError:
		return None
	except xml.etree.ElementTree.ParseError:
		return None
	return doc

def extract_words(nodetext, t2, doc, location):
	try:
	#	tokenizer = RegexT(r'\w*[a-zA-Z]\w*')
	#	return tokenizer.tokenize(nodetext)
	#except TypeError:
	#	return []
		grammar = "NP: {<JJ>*<NN>+}"
		phrases = []
		final_phrases = []
		for sent in sent_tokenize(nodetext):
			doc.add_sentence(Sentence(location, sent))
			tag_list = t2.tag(word_tokenize(sent))
			parser = RegexpParser(grammar)
			result = parser.parse(tag_list)
			for phrase in result:
				if isinstance(phrase, NLTREE.Tree) and phrase.node == "NP":
					phrases.append("_".join([word for word,pos in phrase.leaves()]))
					#n_phrase = "_".join([word for word,pos in phrase.leaves()])
					#if any(c.isdigit() for c in n_phrase):
				#		continue
				#	elif '.' in n_phrase:
				#		continue
				#	else:
				#		doc.add_word(Word(location, n_phrase, sent))

	except TypeError:
		return []
	for phrase in phrases:
		if any(c.isdigit() for c in phrase):
			continue
		elif '.' in phrase:
			continue
		else:
			final_phrases.append(phrase)

	return final_phrases

def get_cooccurence(doc_list, word1, word2):
	total = 0
	cocount = 0
	for doc in doc_list:
		if word1 in doc.values():
			total += 1
			if word2 in doc.values():
				cocount += 1
	if total == 0:
		return 0
	else:
		return float(cocount)/float(total)

def get_average_distances(word_list):
	averages = {}
	for word in word_list:
		print "Checking " + word
		average = 0
		count = 0
		try: 
			synset_one = wn.synsets(word)[0]
		except IndexError:
			continue
		#get average distance from each other word
		for other_word in word_list:
			if word != other_word:
				try:
					synset_two = wn.synsets(other_word)[0]
				except IndexError:
					continue
				word_score = synset_one.wup_similarity(synset_two)
				if word_score != None:
					average += float(word_score)
					count += 1
		if count != 0:
			averages[word] = float(average)/float(count)
		else:
			averages[word] = 0
	return averages

def generate_metrics(filename, doccount):
	phrase_set = {}
	filein = open(filename, 'r')
	for line in filein:
		#parse this CSV line, which is word, then document, then location
		phrase_info = line.split(',')
		if len(phrase_info) > 4:
			#something was wrong with the original parse - maybe a comma in the NP?
			continue
		else:
			try:
				nounphrase = phrase_info[0]
				document = phrase_info[1]
				location = phrase_info[2]
				if nounphrase not in phrase_set:
					phrase_set[nounphrase] = { 'docs':[document], 'google_hits':0, 'occ':0, 'wordnet':'N', 'locations':{}, 'freq_location':'', 'one_mercury_hits':0 }
				else:
					if document not in phrase_set[nounphrase]['docs']:
						phrase_set[nounphrase]['docs'].append(document)
				if location not in phrase_set[nounphrase]['locations']:
					phrase_set[nounphrase]['locations'][location] = 1
				else:
					phrase_set[nounphrase]['locations'][location] += 1
				phrase_set[nounphrase]['freq_location'] = get_highest(phrase_set[nounphrase]['locations'])
			except IndexError:
				continue

	fileout = open("/home/jtroxel/np_metrics.csv", 'w')

	for phrase in phrase_set:
		has_digits = False
		for char in phrase:
			if char.isdigit():
				has_digits = True
		#phrase_set[phrase]['occ'] = float(phrase_set[phrase]['docs']) / float(doccount)
		if not has_digits:
			wordnet_set = wn.synsets(phrase)
			yes_no_wordnet = 'Y' if len(wordnet_set) > 0 else 'N'
			fileout.write(','.join([phrase, str(len(phrase_set[phrase]['docs'])), str(yes_no_wordnet), str(len(phrase_set[phrase]['locations'])), phrase_set[phrase]['freq_location']]))
			fileout.write('\n')

	fileout.close()

def get_highest(dictionary):
	for key in dictionary:
		highest = True
		for otherkey in dictionary:
			if dictionary[key] < dictionary[otherkey]:
				highest = False

		if highest:
			return key
	return ""