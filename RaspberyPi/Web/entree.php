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
                    data: ({iId : '8', iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
				
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iId : '30', iCmdType : "CMD_READ_VALUE_DB"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess4
                });
				
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iId : '31' , iCmdType : "CMD_READ_VALUE_DB"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess4
                });
				
				function onSuccess(data)
				{
					if((data[0].id==8)&&(data[0].status=="on"))
					{
						$('#Flip_LumiereAuto').val('on').slider("refresh");
					}
				}
				
				function onSuccess4(data)
				{
                    if (data[0]["id"]=="30")
                    {
                        $('.Temperature').append("Derniere temperature : ");
                        var aIntValue=parseInt(data[0]["value"]);
                        var aFloat=parseFloat(aIntValue);
                        aFloat=aFloat/10;
                        $('.Temperature').append(aFloat);
                        $('.Temperature').append(" degre releve le : ");
                        $('.Temperature').append(data[0]["timestamp"]);
                    }
                    else
                    {
                        $('.Humidite').append("Derniere humidite : ");
                        var aIntValue=parseInt(data[0]["value"]);
                        var aFloat=parseFloat(aIntValue);
                        aFloat=aFloat/10;
                        $('.Humidite').append(aFloat);
                        $('.Humidite').append(" % humidite relative releve le : ");
                        $('.Humidite').append(data[0]["timestamp"]);
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
				data: ({iCmdToExecute : '30' , iCmdType : "CMD_X10_READ"}),
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
				data: ({iCmdToExecute : '31' , iCmdType : "CMD_X10_READ"}),
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
		
		$( "#Flip_LumiereAuto" ).on( 'slidestop', function( event ) 
		{ 
			sVal = $(this).val();
			var theName;
			if (sVal=="on")
			{
				theName = '37';
			}
			else
			{
				theName = '38';
			}
               $.ajax(
                {
				type: "POST",
                   url: "./Sender/XbeeWrapper.php",
                   data: ({iId : '8' , iStatus : sVal, iCmdToExecute: theName , iCmdType : "CMD_X10"}),
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
			<label for="Flip_LumiereAuto">Lumiere auto:</label>
			<select name="Flip_LumiereAuto" id="Flip_LumiereAuto" data-role="slider">
				<option value="off">Desactiver</option>
				<option value="on">Activer</option>
			</select> 
			<input id="Button_AllumerLumiere" type="button" name="Button_AllumerLumiere" value="Allumer lumiere"/>
			<input id="Button_EteindreLumiere" type="button" name="Button_EteindreLumiere" value="Eteindre lumiere"/>
			<input id="Button_RefreshTemperature" type="button" name="Button_RefreshTemperature" value="Refresh Temperature"/>
			Temperature :
			<div class="Temperature">
			</div>
			<input id="Button_RefreshHumidite" type="button" name="Button_RefreshHumidite" value="Refresh Humidite"/>
			Response :
			<div class="Humidite">
			</div>
		</div>
	</div>
	</body>
</html>
