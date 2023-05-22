<?php
date_default_timezone_set('Asia/Kolkata');
include('database.inc.php');
$txt=mysqli_real_escape_string($con,$_POST['txt']);
$sql="select reply from chatbot_hints where question like '%$txt%'";

$res=mysqli_query($con,$sql);

if(mysqli_num_rows($res)>0){

	$row=mysqli_fetch_assoc($res);
	$html=$row['reply'];

}else{
	$html="Sorry not be able to understand you";
}

$added_on=date('Y-m-d h:i:s');
mysqli_query($con,"insert into message(message,added_on,type) values('$txt','$added_on','user')");
$added_on=date('Y-m-d h:i:s');
$type = 'bot';
$sql="insert into message(message,added_on,type) values(?, ?, ?)";
$stmt = mysqli_prepare($con, $sql);
mysqli_stmt_bind_param($stmt, "sss", $html, $added_on, $type);
mysqli_stmt_execute($stmt);
echo $html;
echo " ";
?>


<!--
<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<style>
	<link href="style.css" rel="stylesheet">
</style>
<a href="#"><small><input name="invalid"  type="button" id="admin_btn" value="Invalid?"></small></a>
<body>
</body>
</html>-->
