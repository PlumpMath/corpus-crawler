import os.path as osp

class MainMenu:
	"""Main Menu for the CorpusCrawler tool, written for Python 2.7"""
	def __init__(self):
		self.is_running = True
		self.corpus_path = ""
		self.load_config()

	def load_config(self):
		print ("Loading config file 'settings.conf'")
		config = "../settings.conf"
		if osp.exists(config): #load config
			config_file = open(config, "r")
			for line in config_file:
				if line[0] != "#":
					self.load(line)
		else: #no config, generate one
			print ("WARNING! Setting file not found. Please update settings.conf before continuing.")
			new_config = open(config, "w")
			new_config.write("# Generated settings.conf. Please update before using.\n")
			new_config.write("# Anything after a '#' will not be read by the program.\n\n")
			new_config.write("# Where the program will look for a corpus\n")
			new_config.write("corpus")
			new_config.close()

	def load(self, line):
		setting_parts = line.split(" ",1)
		setting = setting_parts[0]
		try:
			value = setting_parts[1]
		except IndexError:		
			value = ""
		if setting == "corpus":
			print ("...loading corpus path...")
			self.set_corpus_path(value)

	def display_help(self, flags):
		print ("HELP MENU")

	def prompt(self):
		user_input = str(raw_input("> "))
		command_list = user_input.split(' ', 1) #get us the command as one word, and the flags as another
		command = command_list[0]
		try:
			flags = command_list[1]
		except IndexError:
			flags = ""
		if not self.do_command(command, flags):
			print ("Could not find command '" + command + "'. Type help to see command list.")

	def do_command(self, command, flags):
		if command == "quit" or command == 'q':
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
		else:
			return False

	def run(self):
		while self.is_running:
			self.prompt()

	def set_corpus_path(self, path):
		if path == "":
			print ("Corpus path set to current directory.")
		elif osp.isdir(path):
			self.corpus_path = path
			print ("Corpus path set to '" + path + "'.")
		else:
			print ("Error: '" + path + "' is not a directory.")

def main():
	m = MainMenu()
	m.run()
main()