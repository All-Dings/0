/*
 * Constants for State-Machine
 */
const Dings_Quiz_State = {
	WAIT_START:		"WAIT_START",
	WAIT_ANSWER:		"WAIT_ANSWER",
	WAIT_NEXT_QUESTION:	"WAIT_NEXT_QUESTION",
	WAIT_SCORE:		"WAIT_SCORE",
	WAIT_RESTART:		"WAIT_RESTART",
};

/*
 * One of many Questions
 */
class Dings_Quiz_Question_Class {
	constructor(Json) {
		this.Json = Json;
		this.Answer_Count_Total = Json.Correct_Answer_List.length;
		this.Answer_Count_Right = 0;
		this.Answer_Count_Wrong = 0;
	}
}

/*
 * Quiz that contains multiple Questions
 */
class Dings_Quiz_Class {
	/* Get Html-Element by Name */
	Element(Name) {
		return document.getElementById(this.Html_Id + "." + Name);
	}

	/* Set Text for Controller */
	Set_Div_Controller(Text, Print_Stats=true) {
		let Question_Count = this.Json.Question_List.length;
		let Question_Stat = "";
		let Quiz_Stat = "";
		if (Print_Stats) {
			Question_Stat = this.Current_Question.Answer_Count_Right + "/" + this.Current_Question.Answer_Count_Total;
			Quiz_Stat = (this.Current_Question_Number + 1) + "/" + Question_Count;
		}
		this.Element("Div_Controller_Label_1").innerHTML = Question_Stat;
		this.Element("Div_Controller_Label_2").innerHTML = Text;
		this.Element("Div_Controller_Label_3").innerHTML = Quiz_Stat;
	}

	/* Set Timer for Message */
	Set_Timer(Message, Timeout_Ms=this.Timer_Value_Ms) {
		this.Timer = setTimeout(() => {document.getElementById(`${this.Html_Id}.Div_Controller_Label_2`).innerHTML = Message}, Timeout_Ms);
	}

	/* Clear Timer */
	Clear_Timer() {
		if (this.Timer)
			clearTimeout(this.Timer)
	}

	/* Build Object out of Json and Html_Id for the Widget */
	constructor(Json, Html_Id) {
		console.log("Dings_Quiz_Class: " + Html_Id);
		this.Html_Id = Html_Id;
		this.Json = Json;
		this.Icon_Question = "400000056.png"
		this.Icon_Wrong = "400000057.png"
		this.Icon_Right = "400000058.png";
		this.Element("Image").src = this.Json.Image_Quiz;
		this.Current_Question_Number = 0;
		this.Set_Div_Controller("Start Quiz", false);
		this.State = Dings_Quiz_State.WAIT_START;
		this.Timer_Value_Ms = 3000;
		this.Timer = null;
	}

	/* Start the Quiz */
	Start_Quiz() {
		if (this.Timer)
			clearTimeout(this.Timer)
		this.Question_Done_List = [];
		this.Enter_Question_Running(0);
		this.Element("Sound_Start").play();
	}

	/* State-Change: Start new Question */
	Enter_Question_Running(Question_Number) {
		// Setup new Question
		this.Current_Question_Number = Question_Number;
		this.Current_Question = new Dings_Quiz_Question_Class(this.Json.Question_List[Question_Number]);
		this.Question_Done_List.push(this.Current_Question);
		let Json = this.Current_Question.Json;
		// Clear Buttons
		this.Button_List_Pressed = [];
		for (let Answer_Number = 0; Answer_Number < Json.Answer_List.length; Answer_Number++) {
			this.Element("Button." + Answer_Number).classList.remove("Dings_Quiz-Button_Wrong");
			this.Element("Button." + Answer_Number).classList.remove("Dings_Quiz-Button_Right");
			this.Element("Button." + Answer_Number).classList.remove("Dings_Quiz-Button_Collapsed");
			this.Element("Button." + Answer_Number).classList.add("Dings_Quiz-Button");
			let Inner_Html = `<img id="${this.Html_Id}.Button.${Answer_Number}.Icon" src="${this.Icon_Question}" align="left" class="Dings_Quiz-Button_Icon_Left">`;
			Inner_Html += `${Json.Answer_List[Answer_Number]}`;
			Inner_Html += `<img src="${this.Icon_Question}" class="Dings_Quiz-Button_Icon_Right">`;
			this.Element("Button." + Answer_Number).innerHTML = Inner_Html;
			this.Button_List_Pressed.push(false);
		}
		// Write Question and set Image
		this.Set_Div_Controller(Json.Question)
		this.Element("Image").src = Json.Image_Question;
		this.State = Dings_Quiz_State.WAIT_ANSWER;
	}

	/* State-Change: Last Question has been answered */
	Enter_Wait_Score() {
		this.Element("Div_Controller").disabled = false;
		this.Set_Div_Controller(this.Current_Question.Json.Answer);
		this.Set_Timer("Press for Score!");
		this.State = Dings_Quiz_State.WAIT_SCORE;
	}

	/* State-Change: Last Question has been answered */
	Enter_Wait_Restart() {
		this.Element("Div_Controller").disabled = false;
		this.Set_Timer("Press for Restart!", 6000);
		this.State = Dings_Quiz_State.WAIT_RESTART;
	}

