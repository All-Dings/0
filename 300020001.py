# Dings-Tool-Python
'''

The Dings-Tool-Python is the [Dings-Tool](300020000.md) written in the [Python-Programming-Language](9010003.md).
'''
import Dings as Dings_Lib
from io import StringIO
import contextlib as Context_Lib
import re as Re
import sys as Sys

# Test-Option
class Test_Option(Dings_Lib.String_Option):
	def __init__(Self):
		super().__init__("Test", "Select Test-Case TEST", "TEST")

# Test-Option
class Test_Option_String(Dings_Lib.String_Option):
	def __init__(Self):
		super().__init__("String-Test", "Test String Option", "STRING")

# Pos-Option
class Pos_Option_String(Dings_Lib.String_Option):
	def __init__(Self):
		super().__init__("Position", "Position in String", "POSITION")

## Command: Dings
class Dings_Command(Dings_Lib.Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings"
		Self.Help_On_Empty = True
	def Run(Self):
		quit(0)
	def Info(Self):
		print("Tool for working with Dings.");

## Command: Dings-Bash-Completion
class Dings_Completion_Command(Dings_Lib.Command):
	def __init__(Self):
		super().__init__()
		Self.Help_On_Empty = False
		Self.Name = "dings_completion"
		Self.Pos_Opt = Pos_Option_String()
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
		for Command in Dings_Command.Command_List.values():
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
		quit(0)
	def Info(Self):
		print("Print Bash-Completion List");

## Command: Dings-List
class Dings_List_Command(Dings_Lib.Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_list"
		Self.Help_On_Empty = False
	def Run(Self):
		Dings_Lib.Read_Number_File_List()
		Dings_Lib.Print_Number_File_List()
		quit(0)
	def Info(Self):
		print("List Dings");

## Command: Dings-Test
class Dings_Test_Command(Dings_Lib.Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_test"
		Self.Help_On_Empty = True
	def Run(Self):
		quit(0)
	def Info(Self):
		print("Run Test-Cases");

## Command: Dings-Test-List
class Dings_Test_List_Command(Dings_Test_Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_test_list"
		Self.Help_On_Empty = False
		Self.Option_List.append(Test_Option())
	def Run(Self):
		Test_List = Dings_Lib.Get_Test_List()
		for Test_Name in Test_List:
			print(Test_Name)
		quit(0)
	def Info(Self):
		print("List Test-Cases");

## Command: Dings-Test-Generate
class Dings_Test_Generate_Command(Dings_Test_Command):
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
		quit(0)
	def Info(Self):
		print("Run Test-Cases");

## Command: Dings-Test-Run
class Dings_Test_Run_Command(Dings_Test_Command):
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
		quit(0)
	def Info(Self):
		print("Run Test-Cases");

# Entry-Point
def Main():
	Argument_List = Sys.argv.copy()
	Argument_List[0] = "dings"
	Command_List = Dings_Lib.Get_Dict_Sub_Set(globals(), ".*_Command$")
	Dings_Lib.Command.Parse_And_Run("dings", Command_List, Argument_List)

Main()
