<?php
//接收表單資料，讀取相對應內容後，將資料回傳到表單

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$sql = "select road from map where areaID = '$areaID' AND floor = '$floor';";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));
$res="";
while ($data=mysqli_fetch_assoc($result)) {
	$res .=$data['road'];
};
echo $res;
?>

