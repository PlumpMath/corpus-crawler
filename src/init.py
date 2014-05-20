# Copyright (c) 2014 Jacob Troxel under The MIT License (MIT)
# Full terms and conditions of License available in LICENSE

import os.path as osp
import os
import ConfigParser
from corpustools import *
from nltk.corpus import wordnet as wn

class MainMenu:
	"""Main Menu for the CorpusCrawler tool, written for Python 2.7"""
	def __init__(self):
		self.doc_list = []
		self.word_list = []
		self.is_running = True
		self.corpus_path = None
		self.load_config()
		if self.corpus_path == None:
			self.set_corpus_path("")
		self.command_list = [['help',"Displays help info","help [command]"],['corpus',"Updates corpus path until next reload.", "corpus <path-to-corpus>"],
							['reload',"Reloads config file.", 'reload'],['quit',"Exits", 'quit'],['read',"Reads corpus and generates word list",'read']]

	def load_config(self):
		print ("Loading config file 'settings.conf'")
		root_path = osp.dirname(osp.dirname(osp.realpath(__file__)))
		config = root_path + "/settings.conf"
		if osp.exists(config): #load config
			parser = ConfigParser.ConfigParser()
			parser.optionxform=str
			parser.read(config)
			corpus_config = parser.get("CONFIG","CorpusPath")
			self.set_corpus_path(corpus_config)
		else: #no config, generate one
			print ("WARNING! Setting file not found. Please update settings.conf before continuing.")
			parser = ConfigParser.ConfigParser()
			parser.optionxform=str
			new_config = open(config, "a")
			new_config.write("# Generated settings.conf. Please update before using.\n\n")
			parser.add_section("CONFIG")
			parser.set("CONFIG","#CorpusPath",'/path/to/corpus/')
			parser.write(new_config)
			new_config.close()

	def display_help(self, flags):
		if flags == "":
			print ("Command List - Use 'help <command>' to get more info.")
			for command in self.command_list:
				print (command[0] + ": " + command[1])
		else:
			for command in self.command_list:
				if command[0] == flags:
					print (command[0] + ": " + command[1])
					print ("Usage: " + command[2])
					return
			print ("Could not find command '" + flags + "'. Type help to see command list.")

	def prompt(self):
		user_input = str(raw_input("> "))
		command_in = user_input.split(' ', 1) #get us the command as one word, and the flags as another
		command = command_in[0]
		try:
			flags = command_in[1]
		except IndexError:
			flags = ""
		if not self.do_command(command, flags):
			print ("Could not find command '" + command + "'. Type help to see command list.")

	def do_command(self, command, flags):
		if command == "quit" or command == 'q' or command == "exit":
			self.is_running = False
			return True
		elif command == "help":
			self.display_help(flags)
			return True
		elif command == "corpus":
			self.set_corpus_path(flags)
			return True
		elif command == "reload":
			self.load_config()
			return True
		elif command == "read":
			self._reader = CorpusReader(self.corpus_path)
			return True
		elif command == "display":
			self.display(flags)
			return True
		elif command == "loadxml":
			files = [name for name in os.listdir(self.corpus_path)]
			file_count = len(files)
			count = 0
			for fileid in files:
			#for fileid in self._reader.fileids():
				count += 1
				#print ("Loading " + self.corpus_path + fileid)
				print (str(100 * float(count) / float(file_count)) + "%")
				doc = LoadXML(self.corpus_path, fileid)
				if doc != None:
					self.doc_list.append(doc)
			for doc in self.doc_list:
				self.word_list += doc.values()
				self.word_list = list(set(self.word_list))
			print ("Found " + str(len(self.word_list)) + " unique words.")
			return True
		elif command == "cooccur":
			self.cooccur(flags)
			return True
		elif command == "clear":
			os.system('clear')
			return True
		elif command == "graph":
			self.graph(flags)
			return True
		elif command == "output":
			fileout = open("word_list.txt","w")
			fileout.write(",".join(self.word_list))
			fileout.close()
			return True
		else:
			return False

	def graph(self, flags):
		seed_word = flags.split(' ')[0]
		boundary = flags.split(' ')[1]
		for word in self.word_list:
			seed = wn.synset(seed_word + ".n.01")
			try:
				word_score = seed.wup_similarity(wn.synsets(word)[0])
				if word_score >= float(boundary):
					print (word + ": " + str(word_score))
			except IndexError:
				continue

	def cooccur(self, flags):
		flags_list = flags.split(' ')
		word1 = flags_list[0].upper()
		word2 = flags_list[1].upper()
		print (word1 + " -> " + word2 + " : " + str(get_cooccurence(self.doc_list, word1, word2)))
		print (word2 + " -> " + word1 + " : " + str(get_cooccurence(self.doc_list, word2, word1)))

	def display (self, flags):
		flags_list = flags.split(' ')
		ob_to_display = flags_list[0]
		if ob_to_display == "files":
			for doc in self.doc_list:
				print (doc.fileid)
		elif ob_to_display == "words":
			try:
				filenamei = flags_list.index("-f")
				filename = flags_list[filenamei + 1]
			except ValueError:
				filename = ""
			try:
				locationi = flags_list.index("-l")
				location = flags_list[locationi + 1]
			except ValueError:				
				location = ""
			self.print_words(filename, location)
				
	def print_words(self, filename, location):
		for doc in self.doc_list:
			if doc.fileid == filename or filename == "":
				print (doc.fileid)
				print [(word.value + ":" + word.location) for word in doc.words() if word.location == location or location == ""]

	def run(self):
		while self.is_running:
			self.prompt()

	def set_corpus_path(self, path):
		if path == "":
			print ("Corpus path set to current directory.")
		elif osp.isdir(path):
			self.corpus_path = path
			if self.corpus_path[-1] != "/":
				self.corpus_path += "/"
			print ("Corpus path set to '" + self.corpus_path + "'.")
		else:
			print ("Error: '" + path + "' is not a directory.")

def main():
	m = MainMenu()
	m.run()
main()