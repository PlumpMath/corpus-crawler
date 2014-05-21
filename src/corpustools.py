# Copyright (c) 2014 Jacob Troxel under The MIT License (MIT)
# Full terms and conditions of License available in LICENSE

from corpusdocs import *
from nltk.corpus import *
from nltk.tokenize import RegexpTokenizer as RegexT
from nltk.corpus import wordnet as wn
import os.path as osp
import os
import nltk.text
import xml.etree.ElementTree as ET
import xml

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
def LoadXML(path, filename):
	doc = Document(filename)
	try:
		tree = ET.parse(path + filename)
		root = tree.getroot()
		datanode = root.find("dataset")
		abnode = datanode.find("abstract")
		for word in extract_words(abnode.find("para").text):
			doc.add_word(Word("ABSTRACT",word))

		for keyword in datanode.iter("keyword"):
			for word in extract_words(keyword.text):
				doc.add_word(Word("KEYWORD",word))

		titlenode = datanode.find("title")
		for word in extract_words(titlenode.text):
			doc.add_word(Word("TITLE",word))
	except AttributeError:
		return None
	except xml.etree.ElementTree.ParseError:
		return None
	return doc

def extract_words(nodetext):
	try:
		tokenizer = RegexT(r'\w*[a-zA-Z]\w*')
		return tokenizer.tokenize(nodetext)
	except TypeError:
		return []

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
				