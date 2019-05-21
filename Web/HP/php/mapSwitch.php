<?php
//讀取表單資料，將資料輸出成html給前端顯示內容

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$sql = "select location_Photo from map where areaID = '$areaID' AND floor = $floor;";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));
$res="";
while ($data=mysqli_fetch_assoc($result)) {
	$res .="<img src='".$data["location_Photo"]."' width='700px'>";
};
echo $res;
?>

