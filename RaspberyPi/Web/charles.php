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
						$('#Flip_LumierePrincipale').val('on').slider("refresh");
					}
					if((data[2].id==6)&&(data[2].status=="on"))
					{
						$('#Flip_LumiereSecondaire').val('on').slider("refresh");
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
						$('#Flip_PcCharles').val('on').slider("refresh");
					}
				}

            });
        });
		

		$("#Button_AllumerPcCharles").click(function() 
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
		
		$("#Button_MonterVoletCharles").click(function() 
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
		
		$("#Button_DescendreVoletCharles").click(function() 
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

		$( "#Flip_LumierePrincipale" ).on( 'slidestop', function( event ) 
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

		$( "#Flip_LumiereSecondaire" ).on( 'slidestop', function( event ) 
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
			<label for="Flip_LumierePrincipale">Lumiere Principale:</label>
			<select name="Flip_LumierePrincipale" id="Flip_LumierePrincipale" data-role="slider">
				<option value="off">Allumer(5)</option>
				<option value="on">Eteindre(6)</option>
			</select> 
			<label for="Flip_LumiereSecondaire">Lumiere Secondaire:</label>
			<select name="Flip_LumiereSecondaire" id="Flip_LumiereSecondaire" data-role="slider">
				<option value="off">Allumer(;)</option>
				<option value="on">Eteindre(<)</option>
			</select> 
			<label for="Flip_PcCharles">PC Charles (read only - ping) :</label>
			<select name="Flip_PcCharles" id="Flip_PcCharles" data-role="slider" disabled >
				<option value="off">OFF</option>
				<option value="on">ON</option>
			</select> 
			<input id="Button_AllumerPcCharles" type="button" name="Button_AllumerPcCharles" value="Wake up PC"/>
			<input id="Button_MonterVoletCharles" type="button" name="Button_MonterVoletCharles" value="Monter Volet"/>
			<input id="Button_DescendreVoletCharles" type="button" name="Button_DescendreVoletCharles" value="Descendre Volet"/>
		</div>
	</div>
	</body>
</html>
