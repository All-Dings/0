# Dings-Tool-Python
'''

The Dings-Tool-Python is the [Dings-Tool](300020000.md) written in the [Python-Programming-Language](9010003.md).
'''
import Dings_Lib
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
import urllib.parse as Url_Lib_Parse
import http.client as Http_Client
import contextlib as Context_Lib
import logging as Logging
import os as Os
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
		print(Current_Dings_File.Meta_Data)
		for Dings_File_Number in Current_Dings_File.Meta_Data["300000017"]:
			Dings_File = Dings_Lib.Get_Dings_File(Dings_File_Number)
			if 300000017 in Dings_File.Meta_Data:
				print(f"{Dings_File.Name}.{Dings_File.Number}/")
			else:
				print(f"{Dings_File.Name}.{Dings_File.Number}")
		if not "300000019" in Current_Dings_File.Meta_Data:
			return 0
		for Dings_File_Number in Current_Dings_File.Meta_Data["300000019"]:
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
		for Dings_File_Number in Current_Dings_File.Meta_Data["300000017"]:
			Dings_File = Dings_Lib.Get_Dings_File(Dings_File_Number)
			if not "300000017" in Dings_File.Meta_Data:
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
		Request = Self.path[1:]
		Self.send_response(200)
		if Dings_Lib.Get_File_Extension(Request) == "html":
			Self.send_header("Content-type", "text/html")
		elif Dings_Lib.Get_File_Extension(Request) == "css":
			Self.send_header("Content-type", "text/css")
		elif Dings_Lib.Get_File_Extension(Request) == "jpg":
			Self.send_header("Content-type", "image/jpg")
		elif Dings_Lib.Get_File_Extension(Request) == "mp4":
			Self.send_header("Content-type", "video/mp4")
		else:
			Self.send_header("Content-type", "text/txt")
		Self.end_headers()
		if Dings_Lib.Get_File_Extension(Request) == "":
			Command = Request.lower()
			Logging.warning("Command %s", Command)
			Command_Parts = Command.split(" ")
			Old_Stdout = Sys.stdout
			Sys.stdout = Result = StringIO()
			Dings_Lib.Command_Class.Run_Command(Command_Parts[0], Command_Parts[1:])
			Sys.stdout = Old_Stdout
			Self.wfile.write(bytes(Result.getvalue(), "utf-8"))
		else:
			File = open(Self.path[1:], mode='rb')
			File_Content = File.read()
			File.close()
			Self.wfile.write(File_Content)

	'''
	import cgi as Cgi
	def parse_POST(Self):
		C_Type, P_Dict = Cgi.parse_header(Self.headers['content-type'])
		if C_Type == 'application/x-www-form-urlencoded':
			Length = int(Self.headers['content-length'])
			Post_Data = Url_Lib_Parse.parse_qs(Self.rfile.read(Length), keep_blank_values=1)
		elif C_Type == 'multipart/form-data':
			Post_Data = Cgi.parse_multipart(Self.rfile, P_Dict)
		else:
			Post_Data = {}
		return Post_Data
	'''

	def parse_POST(Self):
		Length = int(Self.headers['content-length'])
		Post_Data = Url_Lib_Parse.parse_qs(Self.rfile.read(Length), keep_blank_values=1)
		return Post_Data

	def do_POST(Self):
		Request = Self.path
		Post_Data = Self.parse_POST()
		print("POST")
		print(f"Request..: '{Request}'")
		for Data in Post_Data:
			print(f"Post_Data: '{Data}'")
		Self.wfile.write(bytes("OK", "utf-8"))

# IP-Adress-Option
class Address_Option_String_Class(Dings_Lib.String_Option_Class):
	def __init__(Self):
		super().__init__("Address", "Server Address and Port", "IP-ADDRESS:PORT")

## Command: Dings-Server
class Dings_Server_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_server"
		Self.Prefix = "dings_"
		Self.Address_Option = Address_Option_String_Class()
		Self.Option_List.append(Self.Address_Option)

	def Run(Self):
		if (Self.Address_Option.Set):
			Address = Self.Address_Option.Value.split(":")
			Self.Host_Name = Address[0]
			Self.Server_Port = int(Address[1])
		else:
			Self.Host_Name = "localhost"
			Self.Server_Port = 8000
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

## Command: Dings-Client
class Dings_Client_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_client"
		Self.Host_Name = "localhost"
		Self.Server_Port = 8000
	def Run(Self):
		Connection = Http_Client.HTTPConnection(Self.Host_Name + ":" + str(Self.Server_Port))
		Connection.request("GET", "/" + Self.Remaining_Argument_List[0])
		Response = Connection.getresponse()
		Data = Response.read().decode('utf-8')
		# print("Status: {} and reason: {}".format(Response.status, Response.reason))
		print(Data)
		Connection.close()
		return 0
	def Info(Self):
		print("Issue Client-Commands")

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
		print("Automatically transform INPUT-FILE into Markdown-File")

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

