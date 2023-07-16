/*
 * Set a new Cookie
 */
function Set_Cookie(Cookie_Name, Cookie_Value, Expire_Days) {
	const Current_Date = new Date();
	Current_Date.setTime(Current_Date.getTime() + (Expire_Days * 24 * 60 * 60 * 1000));
	let Expire_Date = "expires=" + Current_Date.toUTCString();
	New_Cookie = Cookie_Name + "=" + Cookie_Value + ";" + Expire_Date + ";path=/";
	document.cookie = Cookie_Name + "=" + Cookie_Value + ";" + Expire_Date + ";path=/";
}

/*
 * Get a Cookie
 */
function Get_Cookie(Cookie_Name) {
	let Name = Cookie_Name + "=";
	let Cookie_List = document.cookie.split(';');
	for (let i = 0; i < Cookie_List.length; i++) {
		let Cookie = Cookie_List[i];
		while (Cookie.charAt(0) == ' ') {
			Cookie = Cookie.substring(1);
		}
		if (Cookie.indexOf(Name) == 0) {
			return Cookie.substring(Name.length, Cookie.length);
		}
	}
	return "";
}

/*
 * When the User scrolls down, hide the Top-Nave, on Scroll-Up show it again.
 */
var Previous_Scroll_Position = window.pageYOffset;

window.onscroll = function() {
	var Current_Scroll_Position = window.pageYOffset;
	if (Current_Scroll_Position < 50 || Previous_Scroll_Position > Current_Scroll_Position) {
		/* Show Top-Nav */
		document.getElementById("Dings-Top-Nav").style.top = "0";
		document.getElementById("Dings-Side-Bar").style.marginTop = "30px";
	} else {
		/* Hide Top-Nav */
		document.getElementById("Dings-Top-Nav").style.top = "-50px";
		document.getElementById("Dings-Side-Bar").style.marginTop = "-28px";
	}
	Previous_Scroll_Position = Current_Scroll_Position;
}

/*
 * Toggle between collapsed and open Top-Nav-Menu
 */
function Toggle_Top_Nav_Responsive() {
	var Top_Nav = document.getElementById("Dings-Top-Nav");
	var Under_Construction =  document.getElementById("Dings-Under-Construction")
	if (Top_Nav.className === "Dings-Top-Nav") {
		Top_Nav.className += " responsive";
		Under_Construction.style.float = "None"
	} else {
		Top_Nav.className = "Dings-Top-Nav";
		Under_Construction.style.float = "Right"
	}
}

/*
 * Toggle between collapsed and open Top-Nav-Menu
 */
function Toggle_Side_Bar() {
	Button = document.getElementById("Dings-Toggle-Side-Bar");
	Icon = Button.getElementsByTagName("i")[0];
	Icon.classList.toggle("fa-minus");
	var Dings_Content = document.getElementById("Dings-Content");
	var Dings_Side_Bar = document.getElementById("Dings-Side-Bar");

	if (Dings_Content.className === "Dings-Content-With-Side-Bar") {
		Dings_Content.className = "Dings-Content";
		Dings_Side_Bar.className = "Dings-Side-Bar-Hide";
		Set_Cookie("Dings-Side-Bar", "Hide", 30);
	} else {
		Dings_Content.className = "Dings-Content-With-Side-Bar";
		Dings_Side_Bar.className = "Dings-Side-Bar";
		Set_Cookie("Dings-Side-Bar", "Show", 30);
	}
}

/*
 * Execute Stuff after loading Page
 */
function On_Load() {
	console.log("Loading...");
	if (Get_Cookie("Dings-Side-Bar") == "") {
		Set_Cookie("Dings-Side-Bar", "Hide", 30);
	}
	if (Get_Cookie("Dings-Side-Bar") == "Show") {
		Toggle_Side_Bar()
	}
	Selected_Sidebar_Element = document.getElementById("First-Sidebar-Element");
	Selected_Sidebar_Element.classList.add("active");
	Side_Bar = document.getElementById('Dings-Side-Bar');
	Side_Bar.scrollTop = Selected_Sidebar_Element.offsetTop;
	// FIXME: This does not work for some Reason
	// Content = document.getElementById('Dings-Content');
	// Content.scrollTop = 0;
}

