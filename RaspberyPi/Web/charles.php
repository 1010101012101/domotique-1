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
                    data: ({iId : '4,5,6', iCmdToExecute : "2" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
				
				function onSuccess(data)
				{
					if((data[0].id==4)&&(data[0].status=="on"))
					{
						$('#flip-1').val('on').slider("refresh");
					}
					if((data[2].id==6)&&(data[2].status=="on"))
					{
						$('#flip-2').val('on').slider("refresh");
					}
				}
				
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iId : '4,5,6', iCmdToExecute : "2" , iCmdType : "PING_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess2
                });
				
				function onSuccess2(data)
				{
					if(data=="0")
					{
						$('#flip-3').val('on').slider("refresh");
					}
				}

            });
        });
		

		$("#Bopen").click(function() 
		{
			$.ajax(
			{
				type: "POST",
                   url: "./Sender/XbeeWrapper.php",
                   data: ({iCmdType : "CMD_WOL"}),
                   cache: false,
                   dataType: "text",
                   success: onSuccess
            });
        });
		
		$("#VoletUp").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '5' ,iCmdToExecute : '7' , iCmdType : "CMD_X10"}),
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
				data: ({iId : '5' ,iCmdToExecute : '8' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
			
		function onSuccess(data)
		{
		}

		$( "#flip-1" ).on( 'slidestop', function( event ) 
		{ 
			sVal = $(this).val();
			var theName;
			if (sVal=="on")
			{
				theName = '5';
			}
			else
			{
				theName = '6';
			}
               $.ajax(
			{
				type: "POST",
                   url: "./Sender/XbeeWrapper.php",
                   data: ({iId : '4' , iStatus : sVal,iCmdToExecute: theName , iCmdType : "CMD_X10"}),
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
				theName = ';';
			}
			else
			{
				theName = '<';
			}
               $.ajax(
			{
				type: "POST",
                   url: "./Sender/XbeeWrapper.php",
                   data: ({iId : '6', iStatus : sVal ,iCmdToExecute: theName , iCmdType : "CMD_X10"}),
                   cache: false,
                   dataType: "text",
                   success: onSuccess
               });		
		});

   
		
	</script>
		<div data-role="header">
			<?php
				echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
			?>
		</div>
		<div data-role="content">	
			<label for="flip-1">Lumiere Principale:</label>
			<select name="flip-1" id="flip-1" data-role="slider">
				<option value="off">Allumer(5)</option>
				<option value="on">Eteindre(6)</option>
			</select> 
			<label for="flip-2">Lumiere Secondaire:</label>
			<select name="flip-2" id="flip-2" data-role="slider">
				<option value="off">Allumer(;)</option>
				<option value="on">Eteindre(<)</option>
			</select> 
			<label for="flip-3">PC Charles (read only - ping) :</label>
			<select name="flip-3" id="flip-3" data-role="slider" disabled >
				<option value="off">OFF</option>
				<option value="on">ON</option>
			</select> 
			<input id="Bopen" type="button" name="open" value="Wake up PC"/>
			<input id="VoletUp" type="button" name="VoletUp" value="Monter Volet(7)"/>
			<input id="VoletDown" type="button" name="VoletDown" value="Descendre Volet(8)"/>
		</div>
	</div>
	</body>
</html>
