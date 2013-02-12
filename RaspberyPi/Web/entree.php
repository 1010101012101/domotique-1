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
				
				function onSuccess(data)
				{
					if((data[0].id==8)&&(data[0].status=="on"))
					{
						$('#flip-2').val('on').slider("refresh");
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
				data: ({iId : '20' ,iCmdToExecute : 'F' , iCmdType : "CMD_X10_READ"}),
				cache: false,
				dataType: "text",
				success: function(data) {
       onSuccess2(data, aTypeRequest);
     }
			});
        });
		
				function onSuccess2(data,iTypeRequest)
		{
		
		$('.container').text("DEBUG LOG START");
		$('.container').append(data);
		var reg1=new RegExp("Response : (\d*)","g");
		$('.container').append("DEBUG LOG END --");
		$('.container').append(iTypeRequest);
		var myRegexp = /Response : (\d*)/g;
				var match2 = myRegexp.exec(data);
		//$('.container').append(match2[1]);
		var aIntValue=parseInt(match2[1]);
		var aFloat=parseFloat(aIntValue);
		aFloat=aFloat/10;
		$('.container').append(aFloat);
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
			<input id="VoletUp" type="button" name="VoletUp" value="Allumer lumiere - Beta" disabled/>
			<input id="VoletDown" type="button" name="VoletDown" value="Eteindre lumiere - Beta" disabled/>
			<input id="Bopen" type="button" name="open" value="Temperature"/>
			<input id="BHumidite" type="button" name="huminide" value="Humidite"/>
			Response :
			<div class="container">
			</div>
		</div>
	</div>
	</body>
</html>
