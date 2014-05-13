# Copyright (c) 2014 Jacob Troxel under The MIT License (MIT)
# Full terms and conditions of License available in LICENSE

import os.path as osp
from nltk.corpus import PlaintextCorpusReader as PCReader
from nltk.corpus import stopwords
import nltk.text

class CorpusReader:
	"""Reads a corpus and generates word lists.  Uses the NLTK toolkit."""
	word_list = []

	def __init__(self, corpus_path):
		self.corpus_path = corpus_path
		self._reader = PCReader(self.corpus_path, ".*")
		self.stopword_list = stopwords.words('english')
		self.clean_word_list(self._reader.words())
		self.text = nltk.Text(self.word_list)

	def print_fileids(self):
		print (self._reader.fileids())

	def clean_word_list(self, word_list):
		for word in word_list:
			if word.lower() not in self.stopword_list:
				self.word_list.append(word.upper())
		self.word_list = list(sorted(set(self.word_list)))

	def get_words(self):
		return self.word_list