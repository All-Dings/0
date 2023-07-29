import json as Json
import logging as Logging
import Dings_Lib

class Dings_Quiz_Class(Dings_Lib.Object_Class):
	def __init__(Self, Caption, Json_Path, Parameter, Tag, Anchor):
		super().__init__(Caption, Json_Path, Parameter, Tag, Anchor)
		with open(Json_Path) as File:
			Self.Json = Json.load(File)

	def Generate_Html(Self, Html_Id):
		Dings_Json = Self.Json
		Logging.info("Generate")
		print(f'<div>')
		print(f'<img id="{Html_Id}.Image" src="Dings_Quiz-Image.jpg" class="Dings_Quiz-Image">')
		print(f'<audio id="{Html_Id}.Sound_Start" src="400000055.mp3" type="audio/mpeg" preload="auto"></audio>')
		print(f'<audio id="{Html_Id}.Sound_Right_Bell" src="400000059.mp3" type="audio/mpeg" preload="auto"></audio>')
		print(f'<audio id="{Html_Id}.Sound_Right_Perfect" src="400000052.mp3" type="audio/mpeg" preload="auto"></audio>')
		print(f'<audio id="{Html_Id}.Sound_Right_Errors" src="400000053.mp3" type="audio/mpeg" preload="auto"></audio>')
		print(f'<audio id="{Html_Id}.Sound_Wrong" src="400000051.mp3" type="audio/mpeg" preload="auto"></audio>')
		print(f'<audio id="{Html_Id}.Sound_Finish" src="400000054.mp3" type="audio/mpeg" preload="auto"></audio>')
		print(f'<audio id="{Html_Id}.Sound_Statistic" src="400000085.mp3" type="audio/mpeg" preload="auto"></audio>')
		print(f'<div id="{Html_Id}.Div_Controller" class="Dings_Quiz-Div_Controller" onclick="{Html_Id}.On_Press(this)">')
		print(f'<table class="No-Border Dings_Quiz-Table">')
		print(f' <tr class="No-Border Dings_Quiz-Td">')
		print(f'  <th id="{Html_Id}.Div_Controller_Label_1" class="No-Border Dings_Quiz-Th_Left">')
		print(f'   0/1')
		print(f'  </th>')
		print(f'  <th class="No-Border Dings_Quiz-Th_Middle">')
		print(f'   <label id="{Html_Id}.Div_Controller_Label_2" class="Dings_Quiz-Label">Text</label>')
		print(f'  </th>')
		print(f'  <th id="{Html_Id}.Div_Controller_Label_3" class="No-Border Dings_Quiz-Th_Right">')
		print(f'  1/1')
		print(f'  </th>')
		print(f'  </tr>')
		print(f'</table>')
		print(f'</div>')
		for Button_Id in range(0, Self.Json["Max_Answers"]):
			print(f'<button id="{Html_Id}.Button.{Button_Id}" class="Dings_Quiz-Button_Collapsed" onclick="{Html_Id}.On_Press(this)"></button>')
		print(f'</div>')
		print(f'<script src="300040007.js"></script>')
		print(f'<script>')
		print(f'{Html_Id} = new Dings_Quiz_Class(')
		print(f'{Self.Json}')
		print(f', "{Html_Id}");')
		print(f'</script>')
