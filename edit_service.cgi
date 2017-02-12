#!/usr/bin/perl
#
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: edit_service.cgi,v 1.6 2002/12/10 17:35:41 oyvind Exp $


require './fw-lib.pl';
require './obj-lib.pl';



#if ($in{'object'} eq "") { &error($text{'ehost_err_nohost'}) }


&header($text{'eservice_title'}, undef, 'service-edit', undef, undef, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;

print "<center>";
$objects = &get_objects( "servicefile" );

$ob = $objects->{$in{'object'}};
if (!$ob ) { $ob = service->new(); }


print <<EOM;

<FORM ACTION=save_service.cgi METHOD=post>
<INPUT TYPE=hidden NAME="object" VALUE="$in{'object'}">
<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=1 $cb>
 <TR $tb>
  <TD><b>$text{'eservice_header'}</b></TD>
 </TR>
 <TR $cb>
  <TD>
  <TABLE BORDER=0>

EOM

    print "<TR><TD><B>$text{'eservice_name'}:</B></TD>";
    print "<TD><INPUT TYPE=\"text\" NAME=\"names\" SIZE=34 VALUE=\"", $ob->name , "\"></TD></TR>\n";

    if ( $ob->type eq "group" ) {

print "<INPUT TYPE=text NAME=\"members\" SIZE=25 VALUE=\"$members\">";
print &user_chooser_button("members",1 , 0), "</TD>";


    } else {

       $servch=&service_chooser_button("ports"); 
       print "<TR><TD><B>$text{'eservice_ports'}:</B></TD>";
       print "<TD><INPUT TYPE=text NAME=\"ports\" SIZE=15 MAXLENGTH=15 VALUE=\"", $ob->port, "\"> $servch </TD>\n";
      $servch=&service_chooser_button("sports"); 
       print "<TR><TD><B>$text{'eservice_sourceports'}:</B></TD>";
       print "<TD><INPUT TYPE=text NAME=\"sports\" SIZE=15 MAXLENGTH=15 VALUE=\"", $ob->sport, "\"> $servch </TD>\n";

      $proto_select=&proto_select($ob->proto);

      $icmptype_select=&icmptype_select($ob->icmptype);
      $tos_select=&tos_select($ob->tos);
  
       print "<TR><TD><B>$text{'eservice_proto'}:</B></TD>";
###       print "<TD><INPUT TYPE=\"text\" NAME=\"proto\" SIZE=34 VALUE=\"", $ob->proto , "\"></TD></TR>\n";
	print "<TD>$proto_select </TD></TR>";
        print "<TR><TD>ICMP type (if icmp):</TD><TD> $icmptype_select </TD>\n";
	print "</TR><TR><TD>Default TOS ( if not specified in rule:</TD><TD> $tos_select </TD>\n";
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

print "<A HREF=\"delete_service.cgi?object=$in{'object'}\"> Delete $in{'object'} !</A> <P>";

print "\n</center>";
&footer("list_services.cgi", "service list");

### END of edit_host.cgi ###.
