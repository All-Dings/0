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

### Get Heading String from first Line
Heading_Regex = re.compile(r'^#+\s*(.*)\n$')

## Number-File-List
Number_File_List = []

## Read all Number-Files into a [Linked-List](250000019.md)
def Read_Number_File_List():
	print("Moin")
	### Loop over all Files in the Directory
	for File_Name in os.listdir(Dings_Directory):
		if not File_Name.endswith('.md'):
			continue
		with open(os.path.join(Dings_Directory, File_Name), 'r') as File:
			First_Line = File.readline()
		Name = Heading_Regex.sub(r'\1', First_Line)
		Number = Number_Regex.sub(r'\1', File_Name)

		### Define new [Dictionary](250000018.md) for Number-File
		Number_File = {}
		Number_File['Number'] = Number
		Number_File['Name'] = Name
		### Append Number-File-Dictionary to Number-File-List
		Number_File_List.append(Number_File)

## Print all Number-Files
def Print_Number_File_List():
	for Number_File_Dictionary in Number_File_List:
		print(Number_File_Dictionary)

## Test Number File
def Number_File_List_Test():
	print("Moin")
	Read_Number_File_List()
	Print_Number_File_List()

Number_File_List_Test()
