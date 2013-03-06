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

		
		$("#Bluminosite").click(function() 
		{
			var aTypeRequest="luminere";
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iId : '19' ,iCmdToExecute : 'J' , iCmdType : "CMD_X10_READ"}),
				cache: false,
				dataType: "text",
				success:  function(data) {
       onSuccess(data, aTypeRequest);
     }
			});
        });
		
		
		$("#Bping").click(function() 
		{
			$.ajax(
			{
				type: "POST",
				url: "./Reader/GateWayReader.php",
				data: ({iId : '18' ,iCmdToExecute : 'I' , iCmdType : "CMD_X10_READ"}),
				cache: false,
				dataType: "text",
				success: onSuccess2
			});
        });
		
		function onSuccess(data,iTypeRequest)
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
			<input id="Bluminosite" type="button" name="lumiere" value="Ping avec reponse(debug only)"/>
			Response :
			<div class="container">
			</div>
			<input id="Bping" type="button" name="open" value="Ping sans reponse(debug only)"/>
		</div>
	</div>
	</body>
</html>
