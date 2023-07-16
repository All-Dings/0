import json as Json
import Dings_Lib

class Dings_Sip_Toggle_Class(Dings_Lib.Object_Class):
	def __init__(Self, Caption, Json_Path, Parameter, Tag, Anchor):
		super().__init__(Caption, Json_Path, Parameter, Tag, Anchor)
		with open(Json_Path) as File:
			Self.Json = Json.load(File)

	def Generate_Html(Self, Html_Id):
		Dings_Json = Self.Json
		print(f'  <div class="Dings_Sip_Toggle-Container">')
		print(f'   <img id="{Html_Id}.{Dings_Json["Pair_1"]["Image"]}" src="{Dings_Json["Pair_1"]["Image"]}" class="Dings_Sip_Toggle-Child"  onclick="{Html_Id}.Toggle_Play()"/>')
		print(f'   <img id="{Html_Id}.{Dings_Json["Pair_2"]["Image"]}" src="{Dings_Json["Pair_2"]["Image"]}" class="Dings_Sip_Toggle-Parent" onclick="{Html_Id}.Toggle_Play()"/>')
		print(f'  </div>')
		print(f'  <audio id="{Html_Id}.{Dings_Json["Pair_1"]["Sound"]}" src="{Dings_Json["Pair_1"]["Sound"]}" type="audio/mpeg" preload="auto" loop></audio>')
		print(f'  <audio id="{Html_Id}.{Dings_Json["Pair_2"]["Sound"]}" src="{Dings_Json["Pair_2"]["Sound"]}" type="audio/mpeg" preload="auto" loop></audio>')
		print(f'  <table class="No-Border">')
		print(f'   <tr class="No-Border">')
		print(f'    <th colspan="2" class="No-Border">')
		print(f'     <b> <label id="{Html_Id}.Label" class="Dings_Sip_Toggle-Label"></label></b>')
		print(f'    </th>')
		print(f'   <tr class="No-Border">')
		print(f'    <th class="No-Border" width=50%> <button id="{Html_Id}.Button-Toggle" style="height:30px;width:100%" onclick="{Html_Id}.Toggle_Play()">Toggle</button> </th>')
		print(f'    <th class="No-Border" width=50%> <button id="{Html_Id}.Button-Stop"   style="height:30px;width:100%" onclick="{Html_Id}.Stop_Play()">Stop</button> </th>')
		print(f'   </tr>')
		print(f'  </table>')
		print(f'<script src="300040001.js"></script>') # FIXME Include only once
		print(f'<script>')
		print(f'{Html_Id} = new Dings_Sip_Toggle_Class(')
		print(f'{Self.Json}')
		print(f', "{Html_Id}");')
		print(f'</script>')
