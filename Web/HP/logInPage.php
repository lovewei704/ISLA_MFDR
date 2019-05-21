<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>登入</title>
<link rel="stylesheet" type="text/css" href="design.css">
<script src="javascript.js"></script>
<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css">
<meta name="google-signin-client_id" content="631346372917-b3i922ftm6vgocktgqeijh9jbvjqfd8v.apps.googleusercontent.com">
<script src="https://apis.google.com/js/api:client.js"></script>
<style type="text/css">
    #login_google {
      	background:#d34836;
      	width:100%;
		font-size: 35px;
		font-weight:bold;
		border-radius: 20px;
		border-style:double;
		color:white;
		cursor:pointer;
    }
  </style>
</head>

<body class="all_body" ondragstart="window.event.returnValue=false" onLoad="getUserName()">

<div id="fb-root"></div>
    <div id="userName" class="userName">訪客</div>
	<div class="loginButtonDiv"></div><input type="button" class="loginButton" id="loginButton" value="登 入" onClick="loginORlogout()">
	<div id="topMenu">
		<ul>
			<li id="topMenu_logo"><a href="index.html"><img src="img/MFDR_logo.png" alt="MFDR" class="logo">&emsp;&emsp;&emsp;</a></li>
			<li><a href="aboutPage.html">關於</a></li>
			<li><a href="mapPage.html">地圖</a></li>
			<li><a href="robotPage.html">工作指派</a></li>
      		<li><a href="monitorPage.html">即時監控</a></li>
      		<li id="editPage" style="display:none"><a href="editPage.html">編輯</a></li>
		</ul>
	</div><br>
	
    <div id="login_pleaseDiv"><span id="login_pleaseLogin">— 請先登入 —</span></div>
    
    
    <table id="login_table">
    <!--
    	<tr>
        <form action = "./logInPage.php" method="post">
        	<td class="login_table_td">
            	<span class="login_span">帳&emsp;&emsp;號：</span><input type="email" class="login_input" name="logIn_account" id="login_account">
            </td>
        </tr>
        <tr>
        	<td class="login_table_td">
            	<span class="login_span">密&emsp;&emsp;碼：</span><input type="password" class="login_input" name="logIn_password" id="logIn_password">
            </td>
        </tr>
        <tr>
        	<td class="login_table_td">
            	<div class="login_submitMDiv"><input class="login_submitM" type="submit" value="登&emsp;入"></div>
        </form>
            	<div class="login_submitMDiv"><a href="registerPage.php"><input class="login_submitM" type="submit" value="註&emsp;冊"></a></div>
            </td>
        </tr> -->
        <tr>
        	<td class="login_table_td"><div class="login_submitGDiv"><input id="login_google" class="login_submitG" type="submit" value="google"></div></td>
        </tr>
        <tr></tr>
        <tr>
            <td class="login_table_td"><div class="login_submitFDiv"><input id="login_facebook" class="login_submitF" type="submit" value="facebook" onClick="login()"></div></td>
        </tr>
    </table>
    
	<script>startApp();</script>
    
</body>
</html>

<?php
/*
//receive data from loginpage and check data is not empty
   if($_POST)
   {
    if(!empty($_POST['logIn_account']) AND !empty($_POST['logIn_password']))
    {
      $account=$_POST['logIn_account'];
    
      $password=$_POST['logIn_password'];
    }
    else
    {
      echo "account and password is empty";
    }
   }


   //connect database
   require_once("./sql/DBconnection.php");

   //check data from database if data match can login
   if(!empty($account)AND!empty($password))
   {
    $sql_query = "select * from common_user where account = '$account' and password = '$password';";
    $result=mysqli_query($db_link, $sql_query);
    $totalRecords=mysqli_num_rows($result);

    if($totalRecords > 0){header("Location: http://localhost:9527/mfdr/aboutPage.php");exit;}
    else{echo "Account '" . $account ."' does not exist!! or PW '" . $password . "' does not match!! <br />.";}
   }*/
?>