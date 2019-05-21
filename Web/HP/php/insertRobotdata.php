<?php
//從html讀取資料，新增資料庫中相應內容

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$robot=$_GET['robot'];
$execution=$_GET['execution'];
$sql = "insert into robot (areaID, floor, robotID, InExecution) VALUES ('$areaID', '$floor', '$robot', '$execution');";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));

echo $sql;
?>