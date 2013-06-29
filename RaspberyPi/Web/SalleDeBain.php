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
	<div id="SDB" data-role="page" data-add-back-btn="true">
        <script type="text/javascript">
        
            $(document).ready( function()
            {
                $('#SDB').bind('pageshow', function() 
                {
                    $.ajax(
                    {
                        type: "POST",
                        url: "./Reader/GateWayReader.php",
                        data: ({iId : '9', iCmdToExecute : "2" , iCmdType : "CMD_READ"}),
                        cache: false,
                        dataType: "json",
                        success: onSuccess
                    });
                    
                    function onSuccess(data)
                    {
                        if((data[0].id==9)&&(data[0].status=="on"))
                        {
                            $('#Flip_ChauffageSdb').val('on').slider("refresh");
                        }
                    }
    
                });
            });
            
            $( "#Flip_ChauffageSdb" ).on( 'slidestop', function( event ) 
            { 
                sVal = $(this).val();
                var theName;
                if (sVal=="on")
                {
                    theName = '42';
                }
                else
                {
                    theName = '43';
                }
                $.ajax(
                {
                    type: "POST",
                    url: "./Sender/XbeeWrapper.php",
                    data: ({iId : '9', iStatus : sVal ,iCmdToExecute: theName , iCmdType : "CMD_X10"}),
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
            <div data-role="collapsible">
                 <h3>Temperature</h3>
			<label for="Flip_ChauffageSdb">Chauffage:</label>
			<select name="Flip_ChauffageSdb" id="Flip_ChauffageSdb" data-role="slider">
				<option value="off">Desactiver</option>
				<option value="on">Activer</option>
			</select> 	
            </div>            
		</div>
	</div>
	</body>
</html>
