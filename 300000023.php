<?php
session_start();

/*
 * Load the requested File
 */
function Load_File($File_To_Load) {
	if (str_ends_with($File_To_Load, ".jpg")) {
		header("Content-Type: image/jpg");
	} else if (str_ends_with($File_To_Load, ".mp3")) {
		header("Content-Type: audio/mpeg");
	} else if (str_ends_with($File_To_Load, ".mp4")) {
		header("Content-Type: video/mp4");
	} else if (str_ends_with($File_To_Load, ".css")) {
		header("Content-Type: text/css; charset=utf-8");
	} else {
		header("Content-Type: text/html; charset=utf-8");
	}
	header("Content-Length: " . filesize($File_To_Load));
	$fp = fopen($File_To_Load, 'rb');
	fpassthru($fp);
	// readfile($File_To_Load)
}

/*
 * Prevent secret Files from loading
 */
function Exit_if_Secret_File($File_To_Load) {
	$File_Suffix = substr($File_To_Load, strrpos($File_To_Load, ".") + 1);
	if ($File_Suffix == "access" || $File_Suffix == "login") {
		http_response_code(404);
		die();
	}
}

/*
 * Redirect to Login-Page
 */
function Redirect_to_Login_and_Exit($File_To_Load) {
	header("Location: 300000022.php?File_To_Load=" . $File_To_Load . "&Protected=1");
	die("");
}

/*
 * Exit if User has no Access
 */
function Exit_if_User_has_no_Access($File_To_Load) {
	$Dings_Number = substr($File_To_Load, 0, strrpos($File_To_Load, "."));
	$Access_File_Name = $Dings_Number . ".access";
	if (file_exists($Access_File_Name)) {
		if (!isset($_SESSION['User_Id']))
			Redirect_to_Login_and_Exit($File_To_Load);
		$Access_Info = json_decode(file_get_contents($Access_File_Name), true);
		$Current_User = $_SESSION['User_Id'];
		if (!in_array($Current_User, $Access_Info["User_List"]))
			Redirect_to_Login_and_Exit($File_To_Load);
	}
}

/*
 * Get the requested File-Name
 */
function Get_File_To_Load() {
	$File_To_Load = $_GET["File_To_Load"];
	if ($File_To_Load == "")
		return "index.html";
	else
		return $File_To_Load;
}

$File_To_Load = Get_File_To_Load();
Exit_if_Secret_File($File_To_Load);
Exit_if_User_has_no_Access($File_To_Load);
Load_File($File_To_Load);
?>
