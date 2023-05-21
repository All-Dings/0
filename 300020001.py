# Dings-Tool-Python
'''

The Dings-Tool-Python is the [Dings-Tool](300020000.md) written in the [Python-Programming-Language](9010003.md).
'''
import Dings_Lib
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
import contextlib as Context_Lib
import logging as Logging
import re as Re
import sys as Sys

Logging.getLogger().setLevel(Logging.DEBUG)

# Test-Option
class Test_Option_Class(Dings_Lib.String_Option_Class):
	def __init__(Self):
		super().__init__("Test", "Select Test-Case TEST", "TEST")

# Test-Option
class Test_Option_String_Class(Dings_Lib.String_Option_Class):
	def __init__(Self):
		super().__init__("String-Test", "Test String Option", "STRING")

# Pos-Option
class Pos_Option_String_Class(Dings_Lib.String_Option_Class):
	def __init__(Self):
		super().__init__("Position", "Position in String", "POSITION")

## Command: Dings
class Dings_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings"
		Self.Help_On_Empty = True
	def Run(Self):
		return 0
	def Info(Self):
		print("Tool for working with Dings.")

def Get_Command_List(Argument_List, Start_Pos):
	Argument = ""
	if (Argument_List):
		for Arg in Argument_List:
			if Argument == "":
				Argument = Arg
			else:
				Argument = Argument + "_" + Arg
	Argument = Argument.lower()
	Answer = ""
	for Command in Dings_Command_Class.Command_List.values():
		Pos = Start_Pos
		# print(f"Arg={Argument} Command={Command.Name[6:]}")
		if (Command.Name[6:] == Argument):
			continue
		if (Command.Name[6:].startswith(Argument)):
			# print(Command.Name[6:].replace("_", " "))
			Command_Parts = Command.Name[6:].split("_")
			if (len(Command_Parts) > Pos):
				continue
			for Arg in Command_Parts:
				Pos = Pos - 1
				if (Pos > 0):
					continue
				if not Answer:
					Answer = Arg
				else:
					Answer = Answer + " " + Arg
				break
	return Answer

## Command: Dings-Ls
class Dings_Ls_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_ls"
	def Run(Self):
		Dings_Lib.Read_Dings_File_List()
		Current_Dings_File = Dings_Lib.Get_Current_Dings_File()
		for Dings_File_Number in Current_Dings_File.Meta_Data[int(300000017)]:
			Dings_File = Dings_Lib.Get_Dings_File(Dings_File_Number)
			if 300000017 in Dings_File.Meta_Data:
				print(f"{Dings_File.Name}.{Dings_File.Number}/")
			else:
				print(f"{Dings_File.Name}.{Dings_File.Number}")
		for Dings_File_Number in Current_Dings_File.Meta_Data[int(300000019)]:
			Dings_File = Dings_Lib.Get_Dings_File(Dings_File_Number)
			print(f".. ({Dings_File.Name}.{Dings_File.Number})")
		# Dings_Lib.Print_Dings_File_Targets(int(Self.Remaining_Argument_List[0]))
		return 0

	def Info(Self):
		print("List Directory")

## Command: Dings-Cd
class Dings_Cd_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_cd"
	def Run(Self):
		Dings_Lib.Read_Dings_File_List()
		Current_Dings_File = Dings_Lib.Get_Current_Dings_File()
		Cd_Dings_File_Name = Self.Remaining_Argument_List[0]
		for Dings_File_Number in Current_Dings_File.Meta_Data[int(300000017)]:
			Dings_File = Dings_Lib.Get_Dings_File(Dings_File_Number)
			if not int(300000017) in Dings_File.Meta_Data:
				continue
			if (Dings_File.Name.lower() == Cd_Dings_File_Name):
				Dings_Lib.Set_Current_Dings_File(Dings_File.Number)
				return 0
		print(f"Error: No such Directory: {Cd_Dings_File_Name}", file=Sys.stderr)
		return 1

	def Info(Self):
		print("Change Directory")

## Web_Server
class Web_Server_Class(BaseHTTPRequestHandler):
	def do_GET(Self):
		Self.send_response(200)
		Self.send_header("Content-type", "text/html")
		Self.end_headers()
		Request = Self.path[1:]
		if Dings_Lib.Get_File_Extension(Request) == "html":
			File = open(Self.path[1:], mode='r')
			File_Content = File.read()
			File.close()
			Self.wfile.write(bytes(File_Content, "utf-8"))
		else:
			Command = Request.lower()
			Logging.warning("Command %s", Command)
			Command_Parts = Command.split(" ")
			Old_Stdout = Sys.stdout
			Sys.stdout = Result = StringIO()
			Dings_Lib.Command_Class.Run_Command(Command_Parts[0], Command_Parts[1:])
			Sys.stdout = Old_Stdout
			Self.wfile.write(bytes(Result.getvalue(), "utf-8"))

## Command: Dings-Server
class Dings_Server_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_server"
		Self.Prefix = "dings_"
		Self.Host_Name = "localhost"
		Self.Server_Port = 8000

	def Run(Self):
		Dings_Lib.Read_Dings_File_List()
		Web_Server = HTTPServer((Self.Host_Name, Self.Server_Port), Web_Server_Class)
		Logging.info("Server started http://%s:%s", Self.Host_Name, Self.Server_Port)
		try:
			Web_Server.serve_forever()
		except KeyboardInterrupt:
			pass
		Web_Server.server_close()
		Logging.info("Server stopped.")
		quit(0)

	def Info(Self):
		print("Start a Web-Server-Session")

