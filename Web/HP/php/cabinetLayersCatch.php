<?php
//接收html傳入內容，並從資料庫撈取對應資料並做成下拉式選單內容後，回傳到表單

require_once("./sql/DBconnection.php");
$cabinetID=$_GET['cabinetID'];
$sql = "select cabinet_layers from cabinet where cabinetID = '$cabinetID';";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));
while ($data=mysqli_fetch_assoc($result)) {

	$res .="<option value='".$data["cabinet_layers"]."'>".$data['cabinet_layers']."</option>";
};
echo $res;
?>

