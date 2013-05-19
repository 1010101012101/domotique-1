<html>
 <head>
  <title>PHP Test</title>
    <link rel="stylesheet" type="text/css" href="rgbcp/rgbcp.css"/>
  <script language="javascript" src="rgbcp/rgbcp.js"></script>
 </head>
 <body>
 <?php echo '<p>Hello World</p>'; ?> 

 <input id="example_2" type="text" name="field_name_2" size="6" maxlength="6" onchange="cp_update_color_box(this.id);">
<script language="javascript">cp_color_field('example_2', CP_FIELD_BOX);</script>
 <script language="javascript">cp_create();</script>
 </body>
</html>