## Command: Dings-Shell
class Dings_Shell_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_shell"
		Self.Prefix = "dings_"
		Self.Current = int(17)
	def Run(Self):
		Dings_Lib.Read_Dings_File_List()
		while(True):
			Command = input().lower()
			if (Command == "exit" or Command == "quit"):
				quit(0)
			Command_Parts = Command.split(" ")
			Dings_Lib.Command_Class.Run_Command(Command_Parts[0], Command_Parts[1:])
			# for Command in Dings_Command_Class.Command_List.values():
			#	if (Command.Name.startswith(Self.Prefix)):
			#		print(Command.Name[len(Self.Prefix):])
	def Info(Self):
		print("Start a Shell-Session")

## Command: Dings-Bash-Completion
class Dings_Completion_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_completion"
		Self.Pos_Opt = Pos_Option_String_Class()
		Self.Option_List.append(Self.Pos_Opt)
	def Run(Self):
		Argument = ""
		if (Self.Remaining_Argument_List):
			for Arg in Self.Remaining_Argument_List:
				if Argument == "":
					Argument = Arg
				else:
					Argument = Argument + "_" + Arg
		Argument = Argument.lower()
		Answer = ""
		for Command in Dings_Command_Class.Command_List.values():
			Pos = int(Self.Pos_Opt.Value)
			# print(f"Arg={Argument} Command={Command.Name[6:]}")
			if (Command.Name[6:] == Argument):
				continue
			if (Command.Name[6:].startswith(Argument)):
				# print(Command.Name[6:].replace("_", " "))
				Command_Parts = Command.Name[6:].split("_")
				if (len(Command_Parts) > Pos):
					continue
				for Arg in Command_Parts:
					Pos = Pos - 1
					if (Pos > 0):
						continue
					if not Answer:
						Answer = Arg
					else:
						Answer = Answer + " " + Arg
					break
		print(Answer)
		return 0
	def Info(Self):
		print("Print Bash-Completion List")

## Command: Dings-Generate
class Dings_Generate_Command_Class(Dings_Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_generate"
		Self.Argument_String = "INPUT-FILE"
	def Run(Self):
		if (not Self.Remaining_Argument_List):
			print(f"Error: No Input-File specified", file=Sys.stderr)
			return 1
		if (len(Self.Remaining_Argument_List) > 1):
			print(f"Error: Too many Arguments specified: Self.Remaining_Argument_List", file=Sys.stderr)
			return 1
		Input_File_Name = Self.Remaining_Argument_List[0]
		Input_File_Extension = Dings_Lib.Get_File_Extension(Input_File_Name)
		Output_File_Name = Input_File_Name.replace("." + Input_File_Extension, ".md")
		with open(Output_File_Name, 'w') as File:
			with Context_Lib.redirect_stdout(File):
				Dings_Lib.Language_To_Markdown(Input_File_Name)
		return 0
	def Info(Self):
		print("Automatically transform INPUT-FILE into Markdown-File.")

## Command: Dings-List
class Dings_List_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_list"
		Self.Help_On_Empty = False
	def Run(Self):
		Dings_Lib.Read_Dings_File_List()
		Dings_Lib.Print_Dings_File_List()
		return 0
	def Info(Self):
		print("List Dings")

## Command: Dings-Test
class Dings_Test_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_test"
		Self.Help_On_Empty = True
	def Run(Self):
		return 0
	def Info(Self):
		print("Run Test-Cases")

## Command: Dings-Test-List
class Dings_Test_List_Command_Class(Dings_Test_Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_test_list"
		Self.Help_On_Empty = False
		Self.Option_List.append(Test_Option_Class())
	def Run(Self):
		Test_List = Dings_Lib.Get_Test_List()
		for Test_Name in Test_List:
			print(Test_Name)
		return 0
	def Info(Self):
		print("List Test-Cases")

## Command: Dings-Test-Generate
class Dings_Test_Generate_Command_Class(Dings_Test_Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_test_generate"
	def Run(Self):
		Test_List = Dings_Lib.Get_Test_List()
		for Test_Name, Test_Function in Test_List.items():
			Output_File_Name = Dings_Lib.Test_Output_File_Name(Test_Name)
			print(f"Generate: {Output_File_Name}")
			with open(Output_File_Name, 'w') as File:
				with Context_Lib.redirect_stdout(File):
					Test_Function()
		return 0
	def Info(Self):
		print("Run Test-Cases")

## Command: Dings-Test-Run
class Dings_Test_Run_Command_Class(Dings_Test_Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_test_run"
	def Run(Self):
		if (not Self.Remaining_Argument_List):
			Test_Regexp = ".*"
		else:
			Test_Regexp = Self.Remaining_Argument_List[0]
		Test_Reg_Exp = Re.compile(Test_Regexp)
		Test_List = Dings_Lib.Get_Test_List()
		for Test_Name, Test_Function in Test_List.items():
			if (Test_Reg_Exp.match(Test_Name)):
				Old_Stdout = Sys.stdout
				Sys.stdout = Result = StringIO()
				Test_Function()
				Sys.stdout = Old_Stdout
				Output_File_Name = Dings_Lib.Test_Output_File_Name(Test_Name)
				with open(Output_File_Name) as File: Expected_Result = File.read()
				if (Result.getvalue() == Expected_Result):
					print(f"{Test_Name}: Ok")
				else:
					print(f"{Test_Name}: Fail")
		return 0
	def Info(Self):
		print("Run Test-Cases")

# Entry-Point
def Main():
	Argument_List = Sys.argv.copy()
	Argument_List[0] = "dings"
	Command_List = Dings_Lib.Get_Dict_Sub_Set(globals(), ".*_Command_Class$")
	Dings_Lib.Command_Class.Parse_And_Run("dings", Command_List, Argument_List)

Main()
