# Dings-Lib-Python
"""

The Dings-Lib-Python is a [Dings-Lib](300010000.md) in [Python](9010003.md).
"""
## Imports
from enum import Enum
import os as Os
import re as Re
import shutil as Sh_Util
import subprocess as Sub_Process
import sys as Sys
import datetime as Date_Time

## Directory containing the Markdown Files
Dings_Directory = Os.getcwd()

## Blog-Chain-Time
### Get the current Blog-Chain-Time
def Get_Current_Bct():
	Bct_Format = '%Y.%m.%d-%H:%M:%S'
	Time_Now = Date_Time.datetime.now()
	return Time_Now.strftime(Bct_Format)

def Get_Current_Bct_Test():
	print(Get_Current_Bct())

## Regular-Expressions
### Dings-Regular-Expressions
Reg_Exp_Number_File = '\d+' + '\.' + '\w+'
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

# Class Git_Commit_Number_File
class Git_Commit_Number_File_Class:
	def __init__(Self, Commit_Type, Name):
		Self.Commit_Type = Commit_Type
		Self.Name = Name

# Class Git_Commit
class Git_Commit_Class:
	def __init__(Self, Commit_Hash):
		Self.Hash = Commit_Hash
		Self.Time = ""
		Self.Message = ""
		Self.Number_File_List = [];
	def Print(Self):
		print(f"Commit-Hash: {Self.Hash}")
		print(f"       Date: {Self.Time}")
		print(f" Sub-Module: {Self.Sub_Module}")
		print(f"    Message: {Self.Message}")
		for Number_File in Self.Number_File_List:
			print(f"          {Number_File.Commit_Type}: {Number_File.Name}")
		print("")

## Class Git
class Git_Class:
	def __init__(Self):
		Self.Commit_Hash_Reg_Exp = Re.compile('^commit ' + '('  + '[0-9a-fA-F]+' + ')')
		Self.Commit_Time_Reg_Exp = Re.compile('^Date:   ' + '('  + '.*' + ')')
		Self.Number_File_Reg_Exp = Re.compile(Reg_Exp_Number_File)
		Self.Commit_Dict = {}
		Self.Sub_Modules = ["0", "111", "1000001000", "140100000", "1997080300", "2000001", "250000000", "260010000", "400000000", "888"]

	def Read_All(Self):
		for Sub_Module in Self.Sub_Modules:
			print(Sub_Module)
			Os.chdir(Sub_Module)
			Self.Read_Commits(Sub_Module)
			Os.chdir("..")

	def Read_Commits(Self, Sub_Module):
		Lines = Sub_Process.run(['git', 'log', "--date=format:%Y.%m.%d-%H:%M:%S%z", '--name-status'], stdout=Sub_Process.PIPE)
		Lines = Lines.stdout.decode()
		Lines = Lines.split("\n")
		for Line in Lines:
			# print(f"Line: '{Line}'")
			Line = Line.rstrip()
			if not Line:
				continue
			Match = Self.Commit_Hash_Reg_Exp.match(Line)
			if (Match):
				Commit_Hash = Match.group(1)
				# print(Commit_Hash)
				Commit = Git_Commit_Class(Commit_Hash)
				Commit.Sub_Module = Sub_Module
				Self.Commit_Dict[Commit_Hash] = Commit
			Match = Self.Commit_Time_Reg_Exp.match(Line)
			if (Match):
				Commit.Time = Match.group(1)
				# print(f"Time: {Commit.Time}")
			elif (Line[0] == " " and not Line.startswith("    Signed-off-by")):
				Commit.Message = Line[4:]
				# print(f"Message: {Commit.Message}")
			elif (Line.startswith("R100\t")):
				Words = Line.split("\t")
				Match = Self.Number_File_Reg_Exp.match(Words[2])
				if not Match:
					continue
				Commit_Number_File = Git_Commit_Number_File_Class("A", Words[2])
				Commit.Number_File_List.append(Commit_Number_File)
				# print(f"Modify: {Line[2:]}")
			# elif (Line.startswith("D\t")):
			#	Match = Self.Number_File_Reg_Exp.match(Line[2:])
			#	if not Match:
			#		continue
			#	Commit_Number_File = Git_Commit_Number_File_Class("D", Line[2:])
			#	Commit.Number_File_List.append(Commit_Number_File)
			# print(f"Delete: {Line[2:]}")
			elif (Line.startswith("M\t")):
				Match = Self.Number_File_Reg_Exp.match(Line[2:])
				if not Match:
					continue
				Commit_Number_File = Git_Commit_Number_File_Class("M", Line[2:])
				Commit.Number_File_List.append(Commit_Number_File)
				# print(f"Modify: {Line[2:]}")
			elif (Line.startswith("A\t")):
				Match = Self.Number_File_Reg_Exp.match(Line[2:])
				if not Match:
					continue
				Commit_Number_File = Git_Commit_Number_File_Class("A", Line[2:])
				Commit.Number_File_List.append(Commit_Number_File)
				# print(f"Add: {Line[2:]}")

	def Print_Commits(Self):
		Commit_List_Sorted = list(Self.Commit_Dict.values())
		Commit_List_Sorted = sorted(Commit_List_Sorted, key=lambda x: x.Time)
		Number_File_List = {}
		for Commit in Commit_List_Sorted:
			Commit.Print()

	def Fix_Commits(Self):
		Commit_List_Sorted = list(Self.Commit_Dict.values())
		Commit_List_Sorted = sorted(Commit_List_Sorted, key=lambda x: x.Time)
		Number_File_List = {}
		for Commit in Commit_List_Sorted:
			for Number_File in Commit.Number_File_List:
				if Number_File.Commit_Type == "A":
					if Number_File.Name in Number_File_List:
						print(f"Error: {Number_File.Name} already there")
						print("Old:")
						Number_File_List[Number_File.Name].Print()
						print("New:")
						Commit.Print()
						Number_File.Commit_Type = "M"
					else:
						Number_File_List[Number_File.Name] = Commit
				if Number_File.Commit_Type == "D":
					if not Number_File_List[Number_File.Name]:
						print(f"Error: {Number_File.Name} not there")
						Commit.Print()
						quit(1)
					del Number_File_List[Number_File.Name]

	def Write_Commits(Self):
		Commit_Number = 10000000000
		Commit_List_Sorted = list(Self.Commit_Dict.values())
		Commit_List_Sorted = sorted(Commit_List_Sorted, key=lambda x: x.Time)
		for Commit in Commit_List_Sorted:
			Os.system("mkdir -p " + "Commits/" + str(Commit_Number))
			print(f"Commit: {Commit.Hash} {Commit.Time} {Commit.Message}")
			if Commit_Number != 10000000000:
				Last_Commit_Dir = "Commits/" + str(Commit_Number - 1)
				This_Commit_Dir = "Commits/" + str(Commit_Number)
				for File_Name in Os.listdir(Last_Commit_Dir):
					Os.link(Last_Commit_Dir + "/" + File_Name, This_Commit_Dir + "/" + File_Name)
					# Sh_Util.copy(Last_Commit_Dir + "/" + File_Name, This_Commit_Dir + "/" + File_Name)
			Os.chdir(Commit.Sub_Module)
			for Number_File in Commit.Number_File_List:
				Target_File = "../Commits/" + str(Commit_Number) + "/" + Number_File.Name
				if Os.path.isfile(Target_File):
					Os.unlink(Target_File)
				Os.system("git show " + Commit.Hash + ":" + Number_File.Name + ">" + Target_File)
			Os.chdir("..")
			Commit_Number = Commit_Number + 1


