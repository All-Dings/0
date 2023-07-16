import Dings_Lib

class Dings_Video_Class(Dings_Lib.Object_Class):
	def __init__(Self, Caption, Json_Path, Parameter, Tag, Anchor):
		super().__init__(Caption, Json_Path, Parameter, Tag, Anchor)

	def Generate_Html(Self, Html_Id):
		print(f'<video width="100%" height="auto" controls>')
		if Self.Extension == "mp4":
			print(f'  <source src="{Self.File_Path}" type=video/mp4>')
		else:
			print(f"Error: Dings_Video_Class: Unsupported Type: {Self.File_Path}", file=Sys.stderr)
			quit(1)
		print(f'</video>')
