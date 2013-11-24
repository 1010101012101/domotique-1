<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<title>Xbee handler</title>
		<link rel="stylesheet" href="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
		<script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
		<script src="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.js"></script>
	</head>
	
	<body> 
		<div  id="mypage" data-role="page" data-add-back-btn="true">
		<script type="text/javascript">
	
	    $(document).ready( function()
		{
			$('#mypage').bind('pageshow', function() 
			{
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "21" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "23" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "27" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
				
				function onSuccess(data)
				{
                    var aDataReceived = data[0]
                    console.log("aDataReceived: " + aDataReceived)
                    var obj2 = eval("(" + aDataReceived + ')');
                    var obj3 = eval("(" + obj2 + ')');
                    
                    if((obj3.id==21))
                    {
                        $('.Temperature').append("Derniere temperature : ");
                        var aIntValue=parseInt(obj3.currentStatus);
                        var aFloat=parseFloat(aIntValue);
                        aFloat=aFloat/10;
                        $('.Temperature').append(aFloat);
                        $('.Temperature').append(" degre releve le : ");
                        $('.Temperature').append(obj3.LastTMeaureDate["py/repr"]);
                    }
                    console.log("obj3.LastTMeaureDate V1 : " + obj3.LastTMeaureDate)
                    console.log("obj3.LastTMeaureDate V2 : " + Object.keys(obj3.LastTMeaureDate))
                    if((obj3.id==27))
                    {
                        $('.PeopleDetection').append("Derniere detection : ");
                        $('.PeopleDetection').append(obj3.LastTMeaureDate["py/repr"]);
                    }
                    if((obj3.id==23))
                    {
                        $('.Humidite').append("Derniere humidite : ");
                        var aIntValue=parseInt(obj3.currentStatus);
                        var aFloat=parseFloat(aIntValue);
                        aFloat=aFloat/10;
                        $('.Humidite').append(aFloat);
                        $('.Humidite').append(" % humidite relative releve le : ");
                        $('.Humidite').append(obj3.LastTMeaureDate["py/repr"]);
                    }
                    
				}
            });
        });
        
        $("#Button_LightOn").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '46' ,iCmdToExecute : '46' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
        
        $("#Button_LightOff").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '47' ,iCmdToExecute : '47' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
			
		function onSuccess(data)
		{
		}

	</script>
		<div data-role="header">
			<?php
				echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
			?>
		</div>
		<div data-role="content">	
        
            <div data-role="collapsible" data-content-theme="c">
                 <h3>Lumiere</h3>
                <div data-role="controlgroup">
                <input id="Button_LightOn" type="button" name="Button_LightOn" value="Light On"/>
                <input id="Button_LightOff" type="button" name="Button_LightOff" value="Light Off"/>
                </div>
            </div>
            
            <div data-role="collapsible" data-content-theme="c">
                 <h3>Temperature</h3>
                Temperature :
                <div class="Temperature">
                </div>
            </div>
            
            <div data-role="collapsible" data-content-theme="c">
                 <h3>Humidite</h3>
                Humidite :
                <div class="Humidite">
                </div>
            </div>
            
            <div data-role="collapsible" data-content-theme="c">
                 <h3>PeopleDetection</h3>
                PeopleDetection :
                <div class="PeopleDetection">
                </div>
            </div>
            
		</div>
	</div>
	</body>
</html>
