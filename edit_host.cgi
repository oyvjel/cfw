#!/usr/bin/perl
#
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: edit_host.cgi,v 1.6 2003/02/05 02:16:19 oyvind Exp $


require './fw-lib.pl';
require './obj-lib.pl';



#if ($in{'object'} eq "") { &error($text{'ehost_err_nohost'}) }


&header($text{'ehost_title'}, undef, "objects-edit", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});
&toolbar;

$objects = &get_objects;

$ob = $objects->{$in{'object'}};
if (!$ob ) { $ob = host->new(); }


print <<EOM;
<BR>
<center>
<FORM ACTION=save_host.cgi METHOD=post>
<INPUT TYPE=hidden NAME="object" VALUE="$in{'object'}">
<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=1 $cb>
 <TR $tb>
  <TD><b>$text{'ehost_header'}</b></TD>
 </TR>
 <TR $cb>
  <TD>
  <TABLE BORDER=0>

EOM

    print "<TR><TD><B>$text{'ehost_names'}:</B></TD>";
    print "<TD><INPUT TYPE=\"text\" NAME=\"names\" SIZE=34 VALUE=\"", $ob->name , "\"></TD></TR>\n";

    if ( $ob->type eq "group" ) {

print "<INPUT TYPE=text NAME=\"members\" SIZE=25 VALUE=\"$members\">";
print &user_chooser_button("members",1 , 0), "</TD>";

    } else {
       print "<TR><TD><B>$text{'ehost_ip'}:</B></TD>";
       print "<TD><INPUT TYPE=text NAME=\"ip\" SIZE=15 MAXLENGTH=15 VALUE=\"", $ob->ip, "\"> <B>/</B>";
       print "<INPUT TYPE=text NAME=\"netmask\" SIZE=15 MAXLENGTH=15 VALUE=\"",$ob->netmask, "\">";

       $dev_select=&get_iface_select($ob->location);
       print "<TR><TD><B>Location:</B></TD>";
#       print "<TD><INPUT TYPE=\"text\" NAME=\"location\" SIZE=34 VALUE=\"", $ob->location , "\"></TD></TR>\n";
       print "<TD>$dev_select \n";
#
       print "Interface on FW? <INPUT TYPE=checkbox NAME=\"is_if\" VALUE=1",
            ($ob->type eq "interface" ) ? " checked" : "" , "></TD></TR>";
    print "<TR><center><TD><B>$text{'comment'}:</B></TD>";
    print "<TD><INPUT TYPE=\"text\" NAME=\"comment\" SIZE=34 VALUE=\"", $ob->comment , "\"></TD></TR>\n";

}
    print <<EOM;
    </TD>
    <TD ALIGN=right ROWSPAN=2> &nbsp;<INPUT TYPE=submit VALUE=" $text{'ehost_save'} ">&nbsp; </TD></TR>
   
  </TABLE>
  </TD>
 </TR>
</TABLE>
</FORM>
EOM

print "<A HREF=\"delete_object.cgi?object=$in{'object'}\"> Delete $in{'object'} !</A> <P>";

print "\n</center>";
&footer("list_objects.cgi", "object list");

### END of edit_host.cgi ###.
