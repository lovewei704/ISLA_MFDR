<?php
//接收html傳入內容，並從資料庫撈取對應資料並做成下拉式選單內容後，回傳到表單

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$sql = "select distinct cabinetID from cabinet where areaID = '$areaID' AND floor = '$floor';";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));
while ($data=mysqli_fetch_assoc($result)) {
	$res .="<option value='".$data["cabinetID"]."'>".$data['cabinetID']."</option>";
};
echo $res;
?>

