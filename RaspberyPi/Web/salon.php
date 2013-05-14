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
        
        $("#Button_LightOn").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '3' ,iCmdToExecute : '3' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
        
        $("#Button_SwithTv").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '3' ,iCmdToExecute : '65' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
        
        $("#Button_TvInc").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '3' ,iCmdToExecute : '63' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess
			});
        });
        
        $("#Button_TvDec").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Sender/XbeeWrapper.php",
				data: ({iId : '3' ,iCmdToExecute : '64' , iCmdType : "CMD_X10"}),
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
				data: ({iId : '4' ,iCmdToExecute : '4' , iCmdType : "CMD_X10"}),
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
                    data: ({iCmdToExecute : "13" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "24" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "25" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "6" , iCmdType : "CMD_READ"}),
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
                    
                    if((obj3.id==6)&&(obj3.currentStatus=="on"))
					{
						$('#Flip_HalogeneSalon').val('on').slider("refresh");
					}
                    
                    if((obj3.id==13))
                    {
                        $('.PeopleDetection').append("Derniere detection : ");
                        $('.PeopleDetection').append(obj3.LastTMeaureDate["py/repr"]);
                    }
                    
                    if((obj3.id==24))
                    {
                        $('.Temperature').append("Derniere temperature : ");
                        var aIntValue=parseInt(obj3.currentStatus);
                        var aFloat=parseFloat(aIntValue);
                        aFloat=aFloat/10;
                        $('.Temperature').append(aFloat);
                        $('.Temperature').append(" degre releve le : ");
                        $('.Temperature').append(obj3.LastTMeaureDate["py/repr"]);
                    }
                    
                    if((obj3.id==25))
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
		
	</script>
		<div data-role="header">
			<?php
				echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
			?>
		</div>
		<div data-role="content">	
			<input id="Button_MonterVoletSalon" type="button" name="Button_MonterVoletSalon" value="Monter Volet"/>
			<input id="Button_DescendreVoletSalon" type="button" name="Button_DescendreVoletSalon" value="Descendre Volet"/>
            Temperature :
			<div class="Temperature">
			</div>
            Humidite :
			<div class="Humidite">
			</div>
            PeopleDetection :
			<div class="PeopleDetection">
			</div>
            <input id="Button_LightOn" type="button" name="Button_LightOn" value="Light On"/>
            <input id="Button_LightOff" type="button" name="Button_LightOff" value="Light Off"/>
            <div data-role="controlgroup" data-type="horizontal">
                <input id="Button_SwithTv" type="button" name="Button_SwithTv" value="Switch TV"/>
                <input id="Button_TvInc" type="button" name="Button_TvInc" value="TV++"/>
                <input id="Button_TvDec" type="button" name="Button_TvDec" value="TV--"/>
            </div>
			<label for="Flip_HalogeneSalon">Halogene:</label>
			<select name="Flip_HalogeneSalon" id="Flip_HalogeneSalon" data-role="slider">
				<option value="off">Allumer</option>
				<option value="on">Eteindre</option>
			</select>
		</div>
	</div>
	</body>
</html>
