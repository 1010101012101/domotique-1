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

		
		$("#Button_PingAvecReponse").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iCmdToExecute : '39' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success:  function(data) 
                {
                    onSuccess(data);
                }
			});
        });
		
		$("#Button_PingSansReponse").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iCmdToExecute : '40' , iCmdType : "CMD_X10"}),
				cache: false,
				dataType: "text",
				success: onSuccess2
			});
        });
		
		function onSuccess(data)
		{
            $('.container').text("DEBUG LOG START");
            $('.container').append(data);
		}
		
		function onSuccess2(data)
		{
		}
		
	</script>
		<div data-role="header">
			<?php
				echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
			?>
		</div>
		<div data-role="content">
		PAGE DE TEST--le capteur est dans ma chambre en ce moment est pas encore sur la terrasse
			<input id="Button_PingAvecReponse" type="button" name="Button_PingAvecReponse" value="Ping avec reponse(debug only)"/>
			Response :
			<div class="container">
			</div>
			<input id="Button_PingSansReponse" type="button" name="Button_PingSansReponse" value="Ping sans reponse(debug only)"/>
		</div>
	</div>
	</body>
</html>
