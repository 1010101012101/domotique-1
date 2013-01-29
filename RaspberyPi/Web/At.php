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
		<div  id="At" data-role="page" data-add-back-btn="true">
		<script type="text/javascript">
	
				$(function()
				{
					var now = new Date();

					$('#i').scroller(
					{
						preset: 'datetime',
						timeWheels: 'hhiiA',
						minDate: new Date(now.getFullYear(), now.getMonth(), now.getDate()),
						theme: 'jqm',
						display: 'modal',
						mode: 'clickpick'
					});  
	
					function onSuccess(data)
					{
					}

					$("#VoletUp").click(function() 
					{
						var date = $("#i").scroller("getDate");
						console.log("Date (raw) : ", date);
						var formatedDate = jQuery.scroller.formatDate('HH:mm mm/dd/y', date);
						console.log("Date (format2) : ", formatedDate);
						var ccmd = $("#basic").val();
						console.log("Cmd : ", ccmd);
		 
						$.ajax(
						{
							type: "POST",
							url: "./Sender/XbeeWrapper.php",
							data: ({iDate : formatedDate ,iCmdToExecute : ccmd , iCmdType : "CMD_AT"}),
							cache: false,
							dataType: "text",
							success: onSuccess
						});
					});
				});
		
	</script>
		<div data-role="header">
				<?php
					echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
				?>
		</div>
		<div data-role="content">	
<?php
					echo "<h2>" ,"Taches prevues :" , "</h2>" ;
					$output = shell_exec('for each in $(atq | cut -f 1 ); do echo "JOB $each";atq | egrep "^$each" ;at -c $each | grep Wrapper ; done');
echo "<pre>$output</pre>";
					echo "<h2>" ,"Planifie une tache :", "</h2>";
?>
				<div data-role="fieldcontain">
					<label for="i">Date:</label>
					<input id="i" name="i" value="" placeholder="Entrez votre date ici"/>
		</div>
				<div data-role="fieldcontain">
					<label for="basic">Tache:</label>
					<input type="text" name="basic" id="basic" value="" placeholder="Entrer votre tache ici"/>
				</div>
				<div data-role="fieldcontain">
					<label for="comment">Commentaire:</label>
					<input type="text" name="comment" id="comment" value="" placeholder="Entrer votre commentaire ici" />
				</div>
			</div>
			<button name="VoletUp" id="VoletUp">Ajouter tache</button>
	</div>
	</body>
</html>
