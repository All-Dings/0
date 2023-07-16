/*
 * Dings_Sip of a Sound- and an Image-File
 */
class Dings_Sip_Class {
	constructor(Dings_Json, Html_Id) {
		var Sound_Html_File = Dings_Json.Sound.replace(".mp3", ".html");
		this.Title = Dings_Json.Title;
		this.Title_Link = `<a href="${Sound_Html_File}">${this.Title}</a>`;
		this.Image_Html = document.getElementById(Html_Id + "." + Dings_Json.Image);
		this.Sound_Html = document.getElementById(Html_Id + "." + Dings_Json.Sound);
		console.log("Sound     : " + Dings_Json.Sound);
		console.log("Sound Html: " + this.Sound_Html);
	}
}

/*
 * Two Dings_Sip Objects to toggle
 */
class Dings_Sip_Toggle_Class {
	/*
	 * Generate Html-Code for Widget
	 */
	Get_Html(Dings_Json, Html_Id) {
		var Html=`
<figure id="${Html_Id}">
 <div class="Dings_Sip_Toggle-Container">
  <img id="${Html_Id}.${Dings_Json.Pair_1.Image}" src="${Dings_Json.Pair_1.Image}" class="Dings_Sip_Toggle-Child" onclick="${Html_Id}.Toggle_Play()"/>
  <img id="${Html_Id}.${Dings_Json.Pair_2.Image}" src="${Dings_Json.Pair_2.Image}" class="Dings_Sip_Toggle-Parent" onclick="${Html_Id}.Toggle_Play()"/>
 </div>
  <audio id="${Html_Id}.${Dings_Json.Pair_1.Sound}" src="${Dings_Json.Pair_1.Sound}" type="audio/mpeg" preload="auto" loop></audio>
  <audio id="${Html_Id}.${Dings_Json.Pair_2.Sound}" src="${Dings_Json.Pair_2.Sound}" type="audio/mpeg" preload="auto" loop></audio>
<table class="No-Border">
  <tr class="No-Border">
   <th colspan="2" class="No-Border">
     <b> <label id="${Html_Id}.Label" class="Dings_Sip_Toggle-Label"></label></b>
   </th>
  <tr class="No-Border">
   <th class="No-Border" width=50%> <button id="${Html_Id}.Button-Toggle" style="height:30px;width:100%" onclick="${Html_Id}.Toggle_Play()">Toggle</button> </th>
   <th class="No-Border" width=50%> <button id="${Html_Id}.Button-Stop"   style="height:30px;width:100%" onclick="${Html_Id}.Stop_Play()">Stop</button> </th>
  </tr>
</table>
<figcaption>
<a href="1971092002.html">Tone Comparison</a>
</figcaption>
</figure>
`
		return Html;
	}

	/*
	 * Build Object out of Json and Html_Id for the Widget
	 */
	constructor(Dings_Json, Html_Id) {
		// Replace Placeholder Html-Element with new Html-Code
		// var Html = document.getElementById(Html_Id);
		// console.log(Dings_Json)
		// Html.innerHTML = this.Get_Html(Dings_Json, Html_Id);
		this.Dings_Json = Dings_Json;
		this.Sip_1 = new Dings_Sip_Class(Dings_Json.Pair_1, Html_Id);
		this.Sip_2 = new Dings_Sip_Class(Dings_Json.Pair_2, Html_Id);
		this.Label_Html = document.getElementById(Html_Id + ".Label");
		this.Label_Html.innerHTML = this.Sip_1.Title_Link;
		this.Sip_Current = this.Sip_1;
		this.Sip_1.Image_Html.style.opacity = this.Dings_Json.Opacity;
		this.Sip_2.Image_Html.style.opacity = 1.0
	}

	/*
	 * Pause Sound-1 and start Sound-2
	 */
	Toggle_Sound_From_To(Sound_Html_1, Sound_Html_2) {
		Sound_Html_1.pause();
		Sound_Html_2.play();
	}

	/*
	 * Bring Image 2 to front
	 */
	Toggle_Image_From_To(Image_Html_1, Image_Html_2) {
		Image_Html_1.classList.remove("Dings_Sip_Toggle-Child");
		Image_Html_1.classList.add("Dings_Sip_Toggle-Parent");
		Image_Html_1.style.opacity = "1.0";
		Image_Html_2.classList.remove("Dings_Sip_Toggle-Parent");
		Image_Html_2.classList.add("Dings_Sip_Toggle-Child");
		Image_Html_2.style.opacity = this.Dings_Json.Opacity;
	}

	/*
	 * Toggle Image and Sound
	 */
	Toggle_Play() {
		if (this.Sip_Current == this.Sip_1) {
			// Change 1 -> 2
			console.log("Change -> " + this.Sip_2.Title);
			this.Sip_2.Sound_Html.currentTime = this.Sip_1.Sound_Html.currentTime;
			this.Toggle_Sound_From_To(this.Sip_1.Sound_Html, this.Sip_2.Sound_Html);
			this.Toggle_Image_From_To(this.Sip_1.Image_Html, this.Sip_2.Image_Html);
			this.Label_Html.innerHTML = this.Sip_2.Title_Link;
			this.Sip_Current = this.Sip_2;
		} else {
			// Change 2 -> 1
			console.log("Change -> " + this.Sip_1.Title);
			this.Sip_1.Sound_Html.currentTime = this.Sip_2.Sound_Html.currentTime;
			this.Toggle_Sound_From_To(this.Sip_2.Sound_Html, this.Sip_1.Sound_Html);
			this.Toggle_Image_From_To(this.Sip_2.Image_Html, this.Sip_1.Image_Html);
			this.Label_Html.innerHTML = this.Sip_1.Title_Link;
			this.Sip_Current = this.Sip_1;
		}
	}

	/*
	 * Stop Sound
	 */
	Stop_Play() {
		this.Sip_1.Sound_Html.pause();
		this.Sip_2.Sound_Html.pause();
	}
}
