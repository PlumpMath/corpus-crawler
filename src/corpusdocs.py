# Copyright (c) 2014 Jacob Troxel under The MIT License (MIT)
# Full terms and conditions of License available in LICENSE

from nltk.corpus import *

class Document:
	word_list = []
	fileid = ""
	def __init__(self, fileid):
		self.fileid = fileid
		self.stop_words = stopwords.words('english')

	def add_word(self, word):
		if word.value.lower() not in self.stop_words:
			self.word_list.append(word)

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
	location = ""
	value = ""
	def __init__(self, location, value):
		self.location = location.upper()
		self.value = value.upper()
#end class def