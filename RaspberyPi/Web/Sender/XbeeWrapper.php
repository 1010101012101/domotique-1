<?php
    require '../Const.php';
    $aCmdType = $_REQUEST['iCmdType'];
	
	switch($aCmdType) 
		{
			case "CMD_X10" :
            $aCommandToExecute = WRAPPER2 . "-o " . getenv(REMOTE_ADDR) . " -s " . $_REQUEST["iCmdToExecute"] ;
			$output = array();
			exec($aCommandToExecute, $output);
			print(json_encode($output));
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
		}
?>
