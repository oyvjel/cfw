#!/usr/bin/perl
# user_chooser.cgi
# This CGI generated the HTML for choosing a user or list of users.
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: object_chooser.cgi,v 1.7 2003/02/05 02:16:19 oyvind Exp $

#require '../web-lib.pl';


require './fw-lib.pl';
require './obj-lib.pl';

#&init_config();
#&ReadParse();


if ($in{'multi'}) {
	# selecting multiple objects.
	if ($in{'frame'} == 0) {
		# base frame
		&PrintHeader();
		$objects = &get_objects;
		$ob = $objects->{$in{'object'}};
		if (!$ob ) { $ob = group->new(); }
                $obname = $in{'object'};
		
                print "<script>\n";
		print "sel = new Array($len);\n";
		print "selr = new Array($len);\n";
		$i=0;
		foreach $m (sort $ob->members) {		
			print "sel[$i] = \"$m\";\n";

                        $o2 = $objects->{$m};
			if ($o2) {
			   $t = $o2->type;
			   print "selr[$i] = \"$t\";\n";
			 } else {
			   print "selr[$i] = \"Warning: Object is undefined\";\n";			 
			 }
			$i++;
			}
		print "</script>\n";
		print "<frameset rows='140,*'>\n";
		print " <frame src=\"object_chooser.cgi?frame=3&object=$obname&multi=1\" scrolling=no>\n";
		print "<frameset cols='50%,50%' frameborder=yes>\n";
		print "<frame src=\"object_chooser.cgi?frame=1&multi=1\">\n";
		print " <frame src=\"object_chooser.cgi?frame=2&multi=1\">\n";
		print "</frameset>\n";
	        print "</frameset>\n";
		}
	elsif ($in{'frame'} == 1) {
		# list of all objects to choose from
		&header();
		print "<script>\n";
		print "function addobject(o, d)\n";
		print "{\n";
		print "top.sel[top.sel.length] = o\n";
		print "top.selr[top.selr.length] = d\n";
		print "top.frames[2].location = top.frames[2].location\n";
		print "return false;\n";
		print "}\n";
		print "</script>\n";
		print "<font size=+1>All Objects</font>\n";
		print "<table width=100%>\n";
		$objects = &get_objects;
		@sok = sort  keys %$objects;
		foreach $o (@sok) {
		   $v = $objects->{$o};
                   $name=$v->name;
	           $type=$v->type;

			print "<tr><td width=20%><a href=\"\" onClick='return addobject(\"$name\", \"$type\")'>$name</a></td>\n";
			print "<td>$type</td> </tr>\n";
			}
		print "</table>\n";
		}
	elsif ($in{'frame'} == 2) {
		# show chosen objects
		&header();
		print "<font size=+1>Selected objects</font>\n";
		print <<'EOF';
<table width=100%>
<script>
function sub(j)
{
sel2 = new Array(); selr2 = new Array();
for(k=0,l=0; k<top.sel.length; k++) {
	if (k != j) {
		sel2[l] = top.sel[k];
		selr2[l] = top.selr[k];
		l++;
		}
	}
top.sel = sel2; top.selr = selr2;
location = location;
return false;
}
for(i=0; i<top.sel.length; i++) {
	document.write("<tr>\n");
	document.write("<td><a href=\"\" onClick='return sub("+i+")'>"+top.sel[i]+"</a></td>\n");
	document.write("<td>"+top.selr[i]+"</td>\n");
	}
</script>
</table>
EOF
		}
	elsif ($in{'frame'} == 3) {
		# output OK and Cancel buttons
		&header();
	    
	    $objects = &get_objects;
	    
	    $ob = $objects->{$in{'object'}};

		print "<FORM ACTION=\"save_object.cgi\" METHOD=post TARGET=_top>\n";
	        print "<center><h1>Object group: $in{'object'}</h1>\n";
	        print "<INPUT TYPE=hidden NAME=\"object\" VALUE=\"$in{'object'}\">\n";
	        print "Save as: <INPUT TYPE=text NAME=\"name\" VALUE=\"$in{'object'}\">\n";		

		print "<INPUT TYPE=hidden NAME=\"members\"  VALUE=\"$members\">";		
#		print "<input type=button value=\"View\" ",
#		      "onClick='members.value = top.sel.join(\" \"); ",
#		      "'>\n";
		print "<input type=button value=\"$text{'button_ok'}\" ",
		      "onClick='members.value = top.sel.join(\" \"); ",
#		      "document.forms[0].target=\"\";",
		      "document.forms[0].submit();",
#		      "top.location=\"index.cgi\";",
		      "'>\n";
		      
		print "<input type=button value=\"$text{'button_cancel'}\" ",
		      "onClick=\"top.location='list_objects.cgi'\">\n";
		print "&nbsp;&nbsp;<input type=button value=\"$text{'button_clear'}\" onClick='top.sel = new Array(); top.selr = new Array(); top.frames[1].location = top.frames[1].location'>\n";

		print "<input type=button value=\"Delete\" ",
		      "onClick=\"top.location='delete_object.cgi?object=$in{object}'\">\n";
	        print "<br>$text{'comment'}: <INPUT TYPE=text NAME=\"comment\" SIZE=55 VALUE=\"", $ob->comment , "\">\n";		

                print "</form>\n";
		}
	}
else {
	# selecting just one user .. display a list of all users to choose from
	&header();
	print "<script>\n";
	print "function select(f,d)\n";
	print "{\n";
	print "top.opener.ifield.value = f;\n";
	print "top.close();\n";
	print "return false;\n";
	print "}\n";
	print "</script>\n";
	print "<title>Select object</title>\n";
	print "<table width=100%>\n";

		$objects = &get_objects;
		@sok = sort  keys %$objects;
		foreach $o (@sok) {
		   $v = $objects->{$o};
                   $name=$v->name;
	           $type=$v->type;

			print "<tr><td width=20%><a href=\"\" onClick='return select(\"$name\", \"$type\")'>$name</a></td>\n";
			print "<td>$type</td> </tr>\n";
	       	}
		print "</table>\n";

	}

