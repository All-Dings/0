# Dings-Lib-Python
"""

The Dings-Lib-Python is a [Dings-Lib](300010000.md) in [Python](9010003.md).
"""
## Imports
from enum import Enum
import os as Os
import re as Re
import sys as Sys
import datetime

## Directory containing the Markdown Files
Dings_Directory = Os.getcwd()

## Blog-Chain-Time
### Get the current Blog-Chain-Time
def Get_Current_Bct():
	Bct_Format = '%Y.%m.%d-%H:%M:%S'
	Time_Now = datetime.datetime.now()
	return Time_Now.strftime(Bct_Format)

def Get_Current_Bct_Test():
	print(Get_Current_Bct())

## Regular-Expressions
### Dings-Regular-Expressions
Reg_Exp_Number_File = '\d+' + '.' + '\w+'
Reg_Exp_Name = '(?:' + '\"|=|\?|\!|\:|\(|\)|#|-|\w|\s|@|\'' + ')' + '+'

### Apply [Reg_Exp](9000103.md) to [Line](700011.md) and print the [Match](404.md)
def Test_Reg_Exp(Reg_Exp, Line):
	Match = Reg_Exp.search(Line).group(1)
	print(f'"{Line}" -> "{Match}"')

### Get File-Extension
File_Extension_Reg_Exp = Re.compile('.+' + '\.' + '(' + '[a-zA-Z]+' + ')' + '$')

def File_Extension_Reg_Exp_Test():
	Test_Reg_Exp(File_Extension_Reg_Exp, 'test.pl')
	Test_Reg_Exp(File_Extension_Reg_Exp, 'test.py')


def Get_File_Extension(File_Path):
	Match = File_Extension_Reg_Exp.search(File_Path)
	if not Match:
		return ""
	else:
		return Match.group(1)

### Get Dings-Name from First-Line
Name_Reg_Exp = Re.compile('^' + '#' + ' ' + '(' + Reg_Exp_Name + ')' + '\s*' + '$')

def Name_Reg_Exp_Test():
	Test_Reg_Exp(Name_Reg_Exp, '# Michael-Holzheu')
	Test_Reg_Exp(Name_Reg_Exp, '# Michael Holzheu')
	Test_Reg_Exp(Name_Reg_Exp, '# Michael-Holzheu-Neu')
	Test_Reg_Exp(Name_Reg_Exp, '# michael-holzheu@Git-Hub')
	Test_Reg_Exp(Name_Reg_Exp, '# Michael_Holzheu-Neu')
	Test_Reg_Exp(Name_Reg_Exp, '# Brașov')
	Test_Reg_Exp(Name_Reg_Exp, '# Douglas_Noël_Adams')

### Get Number from Number-File
Number_Reg_Exp = Re.compile('^' + '(' + '\d+' + ')' + '.md' + '$')

def Number_Reg_Exp_Test():
	Test_Reg_Exp(Number_Reg_Exp, '0.md')
	Test_Reg_Exp(Number_Reg_Exp, '341324.md')

### Get Reference from Line
Reference_Reg_Exp = Re.compile('(' + '\[' + Reg_Exp_Name + '\]' + '\(' + Reg_Exp_Number_File + '\)' + ')')

def Reference_Reg_Exp_Test():
	Test_Reg_Exp(Reference_Reg_Exp, 'The Man [Michael-Holzheu](0.md) creates the Dings-Project.')
	Test_Reg_Exp(Reference_Reg_Exp, '[Michael-Holzheu](0.md) builds Dings-Project.')
	Test_Reg_Exp(Reference_Reg_Exp, 'The Digns-Prject is created by [Michael-Holzheu](0.md)')
	Test_Reg_Exp(Reference_Reg_Exp, 'Height is a [Dimension-Interval](10000021.md) for the [Altitude-Dimension](10000030.md).')

