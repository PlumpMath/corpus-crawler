# Copyright (c) 2014 Jacob Troxel under The MIT License (MIT)
# Full terms and conditions of License available in LICENSE

from nltk.corpus import *

class Document:
	"""Corpus Document, tracks location and value of words"""
	word_list = []
	sentence_list = []
	fileid = ""
	def __init__(self, fileid):
		self.word_list = []
		self.sentence_list = []
		self.fileid = fileid
		self.stop_words = stopwords.words('english')

	def add_word(self, word):
		if word.value.lower() not in self.stop_words and not self.in_list(word):
			self.word_list.append(word)

	def in_list(self, word):
		for word1 in self.word_list:
			if word1.value == word.value and word1.location == word.location:
				return True
		return False

	def add_sentence(self, sentence):
		self.sentence_list.append(sentence)

	def sentences(self, location=""):
		if location=="":
			return self.sentence_list
		else:
			return [sentence for sentence in self.sentence_list if sentence.location == location]

	def words(self, location=""):
		if location=="":
			return self.word_list
		else:
			return [word for word in self.word_list if word.location == location]

	def values(self, location=""):
		if location=="":
			return [word.value for word in self.word_list]
		else:
			return [word.value for word in self.word_list if word.location == location]

#end class def

class Word:
	"""Corpus word, tied to a document and a location"""
	location = ""
	value = ""
	sentence = ""
	def __init__(self, location, value, sentence=""):
		self.location = location.upper()
		self.value = value.upper()
		self.sentence = sentence
#end class def

class Sentence:
	"""Corpus sentence, tied to a document and a location"""
	location = ""
	value = ""
	def __init__(self, location, value):
		self.location = location.upper()
		self.value = value
#end class def