	/* State-Change: Wait for next Question */
	Enter_Wait_Next_Question() {
		this.Element("Div_Controller").disabled = false;
		this.Set_Div_Controller(this.Current_Question.Json.Answer);
		this.Set_Timer("Press for next Question!");
		this.State = Dings_Quiz_State.WAIT_NEXT_QUESTION;
	}

	/* Action: Process Question-Answer */
	Do_Answer(Button_Name) {
		let Question_Count = this.Json.Question_List.length;
		let Answer_Number = parseInt(Button_Name);
		if (Button_Name == "Div_Controller")
			return;
		if (this.Button_List_Pressed[Answer_Number])
			return;
		let Button_Html = this.Element("Button." + Answer_Number);
		let Button_Icon_Html = this.Element("Button." + Answer_Number + ".Icon");
		this.Button_List_Pressed[Answer_Number] = true;
		if (this.Current_Question.Json.Correct_Answer_List.includes(Answer_Number)) {
			/* Got right Answer */
			Button_Html.classList.add("Dings_Quiz-Button_Right");
			this.Current_Question.Answer_Count_Right++;
			Button_Icon_Html.src = this.Icon_Right;
			this.Set_Div_Controller(this.Current_Question.Json.Question);
			if (this.Current_Question.Answer_Count_Right == this.Current_Question.Answer_Count_Total) {
				/* All required Answers received */
				this.Element("Image").src = this.Current_Question.Json.Image_Answer;
				if (this.Current_Question_Number == Question_Count - 1) {
					/* Last Question done */
					this.Element("Sound_Finish").play();
					this.Enter_Wait_Score();
				} else {
					/* More Questions to do */
					if (this.Current_Question.Answer_Count_Wrong == 0)
						this.Element("Sound_Right_Perfect").play();
					else
						this.Element("Sound_Right_Errors").play();
					this.Element("Image").src = this.Current_Question.Json.Image_Answer;
					this.Enter_Wait_Next_Question();
				}
			} else {
				/* More Answers required */
				this.Element("Sound_Right_Bell").play()
			}
		} else {
			/* Got wrong Answer */
			Button_Html.classList.add("Dings_Quiz-Button_Wrong");
			this.Current_Question.Answer_Count_Wrong++;
			Button_Icon_Html.src = this.Icon_Wrong;
			this.Element("Sound_Wrong").play();
			this.Element("Div_Controller").animate({ backgroundColor: "red" }, 500);
			this.Set_Div_Controller(this.Current_Question.Json.Question);
		}
	}

	/* Action: Start Quiz */
	Do_Start_Quiz(Button_Name) {
		if (Button_Name != "Div_Controller")
			return;
		this.Start_Quiz();
	}

	/* Action: Do the next Question */
	Do_Next_Question(Button_Name) {
		this.Enter_Question_Running(this.Current_Question_Number + 1);
	}

	/* Action: Print Score */
	Do_Score(Button_Name) {
		// Play Sound and set Image
		this.Element("Sound_Statistic").play();
		this.Element("Image").src = this.Json.Image_Finish;
		// Calculate Score
		let Answer_Count_Wrong = 0;
		let Answer_Count_Right = 0;
		let Answer_Count_Total = 0;
		for (let i = 0; i < this.Question_Done_List.length; i++) {
			let Question = this.Question_Done_List[i];
			Answer_Count_Wrong += Question.Answer_Count_Wrong;
			Answer_Count_Right += Question.Answer_Count_Right;
			Answer_Count_Total += Question.Answer_Count_Total;
		}
		// Collapse Buttons
		let Json = this.Current_Question.Json;
		for (let Answer_Number = 0; Answer_Number < Json.Answer_List.length; Answer_Number++) {
			this.Element("Button." + Answer_Number).classList.remove("Dings_Quiz-Button");
			this.Element("Button." + Answer_Number).classList.add("Dings_Quiz-Button_Collapsed");
		}
		let Score_Percent = Answer_Count_Total/(Answer_Count_Wrong + Answer_Count_Right) * 100;
		// Update Controller Message
		this.Current_Question_Number++;
		this.Set_Div_Controller("Score: " + Score_Percent.toFixed(0) + " %", false);
		this.Enter_Wait_Restart();
	}

	/* Action: Restart Quiz */
	Do_Restart(Button_Name) {
		this.Start_Quiz();
	}

	/* State-Machine */
	On_Press(Button) {
		this.Clear_Timer();
		let Button_Name = Button.id.split('.').pop();
		switch (this.State) {
		case Dings_Quiz_State.WAIT_START:
			this.Do_Start_Quiz(Button_Name);
			break;
		case Dings_Quiz_State.WAIT_ANSWER:
			this.Do_Answer(Button_Name);
			break;
		case Dings_Quiz_State.WAIT_NEXT_QUESTION:
			this.Do_Next_Question(Button_Name);
			break;
		case Dings_Quiz_State.WAIT_SCORE:
			this.Do_Score(Button_Name);
			break;
		case Dings_Quiz_State.WAIT_RESTART:
			this.Do_Restart(Button_Name);
			break;
		default:
			console.log("Unknown State: " + this.State);
			break;
		}
	}
}
