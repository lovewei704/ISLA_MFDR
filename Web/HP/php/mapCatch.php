<?php
//連接資料庫
require_once("./sql/DBconnection.php");

//從表單接收資料
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];

//利用表單接收的資料，從資料庫讀取資料
$sql = "select * from map where areaID = '$areaID' AND floor = '$floor';";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));

$res="";
while ($data=mysqli_fetch_assoc($result)) {
	$res .=json_encode($data);
};
echo $res;
?>