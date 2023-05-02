# Dings-Tool-Python
'''

The Dings-Tool-Python is the [Dings-Tool](300020000.md) written in the [Python-Programming-Language](9010003.md).
'''
import Dings
import sys
import typing

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
		Self.Match_Position = -1
		Self.Set = False;

	def Parse(Self, Argument_List):
		Self.Set = False
		for i in range(0, len(Argument_List)):
			Option = Argument_List[i].lower()
			if (Option == '-' + Self.Name[0 : len(Option) - 1]):
				Self.Set = True
				Self.Match_Position = i
				return i

# Help-Option
class Option_Help(Option):
	def __init__(Self):
		super().__init__("Help", "Print Description of Command")

# Test-Option
class Option_Test(Option):
	def __init__(Self):
		super().__init__("Test", "Select Test-Case")

## Command Base-Class
class Command:
	def __init__(Self):
		Self.Name = __class__.__name__[8:].lower()
		Self.Option_Help = Option_Help()
		Self.Option_List = [
			Self.Option_Help,
		]
		Self.Command_List = []

	def Get_Match_List_At_Position(Self, Position):
		Match_List = []
		for Option in Self.Option_List:
			if (Option.Match_Position == Position):
				Match_List.append(Option)
		return Match_List

	def Check_For_Uniqueness(Self, Argument_List):
		Unique = True
		for i in range (0, len(Argument_List)):
			Match_List = Self.Get_Match_List_At_Position(i)
			if (len(Match_List) > 1):
				Unique = False
				print(f"{Self.Command_Name()}: Options not unique: ", file=sys.stderr)
				for Option in Match_List:
					Argument = Argument_List[Option.Match_Position]
					print(f" {Argument}: {Option.Name} ", file=sys.stderr)
		if (not Unique):
			quit(1)

	def Check_For_Invalid_Option(Self, Argument_List):
		Invalid = False
		for i in range (0, len(Argument_List)):
			Match_List = Self.Get_Match_List_At_Position(i)
			if (len(Match_List) == 0):
				print(f"{Self.Command_Name()}: Invalid Option: {Argument_List[i]}", file=sys.stderr)
				Invalid = True
		if (Invalid):
			quit(1)

	def Parse_Commands(Self, Argument_List):
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
			Match_Position = Option.Parse(Argument_List)

		Self.Check_For_Uniqueness(Argument_List)
		Self.Check_For_Invalid_Option(Argument_List)

		if (Self.Option_Help.Set):
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
class Dings(Command):
	def __init__(Self):
		super().__init__()
		Self.Name = __class__.__name__.lower()
	def Run(Self):
		print(f"Run: {Self.Name}")
		quit(0)
	def Info(Self):
		print("Tool for working with Dings")

## Command: Dings-Test
class Dings_Test(Dings):
	def __init__(Self):
		super().__init__()
		Self.Name = __class__.__name__.lower()
	def Run(Self):
		print(f"Run: {Self.Name}")
		quit(0)
	def Info(Self):
		print("Run Test-Cases");

## Command: Dings-Test-List
class Dings_Test_List(Dings_Test):
	def __init__(Self):
		super().__init__()
		Self.Name = __class__.__name__.lower()
		Self.Option_List.append(Option_Test())
	def Run(Self):
		print(f"Run: {Self.Name}")
		quit(0)
	def Info(Self):
		print("List Test-Cases");

## Command: Dings-Test-Run
class Dings_Test_Run(Dings_Test):
	def __init__(Self):
		super().__init__()
		Self.Name = __class__.__name__.lower()
	def Run(Self):
		print(f"Run: {Self.Name}")
		quit(0)
	def Info(Self):
		print("Run Test-Cases");

## Command-List
Command_List = {
	"dings": Dings(),
	"dings_test": Dings_Test(),
	"dings_test_list": Dings_Test_List(),
	"dings_test_run": Dings_Test_Run()
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
	Argument_List = sys.argv.copy()
	Argument_List.pop(0)
	Add_Sub_Commands(Command_List)
	Command = Command_List["dings"].Parse_Commands(Argument_List);
	Command.Parse_Options(Argument_List);
	Command.Run()

Main()
