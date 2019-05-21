<?php
	//connect database
     require_once("./sql/DBconnection.php");
     $area_query = "select distinct areaID from cabinet;";
?>

<?php

//從資料庫抓取資料匯到JS的陣列中
                $aid_r=mysqli_query($db_link, $area_query);
                $i=0;
                echo "area=new Array();";
                echo "floor=new Array();";
                while ($aid=mysqli_fetch_array($aid_r))
                {
                	echo "area[".$i."] = '".$aid['areaID']."'; ";

                    $floor_query = "select distinct floor from cabinet where areaID = '".$aid['areaID']."';";
                    $floor_r=mysqli_query($db_link, $floor_query);
                    echo "floor[".$i."]=[];";
                    while ($floor=mysqli_fetch_array($floor_r))
                    {
                        echo "floor[".$i."].push([".$floor['floor']."]);";
                    }
                	$i++;
                }
?>
