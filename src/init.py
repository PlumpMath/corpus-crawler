class MainMenu:
	"""Main Menu for the CorpusCrawler tool, written for Python 2.7"""
	def __init__(self):
		self.is_running = True

	def display_help(self):
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
		return False

	def run(self):
		print ("Welcome to CorpusCrawler v1.0")
		while self.is_running:
			self.prompt()

def main():
	m = MainMenu()
	m.run()
main()