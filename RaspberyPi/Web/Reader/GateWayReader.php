<?php
	require '../Const.php';
    $aCmdType = $_REQUEST['iCmdType'];
	
	switch($aCmdType) 
		{
			case "CMD_READ" :
			try 
			{
				//connect to SQLite database
				$dbh = new PDO("sqlite:../DataBase/Domos.db");
				$aId = $_REQUEST['iId'];
				$aResponse = array();
		
				//create table object (id integer primary key, status text); 
				//insert into object (status,id) values ('On',8);
	
				$aSqlRequest = 'select id,status from object where id IN (' . $aId . ' )';
				foreach ($dbh->query($aSqlRequest) as $row)
				{
					array_push($aResponse, $row);
				}
			
				//Response object 
				print(json_encode($aResponse));
		
				//close the database connection
				$dbh = null;
			}
			catch(PDOException $e)
			{
				echo $e->getMessage();
			}
			break;
		}
?>
