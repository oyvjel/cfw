#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: tunnel_edit.cgi,v 1.9 2003/01/21 13:01:52 oyvind Exp $
#


require "./fw-lib.pl";
require "./form_lib.pl";
require "./obj-lib.pl";

if ($in{'rule'} ne "") {
  @lines=&read_script;
  if (!$lines[$in{'rule'}]) { &error("No such rule found") }
  $l=&parse_line($lines[$in{'rule'}]);
}



&header("VPN tunnel" , undef, "vpn", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;


$objects = &get_vpn_objects( "vpnfile" );

$ob = $objects->{$in{'object'}};
#      print $ob->txtout;
  
if (!$ob ) { $ob = service->new(); }

print "<BR><HR>";

 $proto_select=&proto_select($proto);
 $dev_select=&get_iface_select($dev);

$shc=&object_chooser_button("source"); # Source Host Chooser
$dhc=&object_chooser_button("dest"); # Destination Host Chooser
$servch=&service_chooser_button("proto"); 


print "<FORM ACTION=\"save_tunnel.cgi\" METHOD=post NAME=\"T\">";

print <<EOM;

<INPUT TYPE=hidden NAME="object" VALUE="$in{'object'}">
<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>
 <TR>
 
<TH $tb><B>Local</B></TH>
  <TH $tb><B>WAN </B></TH>
  <TH $tb><B>Remote</B></TH>
 </TR>

 <TR>

EOM
#print "<INPUT TYPE=checkbox NAME=\"disable\" VALUE=1 ",
#	($l->{'disable'}) ? "checked" : "" ," > $text{'editrule_disable'}";
#print "</TD>";

print "<TD><TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>
      <tr><th $tb>Network</th><th $tb>Gateway</th></tr>
       <TR><TD>Protected net<br>";
       
print "<INPUT TYPE=text NAME=\"source\" SIZE=15 VALUE=\"",$ob->leftsubnet,"\"> $shc";       

print "<br>Default = Gateway</TD><TD>";

#       $dev_select=&get_iface_select("");

print "<br>IP: <INPUT TYPE=text NAME=\"localIP\" SIZE=15 VALUE=\"", $ob->left , "\">";

# print "<br>REAL IF: $dev_select \n";

print "<br>\n";       
&opt_prompt("vpn_fw");
$rv = "<SELECT NAME=\"vpn_fw\">";
   $rv.="<OPTION VALUE=\"". $config{'policypath'} ."/vpn_if_ud" ."\"";
   $rv.=( $ob->leftupdown ne "" ) ? " SELECTED" : "";
   $rv.=">$text{'yes'}\n";
   $rv.="<OPTION VALUE=\"\"";
   $rv.=("" eq $ob->leftupdown) ? " SELECTED" : "";
   $rv.=">$text{'no'}\n";
 
 $rv.="</SELECT>\n";
print $rv;


print "</TD></TR></TABLE><br>\n";


print "ID: <INPUT TYPE=text NAME=\"localID\" SIZE=25 VALUE=\"",$ob->leftid,"\">";       

print "<br>PUB Key \n";

print "<input type=button onClick='ifield = document.forms[0].localkey; 
         chooser = window.open(\"rsa_generator.cgi\", \"chooser\", \"toolbar=no,menubar=no,scrollbars=yes,width=500,height=300\");
	 chooser.ifield = ifield;
	 chooser.focus();' 
	 value=\"".$text{'vpn_gen_button'}."\">";
	
print "<INPUT TYPE=text NAME=\"localkey\" SIZE=40 VALUE=\"",$ob->leftrsasigkey,"\">";       


print " </TD><TD>\n";

print "<INPUT TYPE=text NAME=\"localNHop\" SIZE=15 VALUE=\"",$ob->leftnexthop,"\">";
print "<br>Local nexthop <HR>
       remote nexthop<br>\n";
print "<INPUT TYPE=text NAME=\"remoteNHop\" SIZE=15 VALUE=\"",$ob->rightnexthop,"\">"; 

print "\n<hr>\n Connection setup";
@IF = ("start","add","ignore");
$rv = "<SELECT NAME=\"auto\">";

  foreach $a (@IF) {
   $rv.="<OPTION VALUE=\"$a\"";
   $rv.=($a eq $ob->auto) ? " SELECTED" : "";
   $rv.=">$a\n";
  }
 $rv.="</SELECT>\n";
print $rv;

print "<br>\n";
&opt_prompt("vpn_auth");

#print "<br>Authentication:\n";
$rv = "<br><SELECT NAME=\"authby\">";
   $rv.="<OPTION VALUE=\"rsasig\"";
   $rv.=("rsasig" eq $ob->authby) ? " SELECTED" : "";
   $rv.=">RSA Key\n";
   $rv.="<OPTION VALUE=\"secret\"";
   $rv.=("secret" eq $ob->authby) ? " SELECTED" : "";
   $rv.=">Secret\n";
 $rv.="</SELECT>\n";
print $rv;

print "<br><input type=button onClick='ifield = document.forms[0].localkey; 
         editor = window.open(\"edit_secret.cgi?leftip=\" + document.forms[0].localIP.value +
	                                       \"&rightip=\" + document.forms[0].remoteIP.value,
	                      \"editor\", \"toolbar=no,menubar=no,scrollbars=yes,width=500,height=300\");
	 editor.focus();'
	 value=\"Enter secret\">";
################
print "</TD>
 <TD>
 <TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>
       <tr><th $tb>Gateway</th><th $tb>Network</th></tr>
<TR><TD>";
print "IP: <INPUT TYPE=text NAME=\"remoteIP\" SIZE=15 VALUE=\"",$ob->right,"\">";
print "</TD><TD>Protected net<br>";

print "<INPUT TYPE=text NAME=\"dest\" SIZE=15 VALUE=\"",$ob->rightsubnet,"\"> $dhc";       

print "<br>Default = Gateway";

print "</TD></TR></TABLE><br>\n";

print "ID: <INPUT TYPE=text NAME=\"remoteID\" SIZE=25 VALUE=\"",$ob->rightid,"\">";       

print "<br>PUB Key (paste from remote)<br>\n";
print "<INPUT TYPE=text NAME=\"remotekey\" SIZE=40 VALUE=\"",$ob->rightrsasigkey,"\">";       

print "</TD> </TR></TABLE>\n";


print "<INPUT TYPE=submit NAME=\"save\" VALUE=\"Save\">\n";
print " as connection  <INPUT TYPE=text NAME=\"newtunnel\" SIZE=15 VALUE=\"",$ob->name,"\"> ";

print "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"Delete\">\n";
print "</FORM><BR><HR>\n";



&footer("./list_rules.cgi", "List rules");



### END of edit_rule.cgi ###.
