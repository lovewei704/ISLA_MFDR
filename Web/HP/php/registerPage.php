<?php
//receive data from loginpage
	 if($_POST)
	 {
	 	if(!empty($_POST['register_account']))
	 	{
	 		$account=$_POST['register_account'];
	 	}
	 	if(!empty($_POST['register_password'])&&!empty($_POST['register_checkpassword']))
	 	{
	 		$password=$_POST['register_password'];
	 		$checkpassword=$_POST['register_checkpassword'];
	 	}
	 }

//connect database
	 require_once("./sql/DBconnection.php");

//insert data to database and check data
	if(!empty($account)AND!empty($password))
	{
		if(strcmp($password, $checkpassword)==0)//字串比對，大小寫嚴謹
		{
			$insert_user="insert into common_user(account, password, permission) values('" . $account . "', '" . $password . "', 'user');";
			if(mysqli_query($db_link, $insert_user)==true)
			{
				echo "insert success";
			}
			else
			{
				echo "insert data Error".'<br />';
			}
		}
		else
		{
			echo "password is type error: ".$password."、".$checkpassword;
		}
	}
	else
	{
		echo "password is empty";
	}

	 mysqli_close($db_link);
?>