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
		<div  id="Cron" data-role="page" data-add-back-btn="true" >
		<script type="text/javascript">
	
				$(document).ready( function()
				{
					$('#Cron').bind('pageinit', function() 
					{
						console.log("pageinit");
						$('#selector2').cron(
						{
							onChange: function() 
							{
								$('#example1-val').text($(this).cron("value"));
								console.log("Cron : ", $(this).cron("value"));
							}
						});
					});
				});

				$("#VoletUp").click(function() 
				{
					var ccmd = $("#basic").val();
					console.log("Cmd : ", ccmd);
					var ccmdcomment = $("#comment").val();
					console.log("ccmdcomment : ", ccmdcomment);
					console.log("Cron23 : ", $('#example1-val').text());
					$.ajax(
					{
						type: "POST",
						url: "./Sender/XbeeWrapper.php",
						data: ({iDate : $('#example1-val').text() ,iCmdToExecute : ccmd,iComment : ccmdcomment, iCmdType : "CMD_CRON"}),
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
<?php
					echo "<h2>" ,"Taches prevues :", "</h2>";
$output = shell_exec('crontab -l');
echo "<pre>$output</pre>";
					echo "<h2>" ,"Planifie une tache :", "</h2>";
?>
				

Date:
<div id="selector2"></div>
<div class='example-text' id='example1-val'></div>

				
			
				<div data-role="fieldcontain">
					<label for="basic">Tache:</label>
					<input type="text" name="basic" id="basic" value="" placeholder="Entrer votre tache ici" />
				</div>
				<div data-role="fieldcontain">
					<label for="comment">Commentaire:</label>
					<input type="text" name="comment" id="comment" value="" placeholder="Entrer votre commentaire ici" />
				</div>
				<button name="VoletUp" id="VoletUp">Planifier tache</button>
				
		</div>
	</div>
	</body>
</html>
