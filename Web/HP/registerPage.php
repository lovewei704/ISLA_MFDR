<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>註冊</title>
<link rel="stylesheet" type="text/css" href="design.css">
<script src="javascript.js"></script>
</head>

<body class="all_body" ondragstart="window.event.returnValue=false" onLoad="getUserName()">
	<div id="userName" class="userName"></div>
	<div class="loginButtonDiv"></div><input type="button" class="loginButton" id="loginButton" value="" onClick="loginORlogout()">
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

<form action = "./registerPage.php" method="post">
	 <table id="login_table">
    	<tr>
        	<td class="login_table_td">
            	<span class="login_span">帳&emsp;&emsp;號：</span><input type="email" class="login_input" name="register_account">
            </td>
        </tr>
        <tr>
        	<td class="login_table_td">
            	<span class="login_span">密&emsp;&emsp;碼：</span><input type="password" class="login_input" id="pwd" onkeyup="checkPassword()" name="register_password">
            </td>
        </tr>
        <tr>
        	<td class="login_table_td">
            	<span class="login_span">確認密碼：</span><input type="password" class="login_input" id="checkPwd" onkeyup="checkPassword()" name="register_checkpassword">
                <div id="register_checkDiv">
    				<img src="img/nocheck.png" alt="密碼相同" id="register_check">
    				<div class="register_checkHideDiv" id="register_hideCheck"></div>
  				</div>
            </td>    
        </tr>
        <tr>
        	<td class="login_table_td">
            	<div id="register_submitDiv"><a href="loginPage.php"><input id="register_submit" type="submit" value="註&emsp;冊"></a></div>
            </td>
        </tr>
    </table>
</form>
    
</body>
</html>

<?php
//receive data from registerPage.php
//確認接收值是否為空
     /*if($_POST)
     {
        if(!empty($_POST['register_account']))
        {
            $account=$_POST['register_account'];
        }
        if(!empty($_POST['register_password'])&&!empty($_POST['register_checkpassword']))
        {
            $password=$_POST['register_password'];
            $checkpassword=$_POST['register_checkpassword'];
        }
     }

//connect database
     require_once("./sql/DBconnection.php");

//insert data to database and check data
    if(!empty($account)AND!empty($password))
    {
        if(strcmp($password, $checkpassword)==0)//字串比對，大小寫嚴謹
        {
            $insert_user="insert into common_user(account, password, permission) values('" . $account . "', '" . $password . "', 'user');";
            if(mysqli_query($db_link, $insert_user)==true)
            {
                echo "insert success";
                header("Location: http://localhost:9527/mfdr/logInPage.php");exit;
            }
            else
            {
                echo "insert data Error".'<br />';
            }
        }
        else
        {
            echo "password is type error: ".$password."、".$checkpassword;
        }
    }
    else
    {
        header("Location: http://localhost:9527/mfdr/registerPage.php");exit;
        echo "password is empty";
    }

     mysqli_close($db_link);*/
?>