#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: list_rules.cgi,v 1.17 2004/11/08 11:35:59 oyvind Exp $
#

require "./fw-lib.pl";
require './obj-lib.pl';


if (! $access{'lrules'}) { &error($text{'lrules_err_acl'}) }


&header("Regelsett", undef, "regelsett", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});


&toolbar;

@ps=&parse_script();


$bgc{'ACCEPT'} = "#A0FFA0";
$bgc{'MASQ'} = "#D0FFE0";
$bgc{'DENY'} = "#ffA0A0";
$bgc{'REJECT'} = "#ffD0c0";
$bgc{'RETURN'} = "#ffFFc0";
$bgc{'BLOCK'} = "#00ffff";

# print @ps;

    $objects = &get_objects;
    $services = &get_objects( "servicefile" );		

print "<BR><HR>";

print "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n";
#print "<TR><TD COLSPAN=9 $tb WIDTH=100%><B>$text{'erule_title'}</B></TD></TR>\n";

print "<TR $tb><TD><B>Nr.</B></TD>";
print "<TD><B>$text{'erule_source'}</B></TD>";
print "<TD><B>$text{'erule_dest'}</B></TD>";

print "<TD><B>Service</B></TD>";

print "<TH><B>$text{'erule_frag'}</B></TD>";
print "<TH><B>$text{'erule_log'}</B></TD>";
print "<TD><B>$text{'erule_tos'}</B></TD>";

print "<TD><B>$text{'erule_action'}</B></TD>";
print "<TD ALIGN=right><B>$text{'erule_comment'}</B></TD></TR>\n";


foreach $l (@ps) {

  $line=$l->{'nr'};

 $source=$l->{'source'};
 $source || ($source = "&nbsp;");

 $dest=$l->{'dest'};
 $dest || ($dest = "&nbsp;");

 $proto=($l->{'proto'}) ?  $l->{'proto'} : "Any";
  $action=($l->{'action'}) ?  $l->{'action'} : "Drop";

 $frag=($l->{'frag'}) ?  "X" : "&nbsp;";

 $log=($l->{'log'}) ? "X" : "&nbsp;";

 $tos=($l->{'tos'}) ? "$tos{$l->{'tos'}}" : "&nbsp;";

 $disable=$l->{'disable'};

 $comment=$l->{'comment'};
 $comment || ($comment = "&nbsp;");
if ( $comment =~ /.*BLOCKLIST_RULESET.*/ ) {
    $blocklist=1;
    }
    
if ( $l->{'disable'} ) {
 print "<TR bgcolor=#a0a0a0  >";
 $action .= " (SKIPPED)"
}else{
# print "<TR $cb >";
 print "<TR bgcolor=$bgc{$action} >";
}

 print "<TD><A HREF=\"edit_rule.cgi?rule=$line\">$line</A></TD>";


$v = $objects->{$source};
if (! $v ) {
   print "<TD >$source</TD>";
} else {
    $type=$v->type;

    if ( $type eq "group" ) { 
       print "<TD><A HREF=\" object_chooser.cgi?multi=1&object=$source\"> $source </A> </TD>";
    } else {
       print "<TD><A HREF=\"edit_host.cgi?object=$source\"> $source </A> </TD>";
    }
}
#

$v = $objects->{$dest};
if (! $v ) {
   print "<TD >$dest</TD>";
} else {
    $type=$v->type;

    if ( $type eq "group" ) { 
       print "<TD><A HREF=\" object_chooser.cgi?multi=1&object=$dest\"> $dest </A> </TD>";
    } else {
       print "<TD><A HREF=\"edit_host.cgi?object=$dest\"> $dest </A> </TD>";
    }
}

$v = $services->{$proto};
if (! $v ) {
   print "<TD >$proto</TD>";
} else {
    $type=$v->type;

    if ( $type eq "group" ) { 
       print "<TD><A HREF=\" service_chooser.cgi?multi=1&object=$proto\"> $proto </A> </TD>";
    } else {
       print "<TD><A HREF=\"edit_service.cgi?object=$proto\"> $proto </A> </TD>";
    }
}

 print "<TD ALIGN=center><B>$frag</B></TD>";
 print "<TD ALIGN=center><B>$log</B></TD>";
 print "<TD >$tos</TD>";

 print "<TD >$action</TD>";
 print "<TD >$comment</TD>";
 print "</TR>\n";
}


print "</TABLE>\n";

print "<BR><BR>\n";
print "<A HREF=\"edit_rule.cgi?chain=$in{'chain'}\">$text{'erule_crule'}</A>\n";
print "<HR>\n";




if ($in{'status'}) {

   &safe_exec("IPSEC Status","$IPSEC look");
   &safe_exec("IPSEC Eroute","$IPSEC eroute");
}

if ($in{'install'}) {
require "./lv-lib.pl";

    if ( -l $config{'scriptfile'}) {
	`rm -f $config{'scriptfile'}`;
	$msg .= "Symlink ".$config{'scriptfile'} ." deleted<br>\n";
    }
    
    &generate_fw_script;
    
    if (!-x $config{'scriptfile'}) {
	chmod 0755, $config{'scriptfile'};
	$msg="$text{'sman_msg_exec'}<BR>";
    }

    &safe_exec("Restart FW",$config{'scriptfile'});
    print $msg;
    $msg = "VPN: ";

   if ( -x "$config{'bootloc'}/cfw_vpn") {
     &safe_exec("IPSEC Restart","$config{'bootloc'}/cfw_vpn");
   }
#      print $msg;
}

############  Buttons #######################
print "<center>\n";
if ( $blocklist ) {
    print " Blocklist ruleset. Do not install as main ruleset<br>";
    }else{
	print "<FORM ACTION=\"list_rules.cgi\" METHOD=post>";


	print "<INPUT TYPE=submit NAME=\"install\" VALUE=\"Install ruleset\">\n";
	if ( $config{'vpn'} ) {
	    print "<INPUT TYPE=submit NAME=\"status\" VALUE=\"VPN status\">\n";
	}
	print "</FORM><BR><HR>\n";
    }
print "\n</center>";


&footer("", $text{'erule_return'});



### END of edit_chain.cgi ###.
