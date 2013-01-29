<!DOCTYPE html>
<html>
	<head>
	<meta name="viewport" content="initial-scale=1, maximum-scale=1" charset="utf-8">
		<title>Xbee handler</title>
<link rel="stylesheet" href="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
<script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
<script src="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.js"></script>

		<!--Includes for Mobiscroll-->
		<link href="Libraries/Mobiscroll/css/mobiscroll-2.2.custom.min.css" rel="stylesheet" type="text/css" />
		<script src="Libraries/Mobiscroll/js/mobiscroll-2.2.custom.min.js" type="text/javascript"></script>
		
		<!--Includes for Mobiscroll-->
		<script type="text/javascript" src="Libraries/shawnchin-jquery-cron-v0.1.3.1-0-g9ffb178/gentleSelect/jquery-gentleSelect.js"></script>
<script type="text/javascript" src="Libraries/shawnchin-jquery-cron-v0.1.3.1-0-g9ffb178/cron/jquery-cron.js"></script>

<link type="text/css" href="Libraries/shawnchin-jquery-cron-v0.1.3.1-0-g9ffb178/gentleSelect/jquery-gentleSelect.css" rel="stylesheet" />
<link type="text/css" href="Libraries/shawnchin-jquery-cron-v0.1.3.1-0-g9ffb178/cron/jquery-cron.css" rel="stylesheet" />

 
	</head>
	<body>
	<div data-role="page">
		<div data-role="header">
				<?php
					echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
				?>
		</div>
		<div data-role="content">	
			<a href="charles.php" data-role="button">Charles</a>	
			<a href="salon.php" data-role="button">Salon</a> 
			<a href="entree.php" data-role="button">Entree</a>			
			<a href="SalleDeBain.php" data-role="button">Salle de bain</a>
			<a href="Terasse.php" data-role="button">Terasse</a>
		</div>
		<div data-role="footer" data-id="foo1" data-position="fixed">
	<div data-role="navbar">
		<ul>
			<li><a href="Logs.php">Logs</a></li>
			<li><a href="Cron.php">Cron</a></li>
			<li><a href="At.php">At</a></li>
		</ul>
	</div><!-- /navbar -->
</div><!-- /footer -->
	</div>
	</body>
</html>
