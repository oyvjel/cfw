#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: if_def.pl,v 1.7 2004/09/08 13:18:38 oyvind Exp $


# $ENV{'WEBMIN_CONFIG'} = "/etc/webmin";

# $ENV{'WEBMIN_VAR'} = "/var/webmin";
# $ENV{'SCRIPT_NAME'} = "/cfw/manual.cgi";

$main::no_acl_check++;


require "./fw-lib.pl";
require './obj-lib.pl';


undef $if;
$fwobj = "
interface(
	  name=FW-any-if
	  ip=0.0.0.0
	  location=ALL
	  type=interface
	  netmask=0.0.0.0
	  comment=Automaticly generated firewall object.
)
  
group(
    name=FW
";

   open(FIL, ">>".$config{'objectfile'})  or die "Kan ikke &aring;pne $config{'objectfile'} \n";    
   open(IF, " ifconfig -a |")  or die "Kan ikke &aring;pne ifconfig \n";


while (<IF>) {
#   chop;
   $L=$_;
    if ( $L =~ m/^([a-z0-9:]*) *Link.*/ ) {
#       print "LINE = $L \n";
	&skriv;

       $if = $1;
    }    

    if ( $L =~ m/addr:([0-9.]*) .*/ ) {
	$addr = $1;
    }    
    if ( $L =~ m/cast:([0-9.]*) .*/ ) {
	$bcast = $1;
    }    
    if ( $L =~ m/ask:([0-9.]*).*/ ) {
       	$mask = $1;
#$if = $1;
    }    



#print "\n";
   
}

&skriv;
$fwobj .= ")\n";

print FIL $ifobj;
print FIL $netobj;
print FIL $fwobj;

$fwobj = "
group(
    name=LAN
";
for ($i = 1; $i < $lannr+1; $i++) {
   $fwobj .= "    member=LAN".$i."\n";
            
}
$fwobj .= ")\n";
print FIL $fwobj;



close FIL;
close IF;

&write_file("$module_config_directory/config", \%config);
# &unlock_file("$config_directory/$m/config");

1;
############################################################

sub skriv() {

return if $if eq "lo";
return if $if eq "";
return if $addr eq "";

 $LIF = &get_if_name($if);

if ($LIF) {
  $ifobj .= "interface(
	 type=interface		
       	 name=FW-$LIF
      	 ip=$addr
         location=$location
)\n";

   &wnet;
   $fwobj .= "    member=FW-".$LIF."\n";
   
}
undef $if;
undef $addr;
}

sub wnet() {


($a1,$a2,$a3,$a4)=split('\.',$addr);
($n1,$n2,$n3,$n4)=split('\.',$mask);



$a1=int $a1 & int $n1;
$a2=int $a2 & int $n2;
$a3=int $a3 & int $n3;
$a4=int $a4 & int $n4;

$netobj .= "net(
	 type=net
       	 name=$LIF
      	 ip=$a1.$a2.$a3.$a4
         location=$location
	 netmask=$mask
)\n";
# Internet
   if ( $LIF eq "EXT1" ) {
     $netobj .= "net(
	 type=net
       	 name=INTERNET
      	 ip=0.0.0.0
         location=$location
	 netmask=0.0.0.0
)\n";
   }
}


###############################
sub  get_if_name {
local $i;
   $if = $_[0];
   
   undef $LIF;
   
#   ($i) = split(',',$config{'LAN'});
    if ( $config{'LAN'} =~ m/.*$if.*/ ||($config{'LAN'} eq '' && $if eq "eth1") ) {
	$lannr ++;
	$location="LAN,".$if;
	return "LAN".$lannr;
    }
    if ( $config{'EXT'} =~ m/.*$if.*/ ||($config{'EXT'} eq '' && $if eq "eth0")) {
	$extnr ++;
	$location="EXT,".$if;
	return "EXT".$extnr;
    }
    if ( $config{'DMZ'} =~ m/.*$if.*/ ) {
	$dmznr ++;
	$location="DMZ,".$if;
	return "DMZ".$dmznr;
    }
    if ( $config{'COM'} =~ m/.*$if.*/ ) {
	$comnr ++;
	$location="COM,".$if;
	return "COM".$comnr;
    }

    if ( $if =~ /(ipsec.+)/ ) {
	$comnr ++;
	$ifmod = $1;
	$location="COM,".$ifmod;
#	$config{'COM'} = $ifmod;
	&append_var('COM',$ifmod);
	return "COM".$comnr;
    }
    
    if ( $extnr lt 1 ) { # Første IF = externt hvis ikke allerede definert
             $extnr ++;
             $location="EXT,".$if;
             return "EXT".$extnr;
    }
    
    $lannr ++;
    $ifmod =  $if;
    if ( $if =~ /([a-z]*)/ ) {
	if ( $lannr > 10 ) { $ifmod = "vlan+"; } 
    }else{
        $ifmod = "vlan+"; 
    }
    $location="LAN,".$ifmod;
    &append_var('LAN',$ifmod);
    return "LAN".$lannr;

	  
	
#   if ( $if eq "eth0" ) {   $LIF="LAN"; &wnet; }
#   if ( $if eq "eth1" ) {   $LIF="EXT"; &wnet; }   
#   if ( $if eq "eth2" ) {   $LIF="DMZ"; &wnet; }
#   if ( $if eq "eth3" ) {   $LIF="KOM"; &wnet; }

#  return $LIF;
}

###############################
sub  append_var {
   $var = $_[0];
   $val = $_[1];
    
    
   if (  ! ($config{$var} =~ /$val/) ) { 
       if ( $config{$var} ne "" ) { $config{$var} .= ",";} 
       $config{$var} .= $val;
   }
    return;
}
