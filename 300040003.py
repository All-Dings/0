import Dings_Lib

class Dings_Sound_Class(Dings_Lib.Object_Class):
	def __init__(Self, Caption, Json_Path, Parameter, Tag, Anchor):
		super().__init__(Caption, Json_Path, Parameter, Tag, Anchor)

	def Generate_Html(Self, Html_Id):
		print(f'<audio controls>')
		if Self.Extension == "mp3":
			print(f'  <source src="{Self.File_Path}" type="audio/mpeg">')
		else:
			print(f"Error: Dings_Sound_Class: Unsupported Type: {Self.File_Path}", file=Sys.stderr)
		print(f'</audio>')
