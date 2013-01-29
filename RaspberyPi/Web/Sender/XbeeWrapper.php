<?php
    require '../Const.php';
    $aCmdType = $_REQUEST['iCmdType'];
	
	switch($aCmdType) 
		{
			case "CMD_X10" :
			//$aCommandToExecute = WRAPPER . getenv(REMOTE_ADDR) . ' "1 2 ' . $_REQUEST["iCmdToExecute"] . '"';
			//$aCommandToExecute = WRAPPER . "-o " . getenv(REMOTE_ADDR) . " -s " .' "' . $_REQUEST["iCmdToExecute"] . '"';
			//$aCommandToExecute = "/home/pi/Usb_Arduino_Leonardo/Test.py -s D -t 20 -o TOTO";           OK
			$aCommandToExecute = WRAPPER . "-o " . getenv(REMOTE_ADDR) . " -s " . '"' . $_REQUEST["iCmdToExecute"] . '"';
			//echo exec($aCommandToExecute);
			$output = array();
exec($aCommandToExecute, $output);
//var_dump( $output);
//Response object 
				print(json_encode($output));
			//echo $aCommandToExecute;
			// 1 : on ouvre le fichier
			//$monfichier = fopen('../Logs/logs.txt', 'a+');
			// 2 : on fera ici nos opérations sur le fichier...
			//$aLogTxt = "DATE: " . date("Y-m-d_H:i:s") . " IP: " . getenv(REMOTE_ADDR) . " CMD: " . $aCommandToExecute . "\n";
			//fputs($monfichier, $aLogTxt);
			// 3 : quand on a fini de l'utiliser, on ferme le fichier
			//fclose($monfichier);
			if(isset($_REQUEST['iStatus']))
			{
				try 
				{
					$aId = $_REQUEST['iId'];
					$aStatus = $_REQUEST['iStatus'];
					//connect to SQLite database
					$dbh = new PDO("sqlite:../DataBase/Domos.db");
					$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
					$aSqlRequest = 'update object set status="' . $aStatus . '" where id="' . $aId . '" ';
					$dbh->exec($aSqlRequest);
					//close the database connection
					$dbh = null;
				}
				catch(PDOException $e)
				{
					echo $e->getMessage();
				}
			}
			break;
			
			case "CMD_WOL" :
			$aCommandToExecute = 'sudo /usr/sbin/etherwake 20:cf:30:ca:8a:50';
			echo exec($aCommandToExecute);
			break;
			
			case "CMD_AT" :
			$aDate = $_REQUEST['iDate'];
			$aCmd = $_REQUEST['iCmdToExecute'];
			$aCommandToExecute = 'echo "/home/pi/USB_Leonardo/Wrapper.sh ' . getenv(REMOTE_ADDR) . ' "1 2 ' . $_REQUEST["iCmdToExecute"] . '"" | at ' . $_REQUEST['iDate'];
			echo $aCommandToExecute;
			echo exec($aCommandToExecute);
			break;
			
			case "CMD_CRON" :
			$aDate = $_REQUEST['iDate'];
			$aCmd = $_REQUEST['iCmdToExecute'];
			$aCommandToExecute = 'crontab -l > /tmp/file; echo "#' . $_REQUEST['iComment']  . '">> /tmp/file ; echo "'. $_REQUEST['iDate'] . ' /home/pi/USB_Leonardo/Wrapper.sh ' . getenv(REMOTE_ADDR) . ' \"1 2 ' . $_REQUEST["iCmdToExecute"] . '\"" >> /tmp/file ; crontab /tmp/file';
			echo $aCommandToExecute;
			echo exec($aCommandToExecute);
			break;
			
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
