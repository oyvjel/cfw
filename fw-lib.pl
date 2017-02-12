#
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: fw-lib.pl,v 1.20 2003/02/05 02:16:19 oyvind Exp $

do '../web-lib.pl';
$|=1;

&init_config();
$configfil=$module_config_directory . "/config";

if (!-e $configfil) {
   open(FIL, ">".$configfil)  or die "Kan ikke &aring;pne" . $configfil ." \n";    
   open(MAL, "config")  or die "Kan ikke &aring;pne config-mal \n";
   while (<MAL>) {
     print FIL;
   }  
   close FIL;
   close MAL;   
   &init_config();
}   

%access=&get_module_acl();
$cl=$text{'config_link'};
$version="0.80.3";

$IPSEC = "/usr/sbin/ipsec";

# $ipchains=($config{'filter_path'}) ? $config{'filter_path'} : "iptables";


if (! $config{'policypath'}) { &error(&text('lib_err_policy', $cl)) }
if (! $config{'rule'}) { &error(&text('lib_err_rf', $cl)) }
#if (! $config{'objectfile'}) { &error(&text('lib_err_of', $cl)) }
#if (! $config{'servicefile'}) { &error(&text('lib_err_sf', $cl)) }
if (! $config{'scriptfile'}) { &error(&text('lib_err_sfcm', $cl)) }
#if (! $config{'vpnfile'}) { &error(&text('lib_err_vf', $text{'config_link'})) }

$config{'rulefile'} = $config{'policypath'} ."/".$config{'rule'};
$config{'objectfile'} = $config{'policypath'} ."/objects";
$config{'servicefile'} = $config{'policypath'} ."/services";
$config{'vpnfile'} = $config{'policypath'} ."/vpn.conf";

if (!-e "$config{'rulefile'}") {
   open(FIL, ">".$config{'rulefile'})  or die "Kan ikke &aring;pne $config{'rulefile'} \n";    
   open(MAL, "rules.def")  or die "Kan ikke &aring;pne rules.def \n";
   while (<MAL>) {
     print FIL;
   }  
   close FIL;
   close MAL;   
}   

if (!-e "$config{'objectfile'}") {
   open(FIL, ">".$config{'objectfile'})  or die "Kan ikke &aring;pne $config{'objectfile'} \n";    
   open(MAL, "objects.def")  or die "Kan ikke &aring;pne objects.def \n";
   while (<MAL>) {
     print FIL;
   }  
   close FIL;
   close MAL;
   
#   &safe_exec("","if_def.pl");

   require "./if_def.pl";
   
}   


if (!-e "$config{'servicefile'}") {
   open(FIL, ">".$config{'servicefile'})  or die "Kan ikke &aring;pne $config{'servicefile'} \n";    
   open(MAL, "services.def")  or die "Kan ikke &aring;pne services.def \n";
   while (<MAL>) {
     print FIL;
   }  
   close FIL;
   close MAL;   
}   

if ( $config{'vpnfile'} && !-e "$config{'vpnfile'}") {
   system( "cp ipsec.conf.def /etc/ipsec.conf") ==0 or die "Can not copy /etc/ipsec.conf";
   system( "cp ipsec.secrets.def /etc/ipsec.secrets") ==0 or die "Can not copy /etc/ipsec.secrets";
   system( "cp vpn.def ". $config{'vpnfile'}) ==0 or die "Can not copy $config{'vpnfile'}";
   
   open(FIL, ">>/etc/ipsec.conf")  or die "Kan ikke &aring;pne /etc/ipsec.conf \n";    
   print FIL "include " . $config{'vpnfile'} ."\n";
   close FIL;

   open(FIL, ">>/etc/ipsec.secrets")  or die "Kan ikke &aring;pne /etc/ipsec.secrets \n";    
   print FIL "include " . $config{'policypath'} ."/my.secrets\n";
   print FIL "include " . $config{'policypath'} ."/my.key\n";
   close FIL;

}   


