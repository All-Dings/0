<?php
if (isset($_GET['Protected'])) {
	$Current_User = $_SESSION['User_Id'];
	echo "<h1> Access denied </h1>";
	if ($Current_User == "") {
		echo 'This Page is protected, please login to continue!<br><br>';
	} else {
		echo 'This Page is not accessible for User "' . $Current_User . '".<br><br>';
		exit();
	}
} else if (isset($_GET['Logout'])) {
	echo "<h1>Logout</h1>";
	session_start();
	session_destroy();
	echo 'Successful for User-Id "' .  $_SESSION['User_Id'] . '".';
	echo '<script type="text/javascript">',
	"localStorage.setItem('All_Dings.Current_User', 'Unknown');",
	"Init_Early();",
	"console.log('Logout');",
	'</script>'
	;
	exit();
} else if (isset($_GET['Login'])) {
	echo "<h1>Login</h1>";
	$User_Id = $_POST['User_Id'];
	$Login_File_Name = $User_Id . ".login";
	$Password = $_POST['Password'];

	if (!file_exists($Login_File_Name)) {
		echo 'Please enter a valid User-Id<br>';
		goto out;
	}
	$Login_Info = json_decode(file_get_contents($Login_File_Name), true);
	$Password_Hash = $Login_Info["Password_Hash"];
	if (!password_verify($Password, $Password_Hash)) {
		echo 'Invalid Password<br>';
		goto out;
	}
	// Login User
	$_SESSION['User_Id'] = $User_Id;
	echo 'Successful for User-Id "' .  $_SESSION['User_Id'] . '".' . '<br>';
	$User_Id_String = '"' . $User_Id . '"';
	echo '<script type="text/javascript">',
	"localStorage.setItem('All_Dings.Current_User', $User_Id_String);",
	"document.getElementById('Dings-Login').innerHTML = $User_Id_String;",
	"Init_Early();",
	"console.log('test');",
	'</script>'
	;
	exit();
} else {
	echo "<h1>Login</h1>";
}
out:
?>

<form action="?Login=1" method="post">
User-Id:<br>
<input type="Text" size="40" maxlength="250" name="User_Id"><br><br>

Password:<br>
<input type="Password" size="40"  maxlength="250" name="Password"><br>

<input type="Submit" value="Submit">
</form>
