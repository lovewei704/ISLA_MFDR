<?php
//從html讀取資料，新增資料庫中相應內容

require_once("./sql/DBconnection.php");
$areaID=$_GET['areaID'];
$floor=$_GET['floor'];
$description=$_GET['description'];
$fileToUpload=$_GET['fileToUpload'];

$fileToUpload=explode("fakepath", $fileToUpload);

$FL=count($fileToUpload)-1;

$fileToUpload[$FL]='./img/'.$fileToUpload[$FL];

$sql_m = "insert into map (areaID, floor, cabinetID, Road, description, location_Photo) VALUES ('$areaID', '$floor', '', '', '$description', '$fileToUpload[$FL]');";
$sql_a = "insert into area(areaID, floor, explanation) VALUES ('$areaID', '$floor', '$description');";
$result_m = mysqli_query($db_link, $sql_m) or die("資料選取錯誤!".mysqli_error($db_link));
$result_a = mysqli_query($db_link, $sql_a) or die("資料選取錯誤!".mysqli_error($db_link));
?>
