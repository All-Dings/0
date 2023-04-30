# Dings-Lib-Python

"""
The Dings-Lib-Python is a [Dings-Lib](300010000.md) in [Python](9010003.md).
"""

## Imports

from enum import Enum
import os
import re
import sys

## Directory containing the Markdown Files
Dings_Directory = os.getcwd()

## Regular-Expressions

### Dings-Regular-Expressions
Reg_Exp_Number_File = '\d+' + '.' + '\w+'
Reg_Exp_Name = '(?:' + '\"|=|\?|\!|\:|\(|\)|#|-|\w|\s|@' + ')' + '+'

### Apply [Reg_Exp](9000103.md) to [Line](700011.md) and print the [Match](404.md)
def Reg_Exp_Test(Reg_Exp, Line):
	Match = Reg_Exp.search(Line).group(1)
	print(f'"{Line}" -> "{Match}"')

### Get Dings-Name from First-Line
Name_Reg_Exp = re.compile('^' + '#' + ' ' + '(' + Reg_Exp_Name + ')' + '\s*' + '$')

def Name_Reg_Exp_Test():
	Reg_Exp_Test(Name_Reg_Exp, '# Michael-Holzheu')
	Reg_Exp_Test(Name_Reg_Exp, '# Michael Holzheu')
	Reg_Exp_Test(Name_Reg_Exp, '# Michael-Holzheu-Neu')
	Reg_Exp_Test(Name_Reg_Exp, '# michael-holzheu@Git-Hub')
	Reg_Exp_Test(Name_Reg_Exp, '# Michael_Holzheu-Neu')
	Reg_Exp_Test(Name_Reg_Exp, '# Brașov')

### Get Number from Number-File
Number_Reg_Exp = re.compile('^' + '(' + '\d+' + ')' + '.md' + '$')

def Number_Reg_Exp_Test():
	Reg_Exp_Test(Number_Reg_Exp, '0.md')
	Reg_Exp_Test(Number_Reg_Exp, '341324.md')

### Get Reference from Line
Reference_Reg_Exp = re.compile('(' + '\[' + Reg_Exp_Name + '\]' + '\(' + Reg_Exp_Number_File + '\)' + ')')

def Reference_Reg_Exp_Test():
	Reg_Exp_Test(Reference_Reg_Exp, 'The Man [Michael-Holzheu](0.md) creates the Dings-Project.')
	Reg_Exp_Test(Reference_Reg_Exp, '[Michael-Holzheu](0.md) builds Dings-Project.')
	Reg_Exp_Test(Reference_Reg_Exp, 'The Digns-Prject is created by [Michael-Holzheu](0.md)')
	Reg_Exp_Test(Reference_Reg_Exp, 'Height is a [Dimension-Interval](10000021.md) for the [Altitude-Dimension](10000030.md).')

### Get Name from Reference
Name_From_Reference_Reg_Exp = re.compile('\[' + '(' + Reg_Exp_Name + ')' + '\]' + '\(' + Reg_Exp_Number_File + '\)')

def Name_From_Reference_Reg_Exp_Test():
	Reg_Exp_Test(Name_From_Reference_Reg_Exp, '[Michael-Holzheu](0.md)')

### Get Number from Reference
Number_From_Reference_Reg_Exp = re.compile('\[' + Reg_Exp_Name + '\]' + '\(' + '(' + '\d+' + ')' + '.' + '\w+' + '\)')