# Argument with 0, 1 or 2 following words (! is not a word)
@aw0=("-1", "-y", "-f", "-b", "-l");
@aw1=("-N", "-X", "-F", "-j", "-m", "-p", "-i", "-A", "-I", "--icmp-type");
@aw2=("-D", "-R", "-P", "-d", "-s", "-t");

%tos=("0x00" => "TOS Not Set",
      "0x10" => "Minimum Delay",
      "0x08" => "Maximum Throughput",
      "0x04" => "Maximum Reliability",
      "0x02" => "Minimum Cost");

@basechains=("input", "output", "forward");
@policies=("ACCEPT", "DENY", "MASQ", "REJECT", "RETURN", "BLOCK");

ReadParse();



sub safe_exec {
local $tilte,$cmd;
$title = $_[0];
$cmd = $_[1];

print "<h2>". $title ."</h2>\n<pre>";



   &foreign_check("proc") || &error($text{'sman_err_procneeded'});
   &foreign_require("proc", "proc-lib.pl");

   $got = &foreign_call("proc", "safe_process_exec", $cmd ,
                        0, 0, STDOUT, undef, 1);

  print "</pre>\n";

   if ($got) {
    $msg .= "$text{'sman_exec_err'} $got";
   } else {
     $msg .= $text{'sman_exec_ok'};
   }

}


sub toolbar {
print <<EOM;
<center>
<TABLE BORDER=0 WIDTH=80%>
 <TR>
  <TD valign=top ALIGN=center>
   <TABLE BORDER>
     <TR><TD><A HREF="list_objects.cgi"><IMG SRC="images/objects.gif" BORDER=0></A></TD></TR>
   </TABLE>
   <A HREF="list_objects.cgi">$text{'objects'}</A>
  </TD>
  
  <TD valign=top ALIGN=center>
   <TABLE BORDER>
     <TR><TD><A HREF="list_services.cgi"><IMG SRC="images/services.gif" BORDER=0></A></TD></TR>
   </TABLE>
  <A HREF="list_services.cgi">$text{'services'}</A>
  </TD>
  
  <TD valign=top ALIGN=center>
   <TABLE BORDER>
     <TR><TD><A HREF="list_rules.cgi"><IMG SRC="images/rules.gif" BORDER=0></A></TD></TR>
   </TABLE>
  <A HREF="list_rules.cgi">$text{'rules'}</A>
  </TD>
  
  <TD valign=top ALIGN=center>
   <TABLE BORDER>
     <TR><TD><A HREF="script_manager.cgi"><IMG SRC="images/scripts.gif" BORDER=0></A></TD></TR>
   </TABLE>
  <A HREF="script_manager.cgi">$text{'index_scripts'}</A>
  </TD>
    
  <TD valign=top ALIGN=center>
   <TABLE BORDER>
     <TR><TD><A HREF="log_manager.cgi"><IMG SRC="images/log.gif" BORDER=0></A></TD></TR>
   </TABLE>
  <A HREF="log_manager.cgi">$text{'logs'}</A>
  </TD>

EOM

if ( $config{'vpn'} ) {    
  print " <TD valign=top ALIGN=center>
   <TABLE BORDER>
     <TR><TD><A HREF=\"list_tunnels.cgi\"><IMG SRC=\"images/tunnel.gif\" BORDER=0></A></TD></TR>
   </TABLE>
  <A HREF=\"list_tunnels.cgi\">$text{'vpn_index'}</A>
  </TD>\n";
}
print "</TR></TABLE></center>\n";


}

sub tos_select {
 local($rv, $sel);
 $sel=$_[0];

 $rv="<SELECT NAME=\"tos\">\n";

 for (sort keys %tos) {
  $rv.= "<OPTION VALUE=\"$_\"";
  $rv.= ($_ eq $sel) ? " SELECTED" : "";
  $rv.= ">$tos{$_}\n";
 }
 $rv.="</SELECT>\n";

return $rv;
}


