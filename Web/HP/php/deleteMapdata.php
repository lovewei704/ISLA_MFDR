<?php
//從html讀取資料，刪除資料庫中相應內容

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$sql_m = "delete from map where areaID = '$areaID' AND floor = '$floor';";
$sql_a = "delete from area where areaID = '$areaID' AND floor = '$floor';";
$result_m = mysqli_query($db_link, $sql_m) or die("資料選取錯誤!".mysqli_error($db_link));
$result_a = mysqli_query($db_link, $sql_a)or die("資料選取錯誤!".mysqli_error($db_link));

?>