## Test Git_Class
def Git_Class_Test():
	Git = Git_Class()
	Git.Read_All()
#	Git.Read_Commits("0")
	Git.Print_Commits()
	print("Fixing Problems")
	Git.Fix_Commits()
	print("Now it should work")
	Git.Fix_Commits()
	Git.Write_Commits()
	quit(1)

## Class Number-File
class Number_File_Class:
	def __init__(Self, Number, Name):
		Self.Name = Name
		Self.Number = Number
		Self.Source_References = []
		Self.Target_References = []
		Self.Meta_Data = {}

	## Print Number-File
	def Print(Self):
		print(f'{Self.Number} "{Self.Name}"')
		for Reference in Self.Target_References:
			Number_File = Reference['Source']
			print(f"  - {Reference['Name']} [{Number_File.Name}]({Number_File.Number})")

## Print Number-File-Targets
def Print_Number_File_Targets(Number):
	Number_File = Number_File_List[Number]
	for Reference in Number_File.Source_References:
		Number_File = Reference['Target']
		print(f"{Reference['Name']} [{Number_File.Name}]({Number_File.Number})")

## Read Data of a Number-File
def Read_Number_File(File_Name):
	with open(Os.path.join(Dings_Directory, File_Name), 'r') as File:
		First_Line = File.readline()
	Name = Name_Reg_Exp.match(First_Line).group(1)
	Number = Number_Reg_Exp.match(File_Name).group(1)

	### Define new [Dictionary](250000018.md) for Number-File
	Number_File = Number_File_Class(int(Number), Name.strip())
	return Number_File

