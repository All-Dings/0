# Dings-Lib-Python

"""
The Dings-Lib-Python is a [Dings-Lib](300010000.md) in [Python](9010003.md).
"""

## Imports

import re
import os

## Directory containing the Markdown files
Dings_Directory = os.getcwd()

## Regular-Expressions

### Dings-Regular-Expressions
Reg_Exp_Number_File = '\d+' + '.' + '\w+'
Reg_Exp_Name_Exact = '(' + '\"|=|\?|\!|\:|\(|\)|#|-|\w|\s|@' + ')' + '+'
Reg_Exp_Name = '(' + '.' + ')' + '+'

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

### Get Name from Reference
Name_from_Reference_Reg_Exp = re.compile('\[' + '(' + Reg_Exp_Name + ')' + '\]' + '\(' + Reg_Exp_Number_File + '\)')

def Name_from_Reference_Reg_Exp_Test():
	Reg_Exp_Test(Name_from_Reference_Reg_Exp, '[Michael-Holzheu](0.md)')

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
	return Number_File

## Read all Number-Files into a [Linked-List](250000019.md)
def Read_Number_File_List():
	### Loop over all Files in the Directory
	for File_Name in os.listdir(Dings_Directory):
		if not Number_Reg_Exp.search(File_Name):
			continue
		Number_File = Read_Number_File(File_Name)
		### Append Number-File-Dictionary to Number-File-List
		Number_File_List[Number_File['Number']] = Number_File

## Print all Number-Files
def Print_Number_File_List():
	Number_File_List_Sorted = list(Number_File_List.values())
	Number_File_List_Sorted = sorted(Number_File_List_Sorted, key=lambda x: x['Number'])
	# Number_File_List_Sorted = Quicksort_List_of_Dictionary(Number_File_List_Sorted, 'Number')
	for Number_File in Number_File_List_Sorted:
		Print_Number_File(Number_File)

## Test Number File
def Number_File_List_Test():
	Read_Number_File_List()
	Print_Number_File_List()

Number_Reg_Exp_Test()
Name_Reg_Exp_Test()
Reference_Reg_Exp_Test()
Name_from_Reference_Reg_Exp_Test()
Number_File_List_Test()
