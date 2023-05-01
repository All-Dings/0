# Dings-Tool-Python
'''

The Dings-Tool-Python is the [Dings-Tool](300020000.md) written in the [Python-Programming-Language](9010003.md).
'''
import Dings
import sys

class Command:
	def __init__(Self):
		Self.State = 1

	def Run(Self, Argument_List):
		raise NotImplementedError()
	def Help(Self, Argument_List):
		raise NotImplementedError()

class Command_Dings(Command):
	def Run(Self, Argument_List):
		print(f"Dings called: {Argument_List}")
		Self.Help()
		quit(0)
	def Info(Self):
		print("The Dings-Tool")
	def Help(Self):
		print(f"Dings [COMMAND]")
		for Command in Command_List.values():
			Command.Info(Command)
		quit(0)

class Command_Dings_Test(Command):
	def Run(Self, Argument_List):
		print(f"Dings Test called: {Argument_List}")
		if (Argument_List[0] != "-h"):
			print(f"Dings Test: Invalid Options: {Argument_List}", file=sys.stderr)
			quit(1)
		Self.Help()
		quit(0)
	def Info(Self):
		print("Test1 ...")
	def Help(Self):
		print(f"Dings [COMMAND]")
		for Command in Command_List.values():
			Command.Info()
		quit(0)

class Command_Dings_Test_Test(Command):
	def Run(Self, Argument_List):
		print(f"Dings Test Test called: {Argument_List}")
		Help()
		quit(0)
	def Info(Self):
		print("Test2 ...")
	def Help(Self):
		print(f"Test -h");
		print(f" -h: Print this Hep")

Command_List = {
	"Dings": Command_Dings,
	"Dings_Test": Command_Dings_Test,
	"Dings_Test_Test": Command_Dings_Test_Test
}

def Parse_Arguments(Argument_List):
	Argument_List.pop(0)
	Command = "Dings"
	while len(Argument_List):
		Argument = Argument_List.pop(0)
		if Argument[0:1] == "-":
			Argument_List.insert(0, Argument)
			break
		else:
			Command = Command + "_" + Argument
	if not Command in Command_List.keys():
		print(f"Dings: Unknown Command: {Command}", file=sys.stderr)
		quit(1)
	Command = Command_List[Command]()
	Command.Run(Argument_List)

Parse_Arguments(sys.argv)
Dings.File_Extension_Reg_Exp_Test()
