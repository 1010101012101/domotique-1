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
                    data: ({iCmdToExecute : "1" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "3" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "15" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "19" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "16" , iCmdType : "CMD_READ"}),
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
                    
                    //console.log("Object.keys(obj3) : " + Object.keys(obj3))

                    if((obj3.id==1)&&(obj3.currentStatus=="on"))
					{
						$('#Flip_LumierePrincipale').val('on').slider("refresh");
					}
                    if((obj3.id==3)&&(obj3.currentStatus=="on"))
					{
						$('#Flip_LumiereSecondaire').val('on').slider("refresh");
					}
                    if((obj3.id==19)&&(obj3.currentStatus=="on"))
					{
						$('#Flip_PcCharles').val('on').slider("refresh");
					}
                    //var obj = JSON.parse(aDataReceived);
                    if((obj3.id==15))
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
                    if((obj3.id==16))
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
		
        $( "#Flip_PcCharles" ).on( 'slidestop', function( event ) 
		{ 
			sVal = $(this).val();
			var theName;
			if (sVal=="on")
		{
				theName = '60';
			}
			else
			{
				theName = '62';
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
				theName = '11';
			}
			else
			{
				theName = '12';
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
				<option value="off">Allumer</option>
				<option value="on">Eteindre</option>
			</select> 
			<label for="Flip_LumiereSecondaire">Lumiere Secondaire:</label>
			<select name="Flip_LumiereSecondaire" id="Flip_LumiereSecondaire" data-role="slider">
				<option value="off">Allumer</option>
				<option value="on">Eteindre</option>
			</select> 
			<label for="Flip_PcCharles">PC Charles (read only - ping) :</label>
			<select name="Flip_PcCharles" id="Flip_PcCharles" data-role="slider" >
				<option value="off">OFF</option>
				<option value="on">ON</option>
			</select> 
			<input id="Button_MonterVoletCharles" type="button" name="Button_MonterVoletCharles" value="Monter Volet"/>
			<input id="Button_DescendreVoletCharles" type="button" name="Button_DescendreVoletCharles" value="Descendre Volet"/>
            Temperature :
			<div class="Temperature">
			</div>
            Humidite :
			<div class="Humidite">
			</div>
		</div>
	</div>
	</body>
</html>
