#!/usr/bin/perl
#
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: edit_rule.cgi,v 1.4 2002/09/16 14:37:52 oyvind Exp $


require "./fw-lib.pl";

if ($in{'rule'} ne "") {
  @lines=&read_script;
  if (!$lines[$in{'rule'}]) { &error("No such rule found") }
  $l=&parse_line($lines[$in{'rule'}]);
}



&header("edit_rule ". $l{'nr'} , undef, "intro", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;

print $l->{'source'};
print $l->{'disable'};

print "<BR><HR>";

 $proto_select=&proto_select($proto);
 $dev_select=&get_iface_select($dev);

$shc=&object_chooser_button("source"); # Source Host Chooser
$dhc=&object_chooser_button("dest"); # Destination Host Chooser
$servch=&service_chooser_button("proto"); 


print "<FORM ACTION=\"save_rule.cgi\" METHOD=post>";

print <<EOM;
<INPUT TYPE=hidden NAME="rule" VALUE="$in{'rule'}">
<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>
 <TR>
  <TH $tb><B>X</B></TH>  
  <TH $tb><B>$text{'editrule_source'}</B></TH>
  <TH $tb><B>$text{'editrule_dest'}</B></TH>
  <TH $tb><B>$text{'editrule_proto'}</B></TH>
  <TH $tb><B>$text{'editrule_action'}</B></TH>
  <TH $tb><B>$text{'editrule_comment'}</B></TH>  
 </TR>
 <TR>
EOM
#  <TH $tb><B>$text{'editrule_log'}</B></TH>
print "<TD><INPUT TYPE=checkbox NAME=\"disable\" VALUE=1 ",
	($l->{'disable'}) ? "checked" : "" ," > $text{'editrule_disable'}</TD>";
print "<TD>";
#print "<INPUT TYPE=checkbox NAME="sneg" VALUE=1$sneg><B>!</B>";
print "<INPUT TYPE=text NAME=\"source\" SIZE=15 VALUE=\"$l->{'source'}\"> $shc</TD>";

print "<TD>";
#print "$text{'editrule_hostnet'}:<BR><INPUT TYPE=checkbox NAME="dneg" VALUE=1$dneg><B>!</B>";
print "<INPUT TYPE=text NAME=\"dest\" SIZE=15 VALUE=\"$l->{'dest'}\"> $dhc</TD>";

print "<TD>";
#print "$text{'editrule_hostnet'}:<BR><INPUT TYPE=checkbox NAME="dneg" VALUE=1$dneg><B>!</B>";
print "<INPUT TYPE=text NAME=\"proto\" SIZE=15 VALUE=\"$l->{'proto'}\"> $servch";

#print "<TD>";
#print "<INPUT TYPE=checkbox NAME="pneg" VALUE=1$pneg><B>!</B>";
#print " $proto_select</TD>";
#print "<TD><INPUT TYPE=checkbox NAME=\"devneg\" VALUE=1$devneg><B>!</B> $dev_select</TD>


print "<BR><INPUT TYPE=checkbox NAME=\"frag\" VALUE=1 ",
	($l->{'frag'}) ? "checked" : "" ," > $text{'editrule_frag'}</TD>";

print "<TD><SELECT NAME=\"action\">";


# @ps=&parse_script;
# $chains=&find_arg_struct('-N', \@ps);


# print "<OPTION VALUE=\"\"", ($target eq "&nbsp;") ? " selected" : "", ">No jump\n";
# print "<OPTION VALUE=\"port\"", ($redport) ? " selected" : "", ">Port:\n";
 print "<OPTION VALUE=\"DENY\"", ($l->{'action'} eq "DENY") ? " selected" : "", ">DENY\n";
 print "<OPTION VALUE=\"ACCEPT\"", ($l->{'action'} eq "ACCEPT") ? " selected" : "", ">ACCEPT\n";
 print "<OPTION VALUE=\"MASQ\"", ($l->{'action'} eq "MASQ") ? " selected" : "", ">MASQ\n";
 print "<OPTION VALUE=\"REJECT\"", ($l->{'action'} eq "REJECT") ? " selected" : "", ">REJECT\n";
 print "<OPTION VALUE=\"RETURN\"", ($l->{'action'} eq "RETURN") ? " selected" : "", ">RETURN\n";
 print "<OPTION VALUE=\"BLOCK\"", ($l->{'action'} eq "BLOCK") ? " selected" : "", ">BLOCK\n";
 
print "</SELECT>\n";
print "<BR><INPUT TYPE=checkbox NAME=\"log\" VALUE=1 ",
	($l->{'log'}) ? "checked" : "" ," > $text{'editrule_log'}<BR>\n";

$tos_select=&tos_select($tos);
print "$tos_select</TD>";

print "<TD><INPUT TYPE=text NAME=\"comment\" SIZE=15 VALUE=\"$l->{'comment'}\"></TD>";

# $icmptype_select=&icmptype_select($icmptype);
# $spc=&service_chooser_button("sport");
# $dpc=&service_chooser_button("dport");


print "</TABLE>\n";


#if ( $in{'rule'} ) {
# print "<INPUT TYPE=submit NAME=\"save\" VALUE=\" $text{'editrule_save'}\">\n";
#} else {
# print "<INPUT TYPE=submit NAME=\"append\" VALUE=\" $text{'editrule_append'} \">\n";
# print "<INPUT TYPE=submit NAME=\"insert\" VALUE=\" $text{'editrule_insert'} \">\n";
#}

print "<INPUT TYPE=submit NAME=\"save\" VALUE=\" $text{'editrule_save'}\">\n";
print " as rule nr. <INPUT TYPE=text NAME=\"newrule\" SIZE=15 VALUE=\"$in{'rule'}\">( blank = last ) ";

print "<INPUT TYPE=submit NAME=\"delete\" VALUE=\" $text{'editrule_delete'}\">\n";
print "</FORM><BR><HR>\n";



&footer("./list_rules.cgi", "List rules");



### END of edit_rule.cgi ###.
