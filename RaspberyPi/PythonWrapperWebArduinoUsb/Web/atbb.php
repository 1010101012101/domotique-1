<!DOCTYPE html>
<html>
<head>

	<meta charset="utf-8" />
		<title>Xbee handler</title>
		<link rel="stylesheet" href="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
		<script src="http://code.jquery.com/jquery-1.8.2.min.js"></script>
		<script src="http://code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.js"></script>


    <!--Includes-->
	<link href="css/mobiscroll-2.2.custom.min.css" rel="stylesheet" type="text/css" />
	<script src="js/mobiscroll-2.2.custom.min.js" type="text/javascript"></script>

    
</head>

<body>
    <div data-role="page" data-add-back-btn="true">
	<script type="text/javascript">

$(function(){
    var now = new Date();


    $('#i').scroller({
        preset: 'datetime',
        minDate: new Date(now.getFullYear(), now.getMonth(), now.getDate()),
        theme: 'jqm',
        display: 'modal',
        mode: 'clickpick'
    });  

	
	$("#VoletUp").click(function() 
		{
		 var date = $("#i").scroller("getDate");
alert(date)
        });
	
	
});

		
		

    </script>
        <div data-role="header">
            <h1>Mobiscroll</h1>
        </div>

        <div data-role="content">
				<input id="i" name="i" />
				<input id="VoletUp" type="button" name="VoletUp" value="Monter Volet"/>
        </div>

	</div>
</body>
</html>
