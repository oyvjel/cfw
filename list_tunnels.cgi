#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: list_tunnels.cgi,v 1.16 2003/01/20 12:37:55 oyvind Exp $
#


require './fw-lib.pl';
require './obj-lib.pl';

if (! $access{'lvpn'}) { &error($text{'acl_lvpn'} . ": ".$text{'no'} ) }

&header("VPN tunnels", undef, "vpn", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;


$bgc{'add'} = "#A0FFA0";
$bgc{'start'} = "#D0FFE0";
$bgc{'ignore'} = "#d0d0d0";
$bgc{'REJECT'} = "#ffD0c0";
$bgc{'RETURN'} = "#ffFFc0";

print "<center>";
print <<EOM;

<TABLE BORDER=1 WIDTH=80% CELLSPACING=0 CELLPADDING=1 $cb>
<TR>
 <TD $tb><B>$text{'lhosts_names'}</B></TD>
 <TD $tb COLSPAN=1><B>Local</B></TD>
 <TD $tb COLSPAN=1><B>Remote</B></TD>
 <TD $tb COLSPAN=1><B>Action</B></TD>
</TR>
EOM

    $objects = &get_vpn_objects;
    @sok = sort  keys %$objects;
    foreach $o (@sok) {
       	$v = $objects->{$o};

	$name=$v->name;
	$source=$v->left;
	$dest=$v->right;
	$action=($v->auto) ?  $v->auto : "ignore";

        print "<TR bgcolor=$bgc{$action} >";

# print "<TR>\n";
       print "<TD><A HREF=\"tunnel_edit.cgi?object=$name\"> $name </A> </TD>";

print "<TD> $source </TD>";
print "<TD> $dest </TD>";
print "<TD> $action </TD>";
 print "</TR>";
} 


print "</TABLE></center>";



if ($in{'status'}) {
   &safe_exec("IPSEC Status","$IPSEC look");
   &safe_exec("IPSEC Eroute","$IPSEC eroute");
}

if ($in{'restart'}) {

   &ipsec_def;
   system( "cp ipsec.secrets.def /etc/ipsec.secrets") ==0 or die "Can not copy /etc/ipsec.secrets";
#   system( "cp vpn.def ". $config{'vpnfile'}) ==0 or die "Can not copy $config{'vpnfile'}";
   

   open(FIL, ">>/etc/ipsec.secrets")  or die "Kan ikke &aring;pne /etc/ipsec.secrets \n";    
   print FIL "include " . $config{'policypath'} ."/my.secrets\n";
   print FIL "include " . $config{'policypath'} ."/my.key\n";
   close FIL;
   system( "touch $config{'policypath'}/my.secrets");

   if ( !-e "$config{'policypath'}/vpn_if_ud") {
       system( "cp ipsec_updown $config{'policypath'}/vpn_if_ud") == 0 or die "Can not copy $config{'policypath'}/vpn_if_ud";
   }


   if (! $config{'bootloc'}) { &error(&text('lib_err_boot', $text{'config_link'})) }
   if ( !-e "$config{'bootloc'}/cfw_vpn") {
       system( "cp vpnstart.sh $config{'bootloc'}/cfw_vpn") ==0 or die "Can not copy $config{'bootloc'}/cfw_vpn";
   }
   &safe_exec("IPSEC Restart","$config{'bootloc'}/cfw_vpn");
}

if ($in{'stop'}) {
   &safe_exec("IPSEC Stop","$IPSEC setup stop");
}

############  Buttons #######################
print "<center>\n";
print "<A HREF=\"tunnel_edit.cgi\"> New VPN tunnel</A> <P>";
print "<FORM ACTION=\"list_tunnels.cgi\" METHOD=post>";


print "<INPUT TYPE=submit NAME=\"restart\" VALUE=\"Restart VPN\">\n";
print "<INPUT TYPE=submit NAME=\"stop\" VALUE=\"Stop VPN\">\n";

print "<INPUT TYPE=submit NAME=\"status\" VALUE=\"VPN status\">\n";
print "</FORM><BR><HR>\n";

print "\n</center>";

&footer("./", $text{'return_to_top'});

### END of list_hosts.cgi ###.

########################################################
sub ipsec_def {

#  system( "cp ipsec.conf.def /etc/ipsec.conf") ==0 or die "Can not copy /etc/ipsec.conf";

$vpn_if=($config{'vpn_if'}) ? "\"" . $config{'vpn_if'} . "\"" : "%defaultroute";

   open(FIL, ">/etc/ipsec.conf")  or die "Kan ikke &aring;pne /etc/ipsec.conf \n";    
   print FIL "# /etc/ipsec.conf - FreeS/WAN IPSEC configuration file

# basic configuration
config setup
	# THIS SETTING MUST BE CORRECT or almost nothing will work;
	# %defaultroute is okay for most simple cases.
	#interfaces=\"ipsec0=eth0 ipsec1=eth0:0\"
	interfaces=". $vpn_if . "
	klipsdebug=none
	plutodebug=none
	# Use auto= parameters in conn descriptions to control startup actions.
	plutoload=%search
	plutostart=%search



# defaults for subsequent connection descriptions
conn %default
	# How persistent to be in (re)keying negotiations (0 means very).
	keyingtries=2
	# Parameters for manual-keying testing (DON'T USE OPERATIONALLY).
	# Note:  only one test connection at a time can use these parameters!
	spi=0x200
	esp=3des-md5-96
	espenckey=0x01234567_89abcdef_02468ace_13579bdf_12345678_9abcdef0
	espauthkey=0x12345678_9abcdef0_2468ace0_13579bdf
	# If RSA authentication is used, get keys from DNS.
	leftrsasigkey=%dns
	rightrsasigkey=%dns

";

   print FIL "include " . $config{'vpnfile'} ."\n";
   close FIL;


}
