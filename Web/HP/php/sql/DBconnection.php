<?php
	$Host="192.192.152.86";//設定本機位置
	$User="mfdr";//設定伺服器連線帳號
	$Password="islasssr";//設定伺服器連線密碼
	$Database="mfdr";//設定資料庫
	$db_link=mysqli_connect($Host, $User, $Password, $Database) or die('Error connecting to MySQL server');//設定連線資料庫
?>