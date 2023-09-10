import Dings_Lib

class Dings_Image_Class(Dings_Lib.Object_Class):
	def __init__(Self, Caption, Json_Path, Parameter, Tag, Anchor):
		super().__init__(Caption, Json_Path, Parameter, Tag, Anchor)

	def Generate_Html(Self, Html_Id):
		print(f'<a href="{Self.Number}.html">')
		if Self.Caption:
			print(f'  <img src="{Self.File_Path}" alt="{Self.Caption}" width="100%"/>')
		else:
			print(f'  <img src="{Self.File_Path}" width="100%"/>')
		print(f'</a>')
