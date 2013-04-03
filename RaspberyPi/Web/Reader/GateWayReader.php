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
            
            case "CMD_READ2" :
            $aCommandToExecute = WRAPPER2 . "-o " . getenv(REMOTE_ADDR) . " -s " . $_REQUEST["iCmdToExecute"] . " -t READ";
			$output = array();
			exec($aCommandToExecute, $output);
			print(json_encode($output));
			break;
			
			case "CMD_READ_VALUE_DB" :
			try 
			{
				//connect to SQLite database
				$dbh = new PDO("sqlite:../DataBase/Domos.db");
				$aId = $_REQUEST['iId'];
				$aResponse = array();
	
				$aSqlRequest = 'select id,timestamp,value from measures where id = ' . $aId . ' order by timestamp DESC LIMIT 1';
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
			
			case "PING_READ" :
			$aCommandToExecute = 'ping -c 1 -W 2 192.168.0.7';
			$output = array();
			exec($aCommandToExecute, $output, $result);
			print(json_encode($result));

			break;
		}
?>
