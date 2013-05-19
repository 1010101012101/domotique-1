/*
 *  RGB ColorPicker 1.1
 *  Copyright (c)2006-2007 Bjorge Dijkstra (bjorge@sqweek.com)
 *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy of
 *  this software and associated documentation files (the "Software"), to deal in
 *  the Software without restriction, including without limitation the rights to use,
 *  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
 *  Software, and to permit persons to whom the Software is furnished to do so,
 *  subject to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be included in all
 *  copies or substantial portions of the Software.
 * 
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 *  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 *  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 *  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 *  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 *  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 * 
 *  For more information: http://www.sqweek.com
 *
 *
 */
 
    //
    // consts
    //
    var CP_PAL_WIDTH=280;
    var CP_PAL_HEIGHT=128;    
    var CP_FIELD_INPUT=1;
    var CP_FIELD_ICON=2;
    var CP_FIELD_BOX=4;
    var CP_ICON_URL="rgbcp/edit.png";
    var CP_CUBE_URL="rgbcp/cube-128.png";

    //
    // other globals
    //
    var cpReturnField;
    var cpCurColorCode;    
    
    
    //
    // clamp v so that l <= v <= h
    //
    function cp_clamp_range(v,l,h)
    {
	return (v > h) ? h : (v < l) ? l : v;
    }

    
    //
    // convert n to hex
    //
    function cp_hex(n)
    {
	var digits = "0123456789ABCDEF";
	var n = cp_clamp_range(n,0,255);
	return digits.charAt((n >> 4) & 15) + digits.charAt(n & 15);
    }

    
    //
    //
    //
    function cp_update_color(color)
    {
	var r,g,b;
	
	if (color.length == 6)
	{
	    r = parseInt("0x"+color.substr(0,2));
	    g = parseInt("0x"+color.substr(2,2));
	    b = parseInt("0x"+color.substr(4,2));
	}
	else
	if (color.length == 3)
	{
	    r = parseInt("0x"+color.substr(0,1)+color.substr(0,1));
	    g = parseInt("0x"+color.substr(1,1)+color.substr(1,1));
	    b = parseInt("0x"+color.substr(2,1)+color.substr(2,1));
	}
	else
	{
	    alert('invalid color');
	    return;
	}

	if (isNaN(r) || isNaN(g) || isNaN(b))
	{
	    alert('invalid color');
	    return;
	}
	
	document.getElementById("cp_red").value = r;
	document.getElementById("cp_green").value = g;
	document.getElementById("cp_blue").value = b;
	
	
	cpCurColorCode = color.toUpperCase();
	
	var box = document.getElementById("cp_colorbox");
	box.style.backgroundColor="#"+cpCurColorCode;
	
	document.getElementById("cp_html").value = cpCurColorCode;
	
    }

    
    function cp_html_update()
    {
	cp_update_color(document.getElementById('cp_html').value);
    }

    
    function cp_rgb_update()
    {
	var r,g,b;
	r = document.getElementById('cp_red').value;
	g = document.getElementById('cp_green').value;
	b = document.getElementById('cp_blue').value;
	cp_update_color(cp_hex(r)+cp_hex(g)+cp_hex(b));
    }
    
    
    function cp_get_abs_x(obj,stopobj)
    {
	var offsx = 0;
	while (obj != stopobj)
	{
	    offsx += (obj.offsetLeft - obj.scrollLeft);
	    obj = obj.offsetParent;
	}    
	return offsx;
    }
    
    function cp_get_abs_y(obj, stopobj)
    {
	var offsy = 0;
	while (obj != stopobj)
	{
	    offsy += (obj.offsetTop - obj.scrollTop);
	    obj = obj.offsetParent;
	}    
	return offsy;
    }
    
    function cp_get_scroll_top(obj, stopobj)
    {
	var scrolly = 0;
	while (obj != stopobj)
	{
	    scrolly += obj.scrollTop;
	    obj = obj.offsetParent;
	}    
	return scrolly;
    }
    
    function cp_get_scroll_left(obj, stopobj)
    {
	var scrollx = 0;
	while (obj != stopobj)
	{
	    scrollx += obj.scrollLeft;
	    obj = obj.offsetParent;
	}    
	return scrollx;
    }    

    function cp_get_color(event)
    {
	var red = 0;
	var green = 0;
	var blue = 0;
	var incube = 0;

	//
	// first we need to find out where in the image was clicked
	//
	var obj = document.getElementById("cp_cube");
	var offsx = 0;
	var offsy = 0;
	while (obj)
	{
	    offsx += (obj.offsetLeft - obj.scrollLeft);
	    offsy += (obj.offsetTop - obj.scrollTop);
	    obj = obj.offsetParent;	    
	}
	
	var x = event.clientX - offsx;
	var y = event.clientY - offsy;
	
	//
	// pre calculate some things
	//
	var w = document.getElementById("cp_cube").clientWidth;
	var h = document.getElementById("cp_cube").clientHeight;
	
	var hw = w / 2;
	var qw = w / 4;
	var hh = h / 2;
	var qh = h / 4;
	
	//       G
        //       .
	//      / \
        //   C /   \ Y
	//    |\   /|
        //    | \W/ | 
	//    |  |  |
        //   B \ | / R
	//      \|/
        //       '
	//       M
        //
		
	// edge C-W
	var y_cw_edge = qh + ((x * qh) / hw);
        var x_cw_edge = ((y - qh) * hw) / qh;
	
	// edge B-M
	var y_bm_edge = (h - qh) + ((x * qh) / hw);
	
	// edge C-G
        var y_cg_edge = qh - ((x * qh) / hw);

        // edge W-Y
        var y_wy_edge = hh - (((x - hw) * qh) / hw);
	
	// edge M-R
	var y_mr_edge = h - (((x - hw) * qh) / hw);
	
	// edge G-Y
	var y_gy_edge = ((x - hw) * qh) / hw;
	
	// edge W-M
	var x_wm_edge = hw;
	
	
	if ((x < x_wm_edge) && (y > y_cw_edge) && (y <= y_bm_edge))
	{
	    // left panel
            blue  =  255;
    	    red   = (255 * x) / hw;
	    green = 255 - ((255 * (y - y_cw_edge)) / hh);
	    incube = 1;
	}
	else
	if ((x >= x_wm_edge) && (y > y_wy_edge) && (y <= y_mr_edge))
	{
	    // right panel
    	    red = 255;	
    	    blue = 255 - ((255 * (x - hw)) / hw);
    	    green = 255 - ((255 * (y - y_wy_edge)) / hh);	
	    incube = 1;
	}
	else
	if ( ((x < x_wm_edge) && (y <= y_cw_edge) && (y > y_cg_edge)) ||
	     ((x >= x_wm_edge) && ( y <= y_wy_edge) && (y > y_gy_edge)))
	{
	    // top panel
    	    x_cw = (x + x_cw_edge) / 2;
    	    y_cg = (y + y_cg_edge) / 2;
	    
    	    green = 255;
    	    blue  = (255 * y_cg) / qh;
    	    red   = (255 * x_cw) / hw;	
	    incube = 1;
	}
    
	if (incube)
	{
	    red   = Math.round(cp_clamp_range(red,0,255));
	    green = Math.round(cp_clamp_range(green,0,255));
	    blue  = Math.round(cp_clamp_range(blue,0,255));
	    
	    cp_update_color(cp_hex(red)+cp_hex(green)+cp_hex(blue));
	}
    }	

    function cp_create()
    {
	newHTML = '';
	
	newHTML += "<div id=\"cp_window\" style=\"position:absolute; visibility:hidden;\">";
	newHTML += "<table id=\"cp_table\" cellspacing=\"0\">";
	
	newHTML += "<tr>";
	newHTML += "    <td>";
	newHTML += "        <img id=\"cp_cube\" src=\""+CP_CUBE_URL+"\" onclick=\"cp_get_color(event)\" alt=\"color cube\"/>";
	newHTML += "    </td>";
	newHTML += "    <td rowspan=\"2\">";
	newHTML += "        <div id=\"cp_palette\"></div>";	
	newHTML += "    </td>";
	newHTML += "</tr>";
	
	newHTML += "<tr>";
	newHTML += "    <td>";
	newHTML += "        <div id=\"cp_colorbox\">&nbsp;</div>";
	newHTML += "        <div id=\"cp_animbox\"></div>";
	newHTML += "    </td>";
	newHTML += "    <td colspan=\"2\">";
	newHTML += "        <div style=\"text-align: right;\">";
	newHTML += "            <span class=\"cp_label\">HTML: </span><input class=\"edit\" id=\"cp_html\" type=\"text\" size=\"6\" onchange=\"cp_html_update()\">&nbsp;";
	newHTML += "            <span class=\"cp_label\">RGB: </span>";
	newHTML += "            <input class=\"edit\" id=\"cp_red\" type=\"text\" value=\"0\" size=\"3\" onchange=\"cp_rgb_update()\">";
	newHTML += "            <input class=\"edit\" id=\"cp_green\" type=\"text\" value=\"0\" size=\"3\" onchange=\"cp_rgb_update()\">";
	newHTML += "            <input class=\"edit\" id=\"cp_blue\" type=\"text\" value=\"0\" size=\"3\" onchange=\"cp_rgb_update()\">";
	newHTML += "        </div>";
	newHTML += "    </td>";
	newHTML += "</tr>";
	
	newHTML += "<tr>";
	newHTML += "    <td colspan=\"3\">";
	newHTML += "	     <div>";
	newHTML += "		<input class=\"button\" type=\"button\" value=\"Select\" onclick=\"cp_wrapup();\">&nbsp;";
	newHTML += "		<input class=\"button\" type=\"button\" value=\"Cancel\" onclick=\"cp_hide();\">";
	newHTML += "        </div>";
	newHTML += "    </td>";
	newHTML += "</tr>";	
	newHTML += "</table>";
		
	newHTML += "</div>";
	
	document.write(newHTML);	
    }
    
    function cp_show(event, obj, pal)
    {
	var cp = document.getElementById("cp_window");	
	if (cp.style.visibility == "hidden")
	{	
	    var ev = event.srcElement;
	    if (!ev) ev = event.target;
	    var ax = cp_get_abs_x(ev, undefined);
	    var ay = cp_get_abs_y(ev, undefined);
	    var sy = cp_get_scroll_top(ev, undefined);
	    var sx = cp_get_scroll_left(ev, undefined);
	    var f = document.getElementById(obj);	    
	    cp.style.left = ax + sx + 20;
	    cp.style.top  = ay + sy;
	    cpReturnField = obj;	    
	    if (f && f.value)
	    {
		cp_update_color(f.value);
	    }
	    else
	    {
		cp_update_color("FFFFFF");
	    }
	    cp.style.visibility="visible";
	}
	else
	{
	    cp.style.visibility="hidden";	
	}
    }
        
    function cp_hide()
    {
	var cp = document.getElementById("cp_window");
	cp.style.visibility="hidden";    
    }
    
    function cp_wrapup()
    {

	if (cpReturnField)
	{
	    f=document.getElementById(cpReturnField);
	    if (f) f.value = cpCurColorCode;
	    cp_update_color_box(cpReturnField);
	}
	cp_hide();
    }

    function cp_update_color_box(name)
    {        
        var f = document.getElementById(name);
	if (f)
	{
	    var c = f.value;
    	    f = document.getElementById(name+"_box");
    	    if (f) f.style.backgroundColor="#"+c;
	}
    }
    
    
    function cp_color_field(name, type)
    {
	var f = document.getElementById(name);
	var value = "FFFFFF";
	if (f)
	{
	    if (f.value != '')
	    {	
		value = f.value;
	    }
	    else
	    {
		f.value = value;
	    }
	}
	if (type & CP_FIELD_BOX)
	{
	    document.write("<a href=\"javascript: void(0);\" id=\""+name+"_box\" class=\"cp_color_field_box\" style=\"background-color: #"+value+"\" onclick=\"cp_show(event,'"+name+"','');\">&nbsp;&nbsp;&nbsp;&nbsp;</a>");	
	}        
	if (type & CP_FIELD_ICON)
	{
    	    document.write("<a href=\"javascript: void(0);\" onclick=\"cp_show(event,'"+name+"','');\">");	
	    document.write("<img src=\""+CP_ICON_URL+"\" border=\"0\">");
	    document.write("</a>");	    
	}
    }
    
    