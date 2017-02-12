#!/usr/bin/perl
#
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: list_objects.cgi,v 1.8 2003/02/05 02:16:19 oyvind Exp $


require './fw-lib.pl';
require './obj-lib.pl';



&header($text{'lobjects_title'}, undef, "objects", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;

print "<center>";
print <<EOM;
<H3>$text{'lhosts_usrdef'}</H3>

<TABLE BORDER=1 WIDTH=80% CELLSPACING=0 CELLPADDING=1 $cb>
<TR>
  <TD $tb><B>$text{'lhosts_names'}</B></TD>
  <TD $tb><B>$text{'lhosts_type'}</B></TD>
  <TD $tb><B>$text{'lhosts_location'}</B></TD>
  <TD $tb><B>$text{'lhosts_addr'}</B></TD>
  <TD $tb><B>$text{'lhosts_mask'}</B></TD> 
  <TD $tb><B>$text{'comment'}</B></TD> 
</TR>
EOM

    $objects = &get_objects;
    @sok = sort  keys %$objects;
    foreach $o (@sok) {
       	$v = $objects->{$o};

	$name=$v->name;
	$type=$v->type;
	$location=$v->location;


 print "<TR>\n";
    if ( $type eq "group" ) { 
       print "<TD><A HREF=\" object_chooser.cgi?multi=1&object=$name\"> $name </A> </TD>";
    } else {
       print "<TD><A HREF=\"edit_host.cgi?object=$name\"> $name </A> </TD>";
    }
print "<TD> $type </TD>";
print "<TD> $location </TD>";
print "<TD> ".$v->ip." </TD>";
print "<TD> ".$v->netmask." </TD>";
print "<TD> ".$v->comment." </TD>";


 print "</TR>";
} 
#if (!@userhosts) {
# print "<TR><TD COLSPAN=2>$text{'lhosts_nud'}</TD></TR>";
#}

print "</TABLE>";

print "<A HREF=\" object_chooser.cgi?multi=1\"> New group object</A><br>";
print "<A HREF=\"edit_host.cgi\"> New host/net</A> <P>";

print "\n</center>";
&footer("./", $text{'return_to_top'});

### END of list_hosts.cgi ###.