# Command: Dings-Html
class Dings_Html_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_html"
		Self.Help_On_Empty = True
	def Run(Self):
		return 0
	def Info(Self):
		print("Work with Html")

## Output-Option
class Output_Option_String_Class(Dings_Lib.String_Option_Class):
	def __init__(Self):
		super().__init__("Output", "Html-File to generate", "HTML-FILE")

## Command: Dings-Html-Generate
class Dings_Html_Generate_Command_Class(Dings_Html_Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_html_generate"
		Self.Argument_String = "MARKDOWN-FILE"
		Self.Output_Option = Output_Option_String_Class()
		Self.Option_List.append(Self.Output_Option)
	def Run(Self):
		if (not Self.Remaining_Argument_List):
			print(f"Error: No Markdown-File specified", file=Sys.stderr)
			return 1
		if (Self.Output_Option.Set):
			Output_File_Name = Self.Output_Option.Value
		Markdown_File = Self.Remaining_Argument_List[0]
		return Self.Gen_Html(Markdown_File, Output_File_Name)

	# Generate Pandoc-Markdown for Ids: "Heading <a id=4711>" -> "Heading{#4711}"
	def Gen_Inline_Ids(Self, Markdown_File):
		Heading_Reg_Exp = Re.compile('^' + '(' + '#+' + ')' + '\s+' + '(' + '.+' + ')' + '\s*' + '<a id="' + '(' + '\d+' + ')' + '"/>')
		with open(Markdown_File) as File:
			Md_Lines = File.readlines()
		for Line in Md_Lines:
			Match = Heading_Reg_Exp.match(Line)
			if Match:
				print(Match.group(1) + " " + Match.group(2).strip() + "{#" + Match.group(3) + "}")
			else:
				print(Line, end="")

	def Gen_Side_Bar(Self, Markdown_File):
		Heading_Reg_Exp = Re.compile('^#+\s+' + '(' + '.+' + ')' + '\s*' + '<a id="' + '(' + '\d+' + ')' + '"/>')
		with open(Markdown_File) as File:
			Md_Lines = File.readlines()

		First = True
		print('\t<div class="Dings-Side-Bar-Hide" id="Dings-Side-Bar">')
		for Line in Md_Lines:
			Match = Heading_Reg_Exp.match(Line)
			if Match:
				Text = Match.group(1).strip()
				Link_Target = Match.group(2).strip()
				if Line[0:5] == "#####":
					Heading_Class = 'class="Heading_6"'
				elif Line[0:4] == "####":
					Heading_Class = 'class="Heading_5"'
				elif Line[0:3] == "###":
					Heading_Class = 'class="Heading_4"'
				elif Line[0:2] == "##":
					Heading_Class = 'class="Heading_3"'
				elif Line[0:1] == "##":
					Heading_Class = 'class="Heading_2"'
				elif Line[0] == "#":
					Heading_Class = 'class="Heading_1"'
				if First:
					print('\t\t<a id="First-Sidebar-Element" href="#' + Link_Target + '" ' + Heading_Class + ' onclick="Select_Sidebar_Element(event)">' + Text + '</a>')
					First = False
				else:
					print('\t\t<a href="#' + Link_Target + '" ' + Heading_Class + ' onclick="Select_Sidebar_Element(event)">' + Text + '</a>')
		print('\t</div>')

	def Gen_Html_Pandoc(Self, Markdown_File):
		with open("300000002.htm") as Htm_File:
			Htm_Lines = Htm_File.readlines()
		for Line in Htm_Lines:
			if "$Dings-Side-Bar$" in Line:
				Self.Gen_Side_Bar(Markdown_File)
			else:
				print(Line, end='')

	def Gen_Html(Self, Markdown_File, Output_File_Name=None):
		with open(Markdown_File) as File:
			First_Line = File.readline()
		Title = First_Line[2:].strip()
		Htm_Pandoc_File_Name = Os.path.splitext(Markdown_File)[0] + '.pandoc.htm'
		Md_Pandoc_File_Name = Os.path.splitext(Markdown_File)[0] + '.pandoc.md'
		if not Output_File_Name:
			Output_File_Name = Os.path.splitext(Markdown_File)[0]+'.html'
		with open(Htm_Pandoc_File_Name, 'w') as File:
			with Context_Lib.redirect_stdout(File):
				Self.Gen_Html_Pandoc(Markdown_File)
		with open(Md_Pandoc_File_Name, 'w') as File:
			with Context_Lib.redirect_stdout(File):
				Self.Gen_Inline_Ids(Markdown_File)
		# Os.system(f'pandoc --section-divs -f markdown-auto_identifiers --metadata title="{Title}" --standalone --template {Htm_Pandoc_File_Name} {Md_Pandoc_File_Name} -o {Output_File_Name}')
		Os.system(f'pandoc -f markdown-auto_identifiers --metadata title="{Title}" --standalone --template {Htm_Pandoc_File_Name} {Md_Pandoc_File_Name} -o {Output_File_Name}')
		Os.unlink(Htm_Pandoc_File_Name)
		Os.unlink(Md_Pandoc_File_Name)
		return 0

	def Info(Self):
		print("Generate Html")

## Type-Option
class Is_A_Option_Class(Dings_Lib.Integer_Option_Class):
	def __init__(Self):
		super().__init__("Is-A", "Number of the Parent-Ding", "DINGS-NUMBER")

	def Verify_Quit(Self):
		if not Dings_Lib.Get_Dings_File(Self.Value):
			print(f'Error: Option "Is_A": Number {Self.Value} does not exist', file=Sys.stderr)
			quit(1)

## Number-Option
class Number_Option_Class(Dings_Lib.Integer_Option_Class):
	def __init__(Self):
		super().__init__("Number", "Number of the Ding", "DINGS-NUMBER")

	def Verify_Quit(Self):
		if Dings_Lib.Get_Dings_File(Self.Value) != None:
			print(f'Error: Option "Number": Number {Self.Value} already exists', file=Sys.stderr)
			quit(1)

## Add-On-File-Option
class Add_On_File_Option_Class(Dings_Lib.String_Option_Class):
	def __init__(Self):
		super().__init__("Add-On-File", "File like Image, Sound, etc.", "FILE-PATH")

	def Verify_Quit(Self):
		if not Self.Set:
			return
		if not Os.path.exists(Self.Value):
			print(f'Error: Option "Add-On-File": File {Self.Value} does not exist', file=Sys.stderr)
			quit(1)

## Command: Dings-Html-Generate
class Dings_New_Command_Class(Dings_Lib.Command_Class):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_new"
		Self.Argument_String = "DINGS-NAME"
		Self.Is_A_Option = Is_A_Option_Class()
		Self.Option_List.append(Self.Is_A_Option)
		Self.Number_Option = Number_Option_Class()
		Self.Option_List.append(Self.Number_Option)
		Self.Add_On_File_Option = Add_On_File_Option_Class()
		Self.Option_List.append(Self.Add_On_File_Option)
	def Verify_Is_A_Option(Self):
		Option = Self.Is_A_Option
		if not Self.Value in Dings_Lib.Dings_File_List:
			print(f'Error: Option "Is-A": Number {Self.Value} does not exist', file=Sys.stderr)
			quit(1)
	def Run(Self):
		if (not Self.Remaining_Argument_List):
			print(f"Error: No Dings-Name specified", file=Sys.stderr)
			return 1
		Dings_Lib.Read_Dings_File_List()
		Self.Is_A_Option.Ensure_Option_Set_Quit()
		Self.Number_Option.Ensure_Option_Set_Quit()
		for Option in Self.Option_List:
			Option.Verify_Quit()
		Is_A_Number = Self.Is_A_Option.Value
		Is_A_Name = Dings_Lib.Get_Dings_File(Is_A_Number).Name
		Dings_Number = Self.Number_Option.Value
		Dings_Name = Self.Remaining_Argument_List[0]
		Contents = ''
		Contents += '# ' + Dings_Name + '\n'
		Contents += '\n'
		Contents += Dings_Name + ' is a [' + Is_A_Name + '](' + str(Is_A_Number) + ').\n'
		if Self.Add_On_File_Option.Set:
			Add_On_File = Self.Add_On_File_Option.Value
			Contents += '\n'
			File_Extension = Dings_Lib.Get_File_Extension(Add_On_File)
			if File_Extension == "jpg":
				Contents += '<img src="' + Add_On_File + '" alt="' + Dings_Name + '" style="width:800px;"/>\n'
			elif File_Extension == "mp3":
				Contents += '<audio controls>\n'
				Contents += '  <source src ="' + Add_On_File + '" type="audio/mpeg">\n'
				Contents += '</audio>\n'
			else:
				print(f"Error: Unsupported File-Extension: {Add_On_File}", file=Sys.stderr)
				return 1
		print(Contents)
		return 0
	def Info(Self):
		print("Create a new Dings-File")

# Entry-Point
def Main():
	Argument_List = Sys.argv.copy()
	Argument_List[0] = "dings"
	Command_List = Dings_Lib.Get_Dict_Sub_Set(globals(), ".*_Command_Class$")
	Dings_Lib.Command_Class.Parse_And_Run("dings", Command_List, Argument_List)

Main()
