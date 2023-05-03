# Dings-Tool-Python
'''

The Dings-Tool-Python is the [Dings-Tool](300020000.md) written in the [Python-Programming-Language](9010003.md).
'''
import Dings as Dings_Lib
from io import StringIO
import contextlib as Context_Lib
import re as Re
import sys as Sys

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

# Test-Option
class Test_Option(String_Option):
	def __init__(Self):
		super().__init__("Test", "Select Test-Case TEST", "TEST")

# Test-Option
class Test_Option_String(String_Option):
	def __init__(Self):
		super().__init__("String-Test", "Test String Option", "STRING")

## Command Base-Class
class Command:
	def __init__(Self):
		Self.Name = __class__.__name__[8:].lower()
		Self.Help_Option = Help_Option()
		Self.Option_List = [
			Self.Help_Option,
		]
		Self.Command_List = []
		Self.Remaining_Argument_List = []

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
				print(f"{Self.Command_Name()}: Options not unique: ", file=Sys.stderr)
				for Option in Match_List:
					Argument = Argument_List[Option.Match[0]]
					print(f" {Argument}: {Option.Name} ", file=Sys.stderr)
		if (not Unique):
			quit(1)

	def Check_For_Invalid_Option(Self, Argument_List):
		Invalid = False
		for i in range (0, len(Argument_List)):
			Match_List = Self.Get_Match_List_At_Position(i)
			if (len(Match_List) == 0 and Argument_List[i][0] == "-"):
				print(f"{Self.Command_Name()}: Invalid Option: {Argument_List[i]}", file=Sys.stderr)
				Invalid = True
			else:
				Self.Remaining_Argument_List.append(Argument_List[i])
		if (Invalid):
			quit(1)

	def Parse_Commands(Self, Argument_List):
		if not Argument_List:
			Self.Help()
		Argument = Argument_List[0]
		for Command_Name, Command in Command_List.items():
			if Command_Name == Self.Name + "_" + Argument:
				Argument_List.pop(0)
				if (len(Argument_List) == 0):
					return Command;
				else:
					return Command.Parse_Commands(Argument_List)
		return Self

	def Parse_Options(Self, Argument_List):
		for Option in Self.Option_List:
			Match = Option.Parse(Self.Command_Name(), Argument_List)

		Self.Check_For_Uniqueness(Argument_List)
		Self.Check_For_Invalid_Option(Argument_List)

		if (Self.Help_Option.Set):
			Self.Help()
		else:
			Self.Run()

	def Run(Self, Argument_List):
		raise NotImplementedError()

	def Command_Name(Self):
		return To_Mixed_Case(Self.Name.replace('_', ' '))

	def Sub_Command_Name(Self, Parent):
		return To_Mixed_Case(Self.Name.removeprefix(Parent + '_'))

	def Help(Self):
		Command_Name = Self.Command_Name()
		print(f"{Command_Name} [COMMAND]")
		print("");
		Self.Info()
		print("");
		print("Options:");
		for Option in Self.Option_List:
			if (Option.Parameter_Name):
				print(f"  -{Option.Name} {Option.Parameter_Name}: {Option.Description}")
			else:
				print(f"  -{Option.Name}: {Option.Description}")
		if len(Self.Command_List) == 0:
			quit(0)
		print("");
		print("Commands:");
		for Command in Self.Command_List:
			Sub_Command_Name = Command.Sub_Command_Name(Self.Name)
			print(f"   {Sub_Command_Name}: ", end='')
			Command.Info()
		quit(0)

## Command: Dings
class Dings_Command(Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings"
	def Run(Self):
		print(f"Run: {Self.Name}")
		quit(0)
	def Info(Self):
		print("Tool for working with Dings")

## Command: Dings-Bash-Completion
class Dings_Completion_Command(Dings_Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_completion"
	def Run(Self):
		print(Self.Remaining_Argument_List)
		quit(0)
	def Info(Self):
		print("Print Bash-Completion List");

## Command: Dings-List
class Dings_List_Command(Dings_Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_list"
	def Run(Self):
		Dings_Lib.Read_Number_File_List()
		Dings_Lib.Print_Number_File_List()
		quit(0)
	def Info(Self):
		print("List Dings");

## Command: Dings-Test
class Dings_Test_Command(Dings_Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_test"
	def Run(Self):
		print(f"Run: {Self.Name}")
		quit(0)
	def Info(Self):
		print("Run Test-Cases");

## Command: Dings-Test-List
class Dings_Test_List_Command(Dings_Test_Command):
	def __init__(Self):
		super().__init__()
		Self.Name = "dings_test_list"
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

## Command-List
Command_List = {
	"dings": Dings_Command(),
	"dings_completion": Dings_Completion_Command(),
	"dings_list": Dings_List_Command(),
	"dings_test": Dings_Test_Command(),
	"dings_test_generate": Dings_Test_Generate_Command(),
	"dings_test_list": Dings_Test_List_Command(),
	"dings_test_run": Dings_Test_Run_Command()
}

## Add Sub-Commands to Commands
def Add_Sub_Commands(Command_List):
	for Command in Command_List.values():
		for Sub_Command in Command_List.values():
			if (Sub_Command.Name.startswith(Command.Name + "_")):
				if not "_" in Sub_Command.Name[len(Command.Name) + 1:]:
					Command.Command_List.append(Sub_Command)

# Entry-Point
def Main():
	Argument_List = Sys.argv.copy()
	Argument_List.pop(0)
	Add_Sub_Commands(Command_List)
	Command = Command_List["dings"].Parse_Commands(Argument_List);
	Command.Parse_Options(Argument_List);
	Command.Run()

Main()
