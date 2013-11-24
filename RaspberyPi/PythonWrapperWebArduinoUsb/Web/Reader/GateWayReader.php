<?php
	require '../Const.php';
    $aCmdType = $_REQUEST['iCmdType'];
	
	switch($aCmdType) 
		{            
            case "CMD_READ" :
            $aCommandToExecute = WRAPPER2 . "-o " . getenv(REMOTE_ADDR) . " -s " . $_REQUEST["iCmdToExecute"] . " -t READ";
			$output = array();
			exec($aCommandToExecute, $output);
			print(json_encode($output));
			break;
		}
?>