### Get Name from Reference
Name_From_Reference_Reg_Exp = Re.compile('\[' + '(' + Reg_Exp_Name + ')' + '\]' + '\(' + Reg_Exp_Number_File + '\)')

def Name_From_Reference_Reg_Exp_Test():
	Test_Reg_Exp(Name_From_Reference_Reg_Exp, '[Michael-Holzheu](0.md)')

### Get Number from Reference
Number_From_Reference_Reg_Exp = Re.compile('\[' + Reg_Exp_Name + '\]' + '\(' + '(' + '\d+' + ')' + '.' + '\w+' + '\)')

def Number_From_Reference_Reg_Exp_Test():
	Test_Reg_Exp(Number_From_Reference_Reg_Exp, '[Michael-Holzheu](0.md)')

## Number-File-List
Number_File_List = {}

## Quick-Sort for List of Dictionary
def Quicksort_List_of_Dictionary(List, Key):
	Element_Count = len(List)
	if Element_Count <= 1:
		return List
	Pivot = List[Element_Count // 2][Key]
	Left = [Element for Element in List if Element[Key] < Pivot]
	Middle = [Element for Element in List if Element[Key] == Pivot]
	Right = [Element for Element in List if Element[Key] > Pivot]
	return Quicksort_List_of_Dictionary(Left, Key) + Middle + Quicksort_List_of_Dictionary(Right, Key)

## Print Number-File
def Print_Number_File(Number_File):
	Name = Number_File['Name']
	Number = Number_File['Number']
	print(f'{Number} "{Name}"')
	for Reference in Number_File['Target_References']:
		Source = Reference['Source']
		print(f"  - {Reference['Name']} [{Source['Name']}]({Source['Number']})")

## Read Data of a Number-File
def Read_Number_File(File_Name):
	with open(Os.path.join(Dings_Directory, File_Name), 'r') as File:
		First_Line = File.readline()
	Name = Name_Reg_Exp.match(First_Line).group(1)
	Number = Number_Reg_Exp.match(File_Name).group(1)

	### Define new [Dictionary](250000018.md) for Number-File
	Number_File = {}
	Number_File['Number'] = int(Number)
	Number_File['Name'] = Name.strip()
	Number_File['Source_References'] = []
	Number_File['Target_References'] = []
	return Number_File

## Read References of a Number-File
def Read_Number_File_References(File_Name):
	Source_Number = Number_Reg_Exp.match(File_Name).group(1)
	Source = Number_File_List[int(Source_Number)]
	with open(Os.path.join(Dings_Directory, File_Name), 'r') as File:
		Lines = File.readlines()
	for Line in Lines:
		Match = Reference_Reg_Exp.search(Line)
		if not Match:
			continue
		Reference = Match.group(1)
		Target_Number = Number_From_Reference_Reg_Exp.search(Reference).group(1)
		Target_Name = Name_From_Reference_Reg_Exp.search(Reference).group(1)

		if not int(Source_Number) in Number_File_List:
			print(f"Source-Number {Source_Number} not found.", file=Sys.stderr)
			continue
		if not int(Target_Number) in Number_File_List:
			print(f"Target-Number {Target_Number} not found.", file=Sys.stderr)
			continue
		Target = Number_File_List[int(Target_Number)]
		Reference = {}
		Reference['Source'] = Source
		Reference['Target'] = Target
		Reference['Name'] = Target_Name
		Source['Source_References'].append(Reference)
		Target['Target_References'].append(Reference)

## Read all Number-Files into a [Linked-List](250000019.md)
def Read_Number_File_List():
	### Loop over all Files in the Directory
	for File_Name in Os.listdir(Dings_Directory):
		if not Number_Reg_Exp.search(File_Name):
			continue
		Number_File = Read_Number_File(File_Name)
		#### Append Number-File-Dictionary to Number-File-List
		Number_File_List[Number_File['Number']] = Number_File
	for File_Name in Os.listdir(Dings_Directory):
		if not Number_Reg_Exp.search(File_Name):
			continue
		Read_Number_File_References(File_Name)

## Print all Number-Files
def Print_Number_File_List():
	Number_File_List_Sorted = list(Number_File_List.values())
	Number_File_List_Sorted = sorted(Number_File_List_Sorted, key=lambda x: x['Number'])
	for Number_File in Number_File_List_Sorted:
		Print_Number_File(Number_File)

## Base-Class Code-To-Markdown
class Code_To_Markdown:
	def __init__(Self):
		Self.States = Enum('States', ['Init', 'Heading', 'Comment', 'Code'])
		Self.State = Self.States.Init

	def Process_End(Self):
		if Self.State == Self.States.Code:
			print("```")
		print("")
		print("```")
		print(f"Auto-Generated: {Get_Current_Bct()}")
		print("```")

	def Process_Line(Self, Line, Line_Number):
		Line = Line.rstrip()
		if Self.State == Self.States.Init:
			Self.Handle_State_Init(Line)
		elif Self.State == Self.States.Heading:
			Self.Handle_State_Heading(Line)
		elif Self.State == Self.States.Code:
			Self.Handle_State_Code(Line)
		elif Self.State == Self.State.Comment:
			Self.Handle_State_Comment(Line)
		return Self.State

	def Handle_State_Init(Self, Line):
		raise NotImplementedError()
	def Handle_State_Heading(Self, Line):
		raise NotImplementedError()
	def Handle_State_Code(Self, Line):
		raise NotImplementedError()
	def Handle_State_Comment(Self, Line):
		raise NotImplementedError()

	## Convert a Language-File into a Markdown-File
	def Convert(Self, File_Path):
		Line_Number = 1
		with open(File_Path, 'r') as File:
			Lines = File.readlines()
		for Line in Lines:
			Self.Process_Line(Line, Line_Number)
			Line_Number = Line_Number + 1
		Self.Process_End()

# Convert Python-Code ot Markdown
class Python_To_Markdown(Code_To_Markdown):
	def __init__(Self):
		Self.Reg_Exp_Heading = Re.compile('^' + '#+' + ' ' + '.*')
		Self.Reg_Exp_Comment = Re.compile('^' + '"""' + '\s*')
		super().__init__()

	def Handle_State_Init(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			Self.State = Self.States.Heading
			print(Line)
		elif Self.Reg_Exp_Comment.match(Line):
			Self.State = Self.States.Comment
		else:
			print(f"```python")
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Heading(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			print(Line)
			Self.State = Self.States.Heading
		elif Self.Reg_Exp_Comment.match(Line):
			Self.State = Self.State.Comment
		else:
			print(f"```python")
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Code(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			print("```")
			print(Line)
			Self.State = Self.States.Heading
		elif Self.Reg_Exp_Comment.match(Line):
			print("```")
			Self.State = Self.States.Comment
		else:
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Comment(Self, Line):
		if Self.Reg_Exp_Comment.match(Line):
			Self.State = Self.States.Init
		else:
			print(Line)

# Convert Perl-Code to Markdown
class Perl_To_Markdown(Code_To_Markdown):
	def __init__(Self):
		Self.Reg_Exp_Heading = Re.compile('^' + '#+' + ' ' + '.*')
		Self.Reg_Exp_Comment_Start = Re.compile('^' + '=for comment' + '\s*')
		Self.Reg_Exp_Comment_End = Re.compile('^' + '=cut' + '\s*')
		super().__init__()

	def Handle_State_Init(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			Self.State = Self.States.Heading
			print(Line)
		elif Self.Reg_Exp_Comment_Start.match(Line):
			Self.State = Self.States.Comment
		else:
			print(f"```perl")
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Heading(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			print(Line)
			Self.State = Self.States.Heading
		elif Self.Reg_Exp_Comment_Start.match(Line):
			Self.State = Self.State.Comment
		else:
			print(f"```perl")
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Code(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			print("```")
			print(Line)
			Self.State = Self.States.Heading
		elif Self.Reg_Exp_Comment_Start.match(Line):
			print("```")
			Self.State = Self.States.Comment
		else:
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Comment(Self, Line):
		if Self.Reg_Exp_Comment_End.match(Line):
			Self.State = Self.States.Init
		else:
			print(Line)

# Convert Css-Code to Markdown
class Css_To_Markdown(Code_To_Markdown):
	def __init__(Self):
		Self.Reg_Exp_Heading = Re.compile('^' + ' \* ' + '\s+' + '(' + '#+' + ' ' + '.*' + ')')
		Self.Reg_Exp_Comment_One_Line = Re.compile('^' + '/' + '\*' + '\s+' +'(' + '.*' + ')' + '\*' + '/' + '\s*')
		Self.Reg_Exp_Comment_Start = Re.compile('^' + '/' + '\*' + '\s*')
		Self.Reg_Exp_Comment_End = Re.compile('^' + '\*' + '/' + '\s*')
		super().__init__()

	def Handle_State_Init(Self, Line):
		Match = Self.Reg_Exp_Heading.match(Line)
		if Match:
			Self.State = Self.States.Heading
			print(Match.group(1))
			return
		Match = Self.Reg_Exp_Comment_One_Line.match(Line)
		if Match:
			Self.State = Self.States.Init
			print(Match.group(1))
			return
		Match = Self.Reg_Exp_Comment_Start.match(Line)
		if Match:
			Self.State = Self.States.Comment
			return
		print(f"```css")
		print(Line)
		Self.State = Self.States.Code

	def Handle_State_Heading(Self, Line):
		Match = Self.Reg_Exp_Heading.match(Line)
		if Match:
			Self.State = Self.States.Heading
			print(Match.group(1))
			return
		Match = Self.Reg_Exp_Comment_One_Line.match(Line)
		if Match:
			Self.State = Self.States.Init
			print(Match.group(1))
			return
		Match = Self.Reg_Exp_Comment_Start.match(Line)
		if Match:
			Self.State = Self.State.Comment
			return
		print(f"```css")
		print(Line)
		Self.State = Self.States.Code

	def Handle_State_Code(Self, Line):
		Match = Self.Reg_Exp_Heading.match(Line)
		if Match:
			Self.State = Self.States.Heading
			print("```")
			print(Match.group(1))
			return
		Match = Self.Reg_Exp_Comment_One_Line.match(Line)
		if Match:
			Self.State = Self.States.Init
			print("```")
			print(Match.group(1))
			return
		Match = Self.Reg_Exp_Comment_Start.match(Line)
		if Match:
			print("```")
			Self.State = Self.States.Comment
			return
		print(Line)
		Self.State = Self.States.Code

	def Handle_State_Comment(Self, Line):
		Match = Self.Reg_Exp_Comment_End.match(Line)
		if Match:
			Self.State = Self.States.Init
			return
		print(Line)

# Convert Code-File to Markdown
def Language_To_Markdown(File_Path):
	File_Extension = Get_File_Extension(File_Path)
	if File_Extension == "py":
		To_Markdown = Python_To_Markdown()
	elif File_Extension == "pl":
		To_Markdown = Perl_To_Markdown()
	elif File_Extension == "css":
		To_Markdown = Css_To_Markdown()
	else:
		print(f"File-Type not supported: {File_Path}", file=Sys.stderr)
		quit()
	To_Markdown.Convert(File_Path)

# Test Language-To-Markdown Functions
def Language_To_Markdown_Test():
	File_Path = Os.path.join(Dings_Directory, "300010010.py")
	Language_To_Markdown(File_Path)
	File_Path = Os.path.join(Dings_Directory, "300010011.pl")
	Language_To_Markdown(File_Path)
	File_Path = Os.path.join(Dings_Directory, "300000014.css")
	Language_To_Markdown(File_Path)

## Test Number File
def Number_File_List_Test():
	Read_Number_File_List()
	Print_Number_File_List()

## Generate Test-Output-File_Name from File_Name
def Test_Output_File_Name(File_Name):
	return File_Name + ".Dings-Test"

## Return Sub-Set of String_Dict with all Elements where Reg_Exp applies
def Get_Dict_Sub_Set(String_Dict, Reg_Exp):
	Reg_Exp_Comp = Re.compile(Reg_Exp)
	New_Dict = {}
	for Key, Value in String_Dict.items():
		if (Reg_Exp_Comp.match(Key)):
			New_Dict[Key] = Value
	return New_Dict

## Get Test_List
def Get_Test_List():
	return Get_Dict_Sub_Set(globals(), ".*_Test");

# Convert Combined-String to Mixed-Case
def To_Mixed_Case(String):
	Separator_Character_List = ['-', '_', ' ']
	for i in range(len(String) - 1, 0, -1):
		if (String[i] in Separator_Character_List):
			String = String[0 : i + 1] + String[i + 1].upper() + String[i + 2:]
	String = String[0].upper() + String[1:]
	return String

def To_Mixed_Case_Test():
	In = "dings_test_list"
	Out = To_Mixed_Case(In)
	print(In + " -> " + Out)

	In = "dings-test-list"
	Out = To_Mixed_Case(In)
	print(In + " -> " + Out)

	In = "dings_test-list"
	Out = To_Mixed_Case(In)
	print(In + " -> " + Out)

	In = "dings test"
	Out = To_Mixed_Case(In)
	print(In + " -> " + Out)

	In = "dings-test"
	Out = To_Mixed_Case(In)
	print(In + " -> " + Out)

# Option Base-Class
class Option:
	def __init__(Self, Name, Description):
		Self.Name = Name.lower()
		Self.Description = Description
		Self.Parameter_Name = ""
		Self.Match = [-1,-1]
		Self.Set = False;

# Single-Option without Parameters
class Single_Option(Option):
	def __init__(Self, Name, Description):
		super().__init__(Name, Description)
	def Parse(Self, Command_Name, Argument_List):
		Self.Set = False
		for i in range(0, len(Argument_List)):
			Option = Argument_List[i].lower()
			if (Option == '-' + Self.Name[0 : len(Option) - 1]):
				Self.Set = True
				Self.Match = [i, i]
				return Self.Match

# String-Option
class String_Option(Option):
	def __init__(Self, Name, Description, Parameter_Name):
		super().__init__(Name, Description)
		Self.Value = ""
		Self.Parameter_Name = Parameter_Name

	def Parse(Self, Command_Name, Argument_List):
		Self.Set = False
		for i in range(0, len(Argument_List)):
			Argument = Argument_List[i]
			if (Argument.lower() == '-' + Self.Name[0 : len(Argument) - 1]):
				if i == len(Argument_List) - 1:
					print(f"{Command_Name}: Option -{Self.Name} requires a Value ", file=Sys.stderr)
					quit(1)
				Self.Set = True
				Self.Value = Argument_List[i + 1]
				Self.Match = [i, i + 1]
				return Self.Match

# Help-Option
class Help_Option(Single_Option):
	def __init__(Self):
		super().__init__("Help", "Print Description of Command")

## Command Base-Class
class Command:
	Command_List = {}
	Command_Name = ""

	def __init__(Self):
		Self.Help_Option = Help_Option()
		Self.Option_List = [
			Self.Help_Option,
		]
		Self.Sub_Command_List = []
		Self.Remaining_Argument_List = []
		Self.Help_On_Empty = False
		Self.Argument_String = "[COMMAND]"

	## Initialize all Commands and add Sub-Commands
	@classmethod
	def Parse_And_Run(Class, Command_Name, Command_List, Argument_List):
		Class.Command_List = {}
		Class.Command_Name = Command_Name

		## Create Object-Instances
		for Command_Name, Command_Class in Command_List.items():
			Command_Object = Command_Class()
			Class.Command_List[Command_Object.Name] = Command_Object

		## Add Sub-Commands
		for Command in Class.Command_List.values():
			for Sub_Command in Class.Command_List.values():
				if (not Sub_Command.Name.startswith(Command.Name + "_")):
					continue
				if not "_" in Sub_Command.Name[len(Command.Name) + 1:]:
					Command.Sub_Command_List.append(Sub_Command)

		# Parse Arguments and find Sub-Command "Command"
		Matches = 0
		Command_Name = ""
		for Argument in Argument_List:
			if not Command_Name:
				Command_Name = Argument.lower()
			else:
				Command_Name = Command_Name + "_" + Argument.lower()
			if Command_Name in Command.Command_List:
				Command = Command.Command_List[Command_Name]
				Matches = Matches + 1
		Argument_List = Argument_List[Matches:]

		# Parse Options
		for Option in Command.Option_List:
			Match = Option.Parse(Command.Name, Argument_List)

		Command.Check_For_Uniqueness(Argument_List)
		Command.Check_For_Invalid_Option(Argument_List)

		if (Command.Help_Option.Set):
			Command.Help()
		elif (Command.Help_On_Empty and not Command.Remaining_Argument_List):
			Command.Help()
		else:
			Command.Run()

	def Get_Match_List_At_Position(Self, Position):
		Match_List = []
		for Option in Self.Option_List:
			if (Option.Match[0] == Position or Option.Match[1] == Position):
				Match_List.append(Option)
		return Match_List

	def Check_For_Uniqueness(Self, Argument_List):
		Unique = True
		for i in range (0, len(Argument_List)):
			Match_List = Self.Get_Match_List_At_Position(i)
			if (len(Match_List) > 1):
				Unique = False
				print(f"{Self.Get_Command_Name()}: Options not unique: ", file=Sys.stderr)
				for Option in Match_List:
					Argument = Argument_List[Option.Match[0]]
					print(f" {Argument}: {Option.Name} ", file=Sys.stderr)
		if (not Unique):
			quit(1)

	def Check_For_Invalid_Option(Self, Argument_List):
		Invalid = False
		for i in range (0, len(Argument_List)):
			Match_List = Self.Get_Match_List_At_Position(i)
			if (len(Match_List) != 0):
				continue
			if Argument_List[i][0] == "-":
				print(f"{Self.Get_Command_Name()}: Invalid Option: {Argument_List[i]}", file=Sys.stderr)
				Invalid = True
			else:
				Self.Remaining_Argument_List.append(Argument_List[i])
		if (Invalid):
			quit(1)

	def Run(Self):
		raise NotImplementedError()

	def Get_Command_Name(Self):
		return To_Mixed_Case(Self.Name.replace('_', ' '))

	def Sub_Command_Name(Self, Parent):
		return To_Mixed_Case(Self.Name.removeprefix(Parent + '_'))

	def Info(Self):
		print(Self.Description)

	def Help(Self):
		Command_Name = Self.Get_Command_Name()
		print(f"{Command_Name} {Self.Argument_String}")
		print("");
		Self.Info()
		print("");
		print("Options:");
		for Option in Self.Option_List:
			if (Option.Parameter_Name):
				print(f"  -{Option.Name} {Option.Parameter_Name}: {Option.Description}")
			else:
				print(f"  -{Option.Name}: {Option.Description}")
		if len(Self.Sub_Command_List) == 0:
			quit(0)
		print("");
		print("Commands:");
		for Command in Self.Sub_Command_List:
			Sub_Command_Name = Command.Sub_Command_Name(Self.Name)
			print(f"   {Sub_Command_Name}: ", end='')
			Command.Info()
		quit(0)

