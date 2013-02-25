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
                    data: ({iId : '8', iCmdToExecute : "2" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
				
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iId : '20', iCmdToExecute : "2" , iCmdType : "CMD_READ_VALUE_DB"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess4
                });
				
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iId : '21', iCmdToExecute : "2" , iCmdType : "CMD_READ_VALUE_DB"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess4
                });
				
				function onSuccess(data)
				{
					if((data[0].id==8)&&(data[0].status=="on"))
					{
						$('#flip-2').val('on').slider("refresh");
					}
				}
				
				function onSuccess4(data)
				{
				if (data[0]["id"]=="20")
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
		
				$("#Bopen").click(function() 
		{
			var aTypeRequest="temperature";
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iId : '20' ,iCmdToExecute : 'E' , iCmdType : "CMD_X10_READ"}),
				cache: false,
				dataType: "text",
				success:  function(data) {
       onSuccess2(data, aTypeRequest);
     }
			});
        });
		
				$("#BHumidite").click(function() 
		{
			var aTypeRequest="humidite";
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iId : '21' ,iCmdToExecute : 'F' , iCmdType : "CMD_X10_READ"}),
				cache: false,
				dataType: "text",
				success: function(data) {
       onSuccess2(data, aTypeRequest);
     }
			});
        });
		
				function onSuccess2(data,iTypeRequest)
		{
	
		}
		
		
	
		
		$("#VoletUp").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '5' ,iCmdToExecute : '4' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
		
		$("#VoletDown").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '5' ,iCmdToExecute : '2' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
		
		$("#test").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '5' ,iCmdToExecute : '?' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
		
		$( "#flip-2" ).on( 'slidestop', function( event ) 
		{ 
			sVal = $(this).val();
			var theName;
			if (sVal=="on")
			{
				theName = '@';
			}
			else
			{
				theName = 'A';
			}
               $.ajax(
			{
				type: "POST",
                   url: "./Sender/XbeeWrapper.php",
                   data: ({iId : '8' , iStatus : sVal,iCmdToExecute: theName , iCmdType : "CMD_X10"}),
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
			<label for="flip-2">Lumiere auto:</label>
			<select name="flip-2" id="flip-2" data-role="slider">
				<option value="off">Desactiver</option>
				<option value="on">Activer</option>
			</select> 
			<input id="VoletUp" type="button" name="VoletUp" value="Allumer lumiere"/>
			<input id="VoletDown" type="button" name="VoletDown" value="Eteindre lumiere - Beta" disabled/>
			<input id="Bopen" type="button" name="open" value="Refresh Temperature"/>
			Temperature :
			<div class="Temperature">
			</div>
			<input id="BHumidite" type="button" name="huminide" value="Refresh Humidite"/>
			Response :
			<div class="Humidite">
			</div>
		</div>
	</div>
	</body>
</html>