def Number_From_Reference_Reg_Exp_Test():
	Reg_Exp_Test(Number_From_Reference_Reg_Exp, '[Michael-Holzheu](0.md)')

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
	with open(os.path.join(Dings_Directory, File_Name), 'r') as File:
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
	with open(os.path.join(Dings_Directory, File_Name), 'r') as File:
		Lines = File.readlines()
	for Line in Lines:
		Match = Reference_Reg_Exp.search(Line)
		if not Match:
			continue
		Reference = Match.group(1)
		Target_Number = Number_From_Reference_Reg_Exp.search(Reference).group(1)
		Target_Name = Name_From_Reference_Reg_Exp.search(Reference).group(1)

		if not int(Source_Number) in Number_File_List:
			print(f"Source-Number {Source_Number} not found.", file=sys.stderr)
			continue
		if not int(Target_Number) in Number_File_List:
			print(f"Target-Number {Target_Number} not found.", file=sys.stderr)
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
	for File_Name in os.listdir(Dings_Directory):
		if not Number_Reg_Exp.search(File_Name):
			continue
		Number_File = Read_Number_File(File_Name)
		#### Append Number-File-Dictionary to Number-File-List
		Number_File_List[Number_File['Number']] = Number_File
	for File_Name in os.listdir(Dings_Directory):
		if not Number_Reg_Exp.search(File_Name):
			continue
		Read_Number_File_References(File_Name)

## Print all Number-Files
def Print_Number_File_List():
	Number_File_List_Sorted = list(Number_File_List.values())
	Number_File_List_Sorted = sorted(Number_File_List_Sorted, key=lambda x: x['Number'])
	for Number_File in Number_File_List_Sorted:
		Print_Number_File(Number_File)

## Class Code-To-Markdown
class Code_To_Markdown:
	class State(Enum):
		Init = 1
		Code = 2
		Comment = 3
		Heading = 4

	def __init__(Self):
		Self.State = Code_To_Markdown.State.Init
		Self.Reg_Exp_Heading = re.compile('^' + '#+' + ' ' + '.*')
		Self.Reg_Exp_Comment = re.compile('^' + '"""' + '\s*')

	def Process_End(Self):
		if Self.State == Code_To_Markdown.State.Code:
			print("```")

	def Process_Line(Self, Line, Line_Number):
		Line = Line.rstrip()
		if len(Line) == 0:
			pass
		elif Self.State == Code_To_Markdown.State.Init:
			if Self.Reg_Exp_Heading.match(Line):
				Self.State = Code_To_Markdown.State.Heading
				print(Line)
			elif Self.Reg_Exp_Comment.match(Line):
				Self.State = Code_To_Markdown.State.Comment
			else:
				print("```python")
				print(Line)
				Self.State = Code_To_Markdown.State.Code
		elif Self.State == Code_To_Markdown.State.Heading:
			if Self.Reg_Exp_Heading.match(Line):
				print(Line)
				Self.State = Code_To_Markdown.State.Heading
			elif Self.Reg_Exp_Comment.match(Line):
				Self.State = Code_To_Markdown.State.Comment
			else:
				print("```python")
				print(Line)
				Self.State = Code_To_Markdown.State.Code
		elif Self.State == Code_To_Markdown.State.Code:
			if Self.Reg_Exp_Heading.match(Line):
				print("```")
				print(Line)
				Self.State = Code_To_Markdown.State.Heading
			elif Self.Reg_Exp_Comment.match(Line):
				print("```")
				Self.State = Code_To_Markdown.State.Comment
			else:
				print(Line)
				Self.State = Code_To_Markdown.State.Code
		elif Self.State == Code_To_Markdown.State.Comment:
			if Self.Reg_Exp_Comment.match(Line):
				Self.State = Code_To_Markdown.State.Init
			else:
				print(Line)
		return Self.State

	## Convert a Python-File into a Markdown-File
	def Convert(Self, File_Path):
		Line_Number = 1
		with open(File_Path, 'r') as File:
			Lines = File.readlines()
		for Line in Lines:
			Self.Process_Line(Line, Line_Number)
		Self.Process_End()

### Test
def Python_To_Markdown_Test():
	To_Markdown = Code_To_Markdown()
	File_Path = os.path.join(Dings_Directory, "300010010.py")
	To_Markdown.Convert(File_Path)

## Test Number File
def Number_File_List_Test():
	Read_Number_File_List()
	Print_Number_File_List()

Python_To_Markdown_Test()
Number_From_Reference_Reg_Exp_Test()
Name_From_Reference_Reg_Exp_Test()
Number_Reg_Exp_Test()
Name_Reg_Exp_Test()
Reference_Reg_Exp_Test()
Name_From_Reference_Reg_Exp_Test()
Read_Number_File_List()
Print_Number_File_List()
