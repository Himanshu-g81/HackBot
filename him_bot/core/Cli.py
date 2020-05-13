"""
    Himanshu Gwalani
    2017ucp1356
"""
from core import utils,db,module,Settings,browser
from core.color import *
import os,sys,time,random,traceback,json,argparse,readline

global modules,all_keywords
modules = db.get_modules()

all_keywords = [
			"help","?","os","banner","exit","quit",
			"list","show","use","info","previous","search","sessions","jobs",
			"database","debug","dev","verbose","reload","refresh",
			"history","makerc","resource"
			]

help_msg = end+G+end
module_help = G+end

sessions_parser = argparse.ArgumentParser(prog="sessions",add_help=False)
sessions_parser.add_argument('-h', action="store_true", help="Show this help message.") # I done that because print the normal help exits the framework
sessions_parser.add_argument('-l', action="store_true", help='List all captured sessions.')
sessions_parser.add_argument('-K', action="store_true", help='Remove all captured sessions.')
sessions_parser.add_argument('-s', metavar='', help='Search for sessions with a specifed type.')
sessions_parser.add_argument('-k', metavar='', help='Remove a specifed captured session by ID')
sessions_parser.add_argument('-i', metavar='', help='Interact with a captured session by ID.')

def general_commands(command, args=None, full_help=module_help):

	if command in ["exit","quit"]:
		if Settings.headless_browser:
			Settings.headless_browser.close_all()
			Settings.headless_browser = None
		exit(0)

	else:
		return False

chars_filter = { ";":"{{Semi-Colon}}" } # Here we add all the chars that may do some problems while processing

def start(rc=False):
	
	myinput = input
	utils.Input_completer(all_keywords+modules)

	while True:
		if sys.stdin.closed or sys.stdout.closed:
			exit(0)
		try:
			name = Settings.name
			if rc:
				cmd_to_run = rc
				print("\n"+name+G+" > "+end+cmd_to_run)
			else:
				cmd_to_run = myinput("\n"+name+G+" > "+end)

			cmd_to_run = cmd_to_run.strip()
			
			for c in cmd_to_run.split(";"):
				for char in chars_filter:
					c = c.replace(chars_filter[char],char) # Yeah reversing
				if len( cmd_to_run.split(";") ) > 1:
					print(G+" > "+end+ c)
				if Settings.running_module:
					module.handle(c)
					continue

				head = c.lower().split()[0]
				args = " ".join(c.split()[1:])

				if head == 'exit':
					if Settings.headless_browser:
						Settings.headless_browser.close_all()
						Settings.headless_browser = None
					exit(0)
				
				command_handler(c)

		except KeyboardInterrupt:
			print()
			error("KeyboardInterrupt use exit command!")
			continue
		finally:
			if rc:
				time.sleep(0.3)
				break

#A function for every command (helpful in the future)
def command_handler(c):
	#parsing a command and pass to its function
	if c=="" or c[0]=="#":return
	command = c.lower().split()[0]
	args    = " ".join(c.split()[1:])
	try:
		handler = globals()["command_{}".format(command)]
		handler(args)
		Settings.update_history(c)  # Log the important commands and the ones that doesn't gave error :D
	except Exception as e:
		if command not in all_keywords:
			error( command + " is not recognized as an internal command !")
			#To check for the wanted command on typos
			wanted = utils.grab_wanted(command,all_keywords)
			if len(wanted)>0:
				status( "Maybe you meant : " + wanted )
		else:
			error( "Error in executing command "+ command )
		status( "Type help or ? to learn more..")

		

def command_list(text=False):
	cols = [G+Bold+"Name"+end,G+Bold+"Description"+end]
	Columns = []
	for p in modules:
		info = db.grab(p)
		Columns.append([p ,info.short_description])
	utils.create_table(cols,Columns)

def command_show(text=False):
	command_list(text)

def command_search(text=False):
	if not text:
		error("You must enter a text to search for !")
	else:
		cols = [G+Bold+"Name"+end,G+Bold+"Description"+end]
		Columns = []
		text = text.lower()
		for p in modules:
			info = db.grab(p)
			full_text = " ".join([info.author, info.short_description, info.full_description if info.full_description else ""]).lower()
			if text in full_text:
				Columns.append([p ,info.short_description])
		if not Columns:
			error("Didn't find a module have the entered text!")
		else:
			utils.create_table(cols,Columns)

def command_os(text=False):
	if text:
		os.system(text)
	else:
		error("You must enter a command to execute !")
		return

def command_use(p=False):
	p = p.lower()
	if not p:
		error("You must enter a module to use !")
		return
	else:
		if p in modules:
			if Settings.running_module:
				Settings.update_previous()
			Settings.running_module = p
			module.Exec(all_keywords)
			return
		else:
			error(p+" module not found!")