## Read References of a Number-File
def Read_Number_File_References(File_Name):
	State = "Init"
	Meta_Data_Reg_Exp = Re.compile('^' + '## Meta-Data')
	Meta_Data_Entry_Reg_Exp = Re.compile('^' + '- ' + '(' + '\w+' + ')' + ":" + "\s+" + "(" + ".*" + ")")
	Source_Number = Number_Reg_Exp.match(File_Name).group(1)
	Source = Number_File_List[int(Source_Number)]
	with open(Os.path.join(Dings_Directory, File_Name), 'r') as File:
		Lines = File.readlines()
	for Line in Lines:
		if State == "Init":
			Match = Meta_Data_Reg_Exp.search(Line)
			if Match:
				print("Meta")
				State = "Meta-Data"
				continue
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
			Source.Source_References.append(Reference)
			Target.Target_References.append(Reference)
		elif State == "Meta-Data":
			if Line.strip() == "":
				continue
			Match = Meta_Data_Entry_Reg_Exp.search(Line)
			if (Match):
				Entry_Name = Match.group(1)
				Entry_Value = Match.group(2)
				if Entry_Name not in Source.Meta_Data:
					Source.Meta_Data[Entry_Name] = []
				Source.Meta_Data[Entry_Name].append(Entry_Value)
				print(f"Mata-Data-Entry: {Source.Number}: {Entry_Name}: {Entry_Value}")

## Read all Number-Files into a [Linked-List](250000019.md)
def Read_Number_File_List():
	### Loop over all Files in the Directory
	for File_Name in Os.listdir(Dings_Directory):
		if not Number_Reg_Exp.search(File_Name):
			continue
		Number_File = Read_Number_File(File_Name)
		#### Append Number-File-Dictionary to Number-File-List
		Number_File_List[Number_File.Number] = Number_File
	for File_Name in Os.listdir(Dings_Directory):
		if not Number_Reg_Exp.search(File_Name):
			continue
		Read_Number_File_References(File_Name)

## Print all Number-Files
def Print_Number_File_List():
	Number_File_List_Sorted = list(Number_File_List.values())
	Number_File_List_Sorted = sorted(Number_File_List_Sorted, key=lambda x: x.Number)
	for Number_File in Number_File_List_Sorted:
		Number_File.Print()

# Base-Class Code-To-Markdown
class Code_To_Markdown_Class:
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

## Convert Python-Code to Markdown
class Python_To_Markdown_Class(Code_To_Markdown_Class):
	def __init__(Self):
		Self.Reg_Exp_Heading = Re.compile('^' + '#+' + ' ' + '.*')
		Self.Reg_Exp_Comment = Re.compile('^' + '"""' + '\s*')
		super().__init__()

	def Handle_State_Init(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			Self.State = Self.States.Heading
			print(f"{Line}")
		elif Self.Reg_Exp_Comment.match(Line):
			Self.State = Self.States.Comment
		else:
			print(f"```python")
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Heading(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			print(f"\n{Line}")
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
			print(f"\n{Line}")
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

## Convert Perl-Code to Markdown
class Perl_To_Markdown_Class(Code_To_Markdown_Class):
	def __init__(Self):
		Self.Reg_Exp_Heading = Re.compile('^' + '#+' + ' ' + '.*')
		Self.Reg_Exp_Comment_Start = Re.compile('^' + '=for comment' + '\s*')
		Self.Reg_Exp_Comment_End = Re.compile('^' + '=cut' + '\s*')
		super().__init__()

	def Handle_State_Init(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			Self.State = Self.States.Heading
			print(f"{Line}")
		elif Self.Reg_Exp_Comment_Start.match(Line):
			Self.State = Self.States.Comment
		else:
			print(f"```perl")
			print(Line)
			Self.State = Self.States.Code

	def Handle_State_Heading(Self, Line):
		if Self.Reg_Exp_Heading.match(Line):
			print(f"\n{Line}")
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
			print(f"\n{Line}")
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
class Css_To_Markdown_Class(Code_To_Markdown_Class):
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
			print(f"{Match.group(1)}")
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
			print(f"\n{Match.group(1)}")
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
			print(f"\n{Match.group(1)}")
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
		To_Markdown = Python_To_Markdown_Class()
	elif File_Extension == "pl":
		To_Markdown = Perl_To_Markdown_Class()
	elif File_Extension == "css":
		To_Markdown = Css_To_Markdown_Class()
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
class Option_Class:
	def __init__(Self, Name, Description):
		Self.Name = Name.lower()
		Self.Description = Description
		Self.Parameter_Name = ""
		Self.Match = [-1,-1]
		Self.Set = False;

# Single-Option without Parameters
class Single_Option_Class(Option_Class):
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
class String_Option_Class(Option_Class):
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
class Help_Option_Class(Single_Option_Class):
	def __init__(Self):
		super().__init__("Help", "Print Description of Command")

## Command Base-Class
class Command_Class:
	Command_List = {}
	Command_Name = ""

	def __init__(Self):
		Self.Help_Option = Help_Option_Class()
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
			quit(Command.Run())

	## Run Sub-Command
	@classmethod
	def Run_Command(Class, Command_Name, Argument_List):
		Class.Command_List["dings_" + Command_Name].Remaining_Argument_List = Argument_List
		Class.Command_List["dings_" + Command_Name].Run()

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

