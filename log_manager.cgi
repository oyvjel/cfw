#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: log_manager.cgi,v 1.10 2003/03/18 22:25:29 oyvind Exp $
#

require "./fw-lib.pl";

#@ps=&parse_script();
#$chains=&find_arg_struct('-N', \@ps);

&header("Log", undef, "log", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;

print <<EOM;

<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 WIDTH=100%>

  <TD VALIGN=top ALIGN=center>

   <TABLE BORDER=2 CELLSPACING=0 CELLPADDING=2 $cb>
    <TR $tb>
     <TH>$text{'logs'}</TH>
EOM

if ( $config{'vpn'} ) {
   print "<TH>$text{'vpn_index'}</TH>";
}
print <<EOM;
     <TH>$text{'filters'}</TH>
    </TR>
    <TR $cb>
      <FORM ACTION=view_log.cgi METHOD=get>
     <TD>
       <INPUT TYPE=submit VALUE="View" NAME="command">
       <INPUT TYPE=submit VALUE="Follow" NAME="command">
    </TD>
       </FORM>
    
EOM

############  Buttons #######################

print "<FORM ACTION=\"log_manager.cgi\" METHOD=post NAME=\"vpn\">";
if ( $config{'vpn'} ) {
   print "<TD><INPUT TYPE=submit NAME=\"eroute\" VALUE=\"VPN eroute\">\n";
   print "<INPUT TYPE=submit NAME=\"status\" VALUE=\"VPN status\">\n";
   print "</td>\n";
}


print "<td><INPUT TYPE=submit NAME=\"input\" VALUE=\"Input\">\n";
print "<INPUT TYPE=submit NAME=\"forward\" VALUE=\"Forward\">\n";
print "<INPUT TYPE=submit NAME=\"output\" VALUE=\"Output\">\n";
print "<INPUT TYPE=submit NAME=\"allfilt\" VALUE=\"ALL filters\">\n";
print "<INPUT TYPE=submit NAME=\"allnat\" VALUE=\"ALL nat\">\n";
print "<INPUT TYPE=submit NAME=\"reset\" VALUE=\"Reset\">\n";

print "</td></FORM>";

print <<EOM;
    </TD> 
    </TR>
   </TABLE>

  </TD>
 </TR>
</TABLE>
</TR></TABLE>

EOM


################ ACTIONS #######################


if ($in{'status'}) {
   &safe_exec("IPSEC Status","$IPSEC look");
}

if ($in{'eroute'}) {
   &safe_exec("IPSEC Eroute","$IPSEC eroute");
}

if ($in{'input'}) {
   &safe_exec("Input chain","/sbin/iptables -L INPUT -n -v --line-numbers");
}

if ($in{'forward'}) {
   &safe_exec("Forward chain","/sbin/iptables -L FORWARD -n -v --line-numbers");
}

if ($in{'output'}) {
   &safe_exec("Output chain","/sbin/iptables -L OUTPUT -n -v --line-numbers");
}

if ($in{'allfilt'}) {
   &safe_exec("All filters","/sbin/iptables -L -n  -v");
}

if ($in{'allnat'}) {
   &safe_exec("All nat","/sbin/iptables -t nat -L -n  -v");
}


if ($in{'reset'}) {
   &safe_exec("Reset counters","iptables -L -n  -Z ");
}


&footer("./", $text{'return_to_top'});


### END of index.cgi ###.
