<?php
//從html讀取資料，刪除資料庫中相應內容

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$robot=$_GET['robot'];
$sql = "delete from robot where areaID = '$areaID' AND floor = '$floor' AND robotID= '$robot';";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));

echo $sql;
?>