var Last_Selected_Side_Bar_Secs = new Date().getTime() / 1000;

/*
 * Callback for selecting the clicked Sidebar-Element
 */
function Select_Sidebar_Element(Event) {
	let Target = Event.target;
	/* Remove old Selection */
	if (Selected_Sidebar_Element.classList.contains("active")) {
		Selected_Sidebar_Element.classList.remove("active");
	}
	/* Set new Selection */
	if (!Target.classList.contains("active")) {
		Target.classList.add("active");
		Side_Bar = document.getElementById('Dings-Side-Bar');
	}
	Selected_Sidebar_Element = Target;
	Last_Selected_Side_Bar_Secs = new Date().getTime() / 1000;
}

/*
// Disabled Experimental-Code: https://www.bram.us/2020/01/10/smooth-scrolling-sticky-scrollspy-navigation
// Use --section-divs Pandoc-Option

var Selected_Sidebar_Element
var Active_Elements = []

function Scroll_Sidebar() {
	let i = 0;
	let Min_Level = 10;
	let Top_Element = null;

	Time_Secs = new Date().getTime() / 1000;
	if (Time_Secs - Last_Selected_Side_Bar_Secs <= 1) {
		return;
	}
	Prev_Side_Bar_Scroll_Position = window.pageYOffset;
	console.log(" List-Len: " + Active_Elements.length);
	while (i < Active_Elements.length) {
		console.log("  Element: " + i);
		Nav_Element = Active_Elements[i];
		if (Top_Element == null) {
			Top_Element = Nav_Element;
		}
		// ClassName = "Heading_X"
		Nav_Element_Level = Number(Nav_Element.className.substring(8, 9));
		if (Top_Element.offsetTop <= Nav_Element.offsetTop) {
			console.log(" Up Pos: " + Nav_Element.offsetTop);
			Top_Element = Nav_Element;
			Min_Level = Nav_Element_Level;
		}
		i++
	}
	if (!Top_Element) {
		return;
	}
	console.log(" Top-Elem : " + Top_Element.offsetTop);
	console.log(" Top-Bar  : " + Side_Bar.scrollTop);
	console.log(" Top-Bar H: " + Side_Bar.offsetHeight);
	Side_Bar = document.getElementById('Dings-Side-Bar')
	Side_Bar.scrollTop = Top_Element.offsetTop - Side_Bar.offsetHeight / 2;
	Selected_Sidebar_Element = Top_Element;
}

window.addEventListener('DOMContentLoaded', () => {
	console.log("Listener");
	const observer = new IntersectionObserver(entries => {
		console.log("------------------------------------")
		entries.forEach(entry => {
			const id = entry.target.getAttribute('id');
			console.log(" ID: " + id);
			Nav_Element = document.querySelector(`.Dings-Side-Bar a[href="#${id}"]`)
			if (entry.intersectionRatio > 0) {
				// Nav_Element..parentElement.classList.add('active');
				console.log(" ADD!");
				console.log(" Pos: " + Nav_Element.offsetTop)
				Active_Elements.push(Nav_Element)
				Nav_Element.classList.add('active');
			} else {
				// Nav_Element.parentElement.classList.remove('active');
				console.log(" REMOVE!");
				Active_Elements.pop(Nav_Element)
				Nav_Element.classList.remove('active');
			}
		});
		Scroll_Sidebar()
	});

	// Track all sections that have an `id` applied
	document.querySelectorAll('section[id]').forEach((section) => {
	// document.querySelectorAll('H2[id]').forEach((section) => {
		console.log("Observer");
		observer.observe(section);
	});
});
*/
