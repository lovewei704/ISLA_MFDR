<?php
//從html讀取資料，更新資料庫中相應內容

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$description=$_GET['description'];
$fileToUpload=$_GET['fileToUpload'];

$fileToUpload=explode("fakepath", $fileToUpload);

$FL=count($fileToUpload)-1;

$fileToUpload[$FL]='./img/'.$fileToUpload[$FL];

$sql = "update map set description = '$description',location_Photo = '$fileToUpload[$FL]'  where areaID = '$areaID' AND floor = '$floor';";
$result = mysqli_query($db_link, $sql) or die("資料選取錯誤!".mysqli_error($db_link));

echo $result;
?>