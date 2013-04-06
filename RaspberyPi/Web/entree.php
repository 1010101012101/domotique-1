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
	
	<div id="entree" data-role="page" id="salon" data-add-back-btn="true">
	<script type="text/javascript">
	
		$(document).ready( function()
		{
			$('#entree').bind('pageshow', function() 
			{			
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : '17', iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess4
                });
				
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : '18' , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess4
                });
				
				function onSuccess4(data)
				{
                    var aDataReceived = data[0]
                    console.log("aDataReceived: " + aDataReceived)
                    var obj2 = eval("(" + aDataReceived + ')');
                    var obj3 = eval("(" + obj2 + ')');

                    if((obj3.id==17))
                    {
                        $('.Temperature').append("Derniere temperature : ");
                        var aIntValue=parseInt(obj3.currentStatus);
                        var aFloat=parseFloat(aIntValue);
                        aFloat=aFloat/10;
                        $('.Temperature').append(aFloat);
                        $('.Temperature').append(" degre releve le : ");
                        $('.Temperature').append(obj3.LastTMeaureDate["py/repr"]);
                    }

                    if((obj3.id==18))
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
		
		$("#Button_RefreshTemperature").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iCmdToExecute : '30' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success:  function(data) 
                {
                    onSuccess2(data);
                }
			});
        });
		
		$("#Button_RefreshHumidite").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iCmdToExecute : '31' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: function(data) 
                {
                    onSuccess2(data);
                }
			});
        });
		
		function onSuccess2(data)
		{
		}
		
		$("#Button_AllumerLumiere").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '5' ,iCmdToExecute : '34' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
		
		$("#Button_EteindreLumiere").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '5' ,iCmdToExecute : '35' , iCmdType : "CMD_X10"}),
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
			<input id="Button_AllumerLumiere" type="button" name="Button_AllumerLumiere" value="Allumer lumiere"/>
			<input id="Button_EteindreLumiere" type="button" name="Button_EteindreLumiere" value="Eteindre lumiere"/>
			<input id="Button_RefreshTemperature" type="button" name="Button_RefreshTemperature" value="Refresh Temperature"/>
			Temperature :
			<div class="Temperature">
			</div>
			<input id="Button_RefreshHumidite" type="button" name="Button_RefreshHumidite" value="Refresh Humidite"/>
			Humidite :
			<div class="Humidite">
			</div>
		</div>
	</div>
	</body>
</html>
