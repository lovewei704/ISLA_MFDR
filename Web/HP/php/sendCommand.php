<?php
//讀取表單資料，將資料輸出成文字檔

require_once("./sql/DBconnection.php");
$jsData="";
$jsData=$_GET['jsData'];
//$jsEData=json_encode($jsData);
$CommandFile = fopen("CommandFile.txt", "w") or die("Unable to open file!");
fwrite($CommandFile, $jsData);
fclose($CommandFile);
echo $jsData;
?>

