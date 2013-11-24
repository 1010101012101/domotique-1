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
	</script>
		<div data-role="header">
					<?php
						echo "<h1>" , basename($_SERVER['PHP_SELF'], ".php") , "</h1>" ;
					?>
		</div>
		<div data-role="content">	
<?php
$homepage = file_get_contents('./Logs/logs.txt');
echo "<pre>$homepage</pre>";
?>
		</div>
	</div>
	</body>
</html>