sub get_icmptype_list {
 local(@rv, $i);
 if ( ! open (CHILD, "iptables -p icmp -h |") ) {
   print "<h2>Kan ikke &aring;pne iptables -p icmp -h </h2>\n";    
   return ;
   }
  while (<CHILD>) {
   push(@rv, $_);
  }
 close(CHILD);

 for (my $i=0; $i<@rv; $i++) {
  if ($rv[$i] =~ /\(/) {
   $rv[$i] = substr($rv[$i], 0, index($rv[$i], '(')-1);
  }
 }

 while ($rv[0] !~ /Valid ICMP Types/) {
  splice(@rv, 0, 1);
 }
 splice(@rv, 0, 1);

return @rv;
}


sub icmptype_select {
 local($rv, @icmpt, $i, $sel);
 $sel=$_[0];

 $rv="<SELECT NAME=\"icmptype\">\n";
 $rv.="<OPTION VALUE=0>$text{'lib_icmptsel'}\n";
 @icmpt=&get_icmptype_list();
 foreach $i (@icmpt) {
  chomp($i);
  $i =~ s/ //g;
  $rv.= "<OPTION VALUE=\"$i\"";
  $rv.= ($i eq $sel) ? " SELECTED" : "";
  $rv.= ">$i\n";
 }
 $rv.="</SELECT>\n";

return $rv;
}

sub get_proto_list {
 local($file, @rv, $l, @lines);
 $file = ($config{'proto_file'}) ? $config{'proto_file'} : "/etc/protocols";
 
 (-e $file) || &error(&text('lib_err_protomis', $cl));
 
 open(PROTO, $file);
  @lines=<PROTO>;
 close(PROTO);
 @lines = grep(!/^#/, @lines);

 foreach $l (@lines) {
  local(@proto);
   $l =~ s/\t/ /g;
   $l =~ s/ {2,}/ /g;  
   chomp $l;
   next if (!$l);
   @proto=split(/ /, $l);
   push(@rv, $proto[0]);
 }

return sort @rv; 
}

sub proto_select {
 local(@proto, $p, $rv, $sel);
 $sel=$_[0];

 $rv="<SELECT NAME=\"proto\">\n";
 $rv.="<OPTION VALUE=0>Any\n";
 @proto=&get_proto_list();
 foreach $p (@proto) {
  $rv.= "<OPTION VALUE=\"$p\"";
  $rv.= ($p eq $sel) ? " SELECTED" : "";
  $rv.= ">$p\n";
 }
 $rv.="</SELECT>\n";

return $rv;
}

sub get_iface_select {
 local(@act, $rv, $a, $sel);
 $sel=$_[0];

 $rv="<SELECT NAME=\"dev\">\n";
# $rv.="<OPTION VALUE=\"\">Any Device\n";



 if (!$config{'LAN'}) {
    push (@IF,"LAN,eth1");
 } else {
  $a=$config{'LAN'};
  $a=~tr/\s+//;
  @act=split(/,/, $a);
  foreach $a (@act) {
     push (@IF,"LAN,".$a);
  }   
 }


 if (!$config{'EXT'}) {
    push (@IF,"EXT,eth0");
 } else {
  $a=$config{'EXT'};
  $a=~tr/\s+//;
  @act=split(/,/, $a);
  foreach $a (@act) {
     push (@IF,"EXT,".$a);
  }   
 }

 if (!$config{'DMZ'}) {
#    push (@IF,"eth0");
 } else {
  $a=$config{'DMZ'};
  $a=~tr/\s+//;
  @act=split(/,/, $a);
  foreach $a (@act) {
     push (@IF,"DMZ,".$a);
  }   
 }


 if (!$config{'COM'}) {
#    push (@IF,"eth0");
 } else {
  $a=$config{'COM'};
  $a=~tr/\s+//;
  @act=split(/,/, $a);
  foreach $a (@act) {
     push (@IF,"COM,".$a);
  }   
 }

#   push (@IF,"FW,lo");
   push (@IF,"ALL");
  foreach $a (@IF) {
   $rv.="<OPTION VALUE=\"$a\"";
   $rv.=($a eq $sel) ? " SELECTED" : "";
   $rv.=">$a\n";
  }


 $rv.="</SELECT>\n";

return $rv;
}


sub read_script {
 open(SCRIPT, $config{'rulefile'});
  @lines=<SCRIPT>;
 close SCRIPT;
# @lines = grep(!/^#/, @lines);
return @lines;
}


sub parse_line {
  local(%line, $tmpstr, $n);

  $tmpstr=$_[0];
  $n=$_[1];

  chomp($tmpstr);
  $tmpstr =~ s/\t/ /g;       # Convert tabs to spaces
  $tmpstr =~ s/[ ]{2,}/ /g;  # Convert multi-spaces to singel-spaces

  @params=split(/,/, $tmpstr);

    $line{'nr'} = $n;
    $line{'source'} = $params[0];
    $line{'dest'} = $params[1];
    $line{'proto'} = $params[2];
    $line{'frag'} = $params[3];
    $line{'log'} = $params[4];
    $line{'tos'} = $params[5];
    $line{'action'} = $params[6];
    $line{'disable'} = $params[7];
    $line{'comment'} = $params[8];
   
  
return \%line;
#return \@parsedparams;
}

sub parse_script {
 local(@lines, @rv, $tmpstr, $i) ;
 
 @lines=&read_script;
 
 for (my $n=0; $n<@lines; $n++) {
  $tmpstr=@lines[$n];
  next if ($tmpstr =~ /^#/);
  push(@rv, &parse_line($tmpstr, $n));
 }

return @rv;
}


sub object_chooser_button
{
local $form = @_ > 1 ? $_[1] : 0;
return "<input type=button onClick='ifield = document.forms[$form].$_[0]; chooser = window.open(\"object_chooser.cgi\", \"chooser\", \"toolbar=no,menubar=no,scrollbars=yes,width=500,height=300\"); chooser.ifield = ifield' value=\"...\">\n";
}

sub get_services {
 local(@rv, @lines, $l);

 return () if (!-e "/etc/services");
 open(SERVICES, "/etc/services");
  @lines=<SERVICES>;
 close(SERVICES);
 push(@lines, "0:65535 0:65535/tcp # Any Port");
 
 @rv=();

 foreach $l (sort @lines) {
  local(%service);
  next if ($l =~ m/^#/i);
 # chomp $l;
 # $l =~ s/\t/ /g;
 # $l =~ s/[ ]{2,}/ /g;
 # ($service{'name'}, $service{'port'}, $service{'comment'}) = split(/ /, $l,3);
 # ($service{'port'}, $service{'proto'}) = split(/\//, $service{'port'}, 2);
   next if ! (  $l =~ m/^\s*(\S+)\s*(\S+)\/(\S+)\s*(.*)/);
     ($service{'name'}, $service{'port'},$service{'proto'}, $service{'comment'}) = ( $1,$2,$3,$4);
     
   push(@rv, \%service);

 }

return @rv;
}

sub get_services_list {
 local(@rv, @lines, $l);

 return () if (!-e "/etc/services");
 open(SERVICES, "/etc/services");
  @lines=<SERVICES>;
 close(SERVICES);
 push(@lines, "any	0:65535	# Any Port");
 
 @rv=();
 foreach $l (sort @lines) {
  local($name, $rest);
  next if ($l =~ m/^#/i);
  $l =~ s/\t/ /g;
  $l =~ s/[ ]{2,}/ /g;
  ($name, $rest) = split(/ /, $l, 2);
   push(@rv, $name);
 }

return @rv;
}


# service_chooser_button(field, [form])
# Returns HTML for a javascript button for choosing a host
sub service_chooser_button
{
local $form = @_ > 1 ? $_[1] : 0;
return "<input type=button onClick='ifield = document.forms[$form].$_[0]; chooser = window.open(\"service_chooser.cgi\", \"chooser\", \"toolbar=no,menubar=no,scrollbars=yes,width=500,height=300\"); chooser.ifield = ifield' value=\"...\">\n";
}




1;