def command_sessions(text=""):
	sessions_file = os.path.join("core","sessions.json")
	sessions = json.load(open( sessions_file ))
	try:
		cmd = sessions_parser.parse_args(text.split())
	except:
		cmd = sessions_parser.parse_args("") # Fuck you argparse, next time I will use more flexible module like getopt globally
		# I done this because any error argparse gives is printed and it exit the framework but now no

	if cmd.h:
		print(sessions_parser.format_help())
		return

	elif not text or cmd.l:
		if not sessions:
			error("No captured sessions.")
		else:
			cols = [G+Bold+"ID"+end, G+Bold+"Module name"+end,G+Bold+"Captured on"+end]
			Columns = []
			for session_id in list(sessions.keys()):
				line = sessions[session_id]
				date = line["session_path"].replace( os.path.join("sessions",""),"").replace(".session","")
				Columns.append([session_id, line["name"], date])
			utils.create_table(cols,Columns)

	elif cmd.i:
		if not sessions:
			error("No captured sessions.")
		else:
			if not cmd.i:
				error("Enter a session ID to interact with!")
			elif cmd.i not in list(sessions.keys()):
				error("Invalid session ID!")
			else:
				if not Settings.visible_browser:
					Settings.visible_browser = browser.visible_browsers()
				status(f"Starting interaction with ({cmd.i})...")
				if sessions[cmd.i]["session_type"] == "localStorage":
					Settings.visible_browser.load_localstorage(cmd.i)
				else:
					Settings.visible_browser.load_cookie(cmd.i)

	elif cmd.k:
		if not sessions:
			error("No captured sessions.")
		else:
			if not cmd.k:
				error("Enter a session ID to interact with!")
			elif cmd.k not in list(sessions.keys()):
				error("Invalid session ID!")
			else:
				session_file = sessions[cmd.k]["session_path"]
				os.remove(session_file)
				sessions.pop(cmd.k)
				f = open( sessions_file,"w" )
				json.dump(sessions, f, indent=2)
				f.close()
				status(f"Session ({cmd.k}) removed!")

	elif cmd.s:
		if not sessions:
			error("No captured sessions.")
		else:
			if not cmd.s:
				error("Enter a session type to filter with!")
			elif cmd.s not in [ sessions[i]["name"] for i in list(sessions.keys()) ]:
				error("Invalid session type!")
			else:
				cols = [G+Bold+"ID"+end, G+Bold+"Captured on"+end]
				Columns = []
				for session_id in list(sessions.keys()):
					line = sessions[session_id]
					if cmd.s == line["name"]:
						date = line["session_path"].replace( os.path.join("sessions",""),"").replace(".session","")
						Columns.append([session_id, date])
				utils.create_table(cols,Columns)

	elif cmd.K:
		if not sessions:
			error("No captured sessions.")
		else:
			for sess in list(sessions.keys()):
				session_file = sessions[sess]["session_path"]
				os.remove(session_file)
			f = open( sessions_file,"w" )
			json.dump({}, f, indent=2)
			f.close()
			status(f"All captured sessions removed!")

def command_jobs(process=""):
	help_command = """
usage: jobs [-h] [-l] [-K] [-k]

optional arguments:
  -h   Show this help message.
  -l   List all running jobs.
  -K   Terminate all running jobs.
  -k   Terminate jobs by job ID or module name"""

	if process=="-h":
		print(help_command)
		return

	else:
		if not Settings.headless_browser or Settings.headless_browser.browsers=={}:
			error("No active jobs.")
			return

	option = process.split()[:1]
	args   = process.split()[1:]
	if not process or option[0] =="-l":
		cols = [G+Bold+"ID"+end, G+Bold+"Module name"+end,G+Bold+"Serving on"+end]
		Columns = []
		for module_name in list(Settings.headless_browser.browsers.keys()):
			line = Settings.headless_browser.browsers[module_name]
			if Settings.headless_browser.browsers[module_name]["Status"]:
				uri = line["host"]+":"+line["port"]
				Columns.append([line["Controller"].session_id, module_name, uri])
		if Columns:
			utils.create_table(cols,Columns)
		else:
			error("No active jobs.")

	elif option[0]=="-k":
		if not args:
			error("Enter a job ID/module name to terminate!")
		else:
			for module_name in list(Settings.headless_browser.browsers.keys()):
				if Settings.headless_browser.browsers[module_name]["Controller"].session_id == args[0]:
					Settings.headless_browser.close_job(module_name)
					status("Job terminated successfully!")
					return
			for module_name in list(Settings.headless_browser.browsers.keys()):
				if module_name == args[0]:
					Settings.headless_browser.close_job(module_name)
					status("Job terminated successfully!")
					return
			error("Job not found!")

	elif option[0] == "-K":
		Settings.headless_browser.close_all()
		Settings.headless_browser = None
		status("All jobs terminated successfully!")

	else:
		error("Invalid option!")

def command_previous(p=False):
	if len(Settings.previous)!=0:
		prev = Settings.previous.pop(-1)
		command_use(prev)
	else:
		error("You haven't used a modules yet !")

def command_resource(p=False):
	try:
		with open(p,"r") as f:
			cmds = f.readlines()
			for cmd in cmds:
				start(cmd.strip())
	except:
		if not p:
			error("Enter a resource file to read!")
		return

def command_info(p=False):
	if not p:
		error("You must enter a module to get it's information !")
		return
	p   = p.lower()
	if p in modules:
		info = db.grab(p)
		print( "      Module : " + utils.humanize(p) )
		print( " Provided by : " + info.author )
		if info.full_description:
			print( " Description : " + info.full_description )
		else:
			print( " Description : " + info.short_description )
	else:
		error(p+" module not found!")



