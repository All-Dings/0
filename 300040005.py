import Dings_Lib

class Dings_Pdf_Class(Dings_Lib.Object_Class):
	def __init__(Self, Caption, Json_Path, Parameter, Tag, Anchor):
		super().__init__(Caption, Json_Path, Parameter, Tag, Anchor)

	def Generate_Html(Self, Html_Id):
		print(f'<a href="{Self.Number}.pdf" type="application/pdf" target="_blank">')
		print(f' <div class="Overlay-Image-Container">')
		print(f'  <img src="{Self.Number}.jpg" class="Overlay-Image-Parent" alt="{Self.Caption}" width="100%"/>')
		print(f'  <img src="300000101.png" class="Overlay-Image-Child" width="100%"/>')
		print(f' </div>')
		print(f'</a>')
