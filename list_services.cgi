#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: list_services.cgi,v 1.5 2002/10/06 21:44:08 oyvind Exp $
#


require './fw-lib.pl';
require './obj-lib.pl';


&header($text{'lservices_title'}, undef, "services", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;
print "<center>";
print <<EOM;
<H3>$text{'lservices_usrdef'}</H3>

<TABLE BORDER=1 WIDTH=80% CELLSPACING=0 CELLPADDING=1 $cb>
<TR>
 <TD $tb><B>'lservices_names'</B></TD>
 <TD $tb COLSPAN=1><B>Type</B></TD>
</TR>
EOM

    $objects = &get_objects( "servicefile" );
    @sok = sort  keys %$objects;
    foreach $o (@sok) {
       	$v = $objects->{$o};

	$name=$v->name;
	$type=$v->type;


 print "<TR>\n";
    if ( $type eq "group" ) { 
       print "<TD><A HREF=\" service_chooser.cgi?multi=1&object=$name\"> $name </A> </TD>";
    } else {
       print "<TD><A HREF=\"edit_service.cgi?object=$name\"> $name </A> </TD>";
    }
print "<TD> $type </TD>";
 print "</TR>";
} 
#if (!@userhosts) {
# print "<TR><TD COLSPAN=2>$text{'lhosts_nud'}</TD></TR>";
#}

print "</TABLE>";

print "<A HREF=\" service_chooser.cgi?multi=1\"> New service group </A><br>";
print "<A HREF=\"edit_service.cgi\"> New service</A> <P>";

print "\n</center>";
&footer("./", $text{'return_to_top'});


### END of list_hosts.cgi ###.
