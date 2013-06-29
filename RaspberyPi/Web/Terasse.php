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
	
	<div id="TERASSE" data-role="page" data-add-back-btn="true">
	<script type="text/javascript">
    
        function onSuccess(data)
		{
		}

        $(document).ready( function()
		{
			$('#TERASSE').bind('pageshow', function() 
			{
				$.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "20" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "22" , iCmdType : "CMD_READ"}),
                    cache: false,
                    dataType: "json",
                    success: onSuccess
                });
                
                $.ajax(
				{
					type: "POST",
                    url: "./Reader/GateWayReader.php",
                    data: ({iCmdToExecute : "26" , iCmdType : "CMD_READ"}),
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
                    
                    
                    if((obj3.id==22))
                    {
                        $('.Luminosite').append("Derniere luminosite : ");
                        var aIntValue=parseInt(obj3.currentStatus);
                        $('.Luminosite').append(aIntValue);
                        $('.Luminosite').append(" lux releve le : ");
                        $('.Luminosite').append(obj3.LastTMeaureDate["py/repr"]);
                    }
                    
                    if((obj3.id==20))
                    {
                        $('.Temperature').append("Derniere temperature : ");
                        var aIntValue=parseInt(obj3.currentStatus);
                        var aFloat=parseFloat(aIntValue);
                        aFloat=aFloat/10;
                        $('.Temperature').append(aFloat);
                        $('.Temperature').append(" degre releve le : ");
                        $('.Temperature').append(obj3.LastTMeaureDate["py/repr"]);
                    }
                    
                    if((obj3.id==26))
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
            <div data-role="collapsible">
                 <h3>Temperature</h3>
			Temperature :
			<div class="Temperature">
			</div>
            </div>
            
            <div data-role="collapsible">
                 <h3>Humidite</h3>
            Humidite :
			<div class="Humidite">
			</div>
            </div>
            
            <div data-role="collapsible">
                 <h3>Luminosite</h3>
            Luminosite :
			<div class="Luminosite">
			</div>
            </div>
            
		</div>
	</div>
	</body>
</html>
