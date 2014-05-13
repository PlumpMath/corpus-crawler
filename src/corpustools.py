# Copyright (c) 2014 Jacob Troxel under The MIT License (MIT)
# Full terms and conditions of License available in LICENSE

import os.path as osp
from nltk.corpus import PlaintextCorpusReader as PCReader

class CorpusReader:
	"""Reads a corpus and generates word lists.  Uses the NLTK toolkit."""
	def __init__(self, corpus_path):
		self.corpus_path = corpus_path
		self._reader = PCReader(self.corpus_path, ".*")

	def print_fileids(self):
		print (self._reader.fileids())