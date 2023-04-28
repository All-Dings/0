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

### Get Number from Number-File
Number_Regex = re.compile(r'^(\d+).md$')

### Get Name String from first Line
Name_Regex = re.compile(r'^#\s+(.*)$')

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
	Name = Name_Regex.sub(r'\1', First_Line)
	Number = Number_Regex.sub(r'\1', File_Name)

	### Define new [Dictionary](250000018.md) for Number-File
	Number_File = {}
	Number_File['Number'] = int(Number)
	Number_File['Name'] = Name.strip()
	return Number_File

## Read all Number-Files into a [Linked-List](250000019.md)
def Read_Number_File_List():
	### Loop over all Files in the Directory
	for File_Name in os.listdir(Dings_Directory):
		if not Number_Regex.match(File_Name):
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

Number_File_List_Test()
