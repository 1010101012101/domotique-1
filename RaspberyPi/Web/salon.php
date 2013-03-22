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
	
	<div data-role="page" id="salon" data-add-back-btn="true">
	<script type="text/javascript">
	
		
		$("#Button_MonterVoletSalon").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '7' ,iCmdToExecute : '9' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
		
		$("#Button_DescendreVoletSalon").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '7' ,iCmdToExecute : '10' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
		
		$( "#Flip_HalogeneSalon" ).on( 'slidestop', function( event ) 
		{ 
			sVal = $(this).val();
			var theName;
			if (sVal=="on")
			{
				theName = '13';
			}
			else
			{
				theName = '14';
			}
               $.ajax(
			{
				type: "POST",
                   url: "./Sender/XbeeWrapper.php",
                   data: ({iId : '13', iStatus : sVal ,iCmdToExecute: theName , iCmdType : "CMD_X10"}),
                   cache: false,
                   dataType: "text",
                   success: onSuccess
               });		
		});
		
		function onSuccess(data)
		{
		}
		
		$(document).ready( function()
		{
			$('#salon').bind('pageshow', function() 
			{
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iId : '13', iCmdToExecute : "2" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
				
				function onSuccess(data)
				{
					if((data[1].id==13)&&(data[1].status=="on"))
					{
						$('#Flip_HalogeneSalon').val('on').slider("refresh");
					}
				}

            });
        });
		
	</script>
		<div data-role="header">
			<?php
				echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
			?>
		</div>
		<div data-role="content">	
			<input id="Button_MonterVoletSalon" type="button" name="Button_MonterVoletSalon" value="Monter Volet"/>
			<input id="Button_DescendreVoletSalon" type="button" name="Button_DescendreVoletSalon" value="Descendre Volet"/>
			<label for="Flip_HalogeneSalon">Halogene:</label>
			<select name="Flip_HalogeneSalon" id="Flip_HalogeneSalon" data-role="slider">
				<option value="off">Allumer</option>
				<option value="on">Eteindre</option>
			</select> 			
		</div>
	</div>
	</body>
</html>
