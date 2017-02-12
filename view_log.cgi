#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: view_log.cgi,v 1.10 2002/12/15 20:20:20 oyvind Exp $
#


require "./fw-lib.pl";
require "./obj-lib.pl";

if (! $access{'vlogs'}) { &error($text{'acl_vlogs'} . ": ".$text{'no'} ) }

$Color{'ACCEPT'}="#00aa00";
$Color{'DENY'}="#FF0000";
$Color{'DROP'}="#FF0000";
$Color{'MASQ'}="#0000FF";

   &header($text{'log'}, undef, "log", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

#   print "<HR><pre>\n"; 
#   print  keys %in;
#   print "<HR></pre>\n"; 


$cur = 0;
$lines = 100;


$fpos = 0;


$logfile  = ($config{'logfile'}) ? $config{'logfile'} : "/var/log/messages";


if ( $in{'command'} eq "Follow" ) { 
print <<EOM;
<HEAD>
<TITLE>Firewall Log</TITLE>
<META HTTP-EQUIV="refresh"
   CONTENT="15">
   </HEAD>
   <BODY>
EOM

   open(FILE, "tail -20 $logfile |") || &error($text{'sman_err_read'});	


#   print "<HR><pre>\n"; 
   print "<TABLE border=0 cellpadding=3 cellspacing=1>\n";
   print "<TR $tb> \n";
   print "<TD>Nr</TD>";
   print "<TD>Time</TD>";
   print "<TD>FW</TD>";
   print "<TD>Filter</TD>";
   print "<TD>Action</TD>";
   print "<TD>Proto</TD>";
   print "<TD>Source</TD>";
   print "<TD>S.IF</TD>";
   print "<TD>S.Port</TD>";
   print "<TD>Dest</TD>";
   print "<TD>D.IF</TD>";
   print "<TD>D.port</TD>";
   print "<TD>Flag</TD>";
   print "<TD>Rule</TD>";
   print "</TR>\n";
 
}else{

    open(FILE, "$logfile") || &error($text{'sman_err_read'});	
    $lline = 0;

   if ( $in{'submit'} eq "P" ) {
      $fpos = $in{'line'} - $lines ;
      if ($in{'line'} != $in{'cline'}){
               $fpos = $in{'line'};
      }
      if ( $fpos < 0 ) { $fpos = 0; }
       
   }elsif ( $in{'submit'} eq "N" ) {
         $fpos = $in{'lline'};      
	 
   }elsif ( $in{'submit'} eq "E" ) {
    while (<FILE>) {
        $lline ++;
    }
       seek ( FILE, 0 , 0 );
       $fpos = $lline -10;
       $lline = 0;
	 
   }else{
         $fpos = $in{'line'};      
   }
 
# $lline  = $fpos;
 

#   seek ( FILE, int ($fpos) , 0 );
#    for ($curpos = tell(FILE); $_ = <FILE>; 
#        $cur++ ) {
#	last if $cur
#	print " $curpos , $cur , $fpos <br> \n";
#    }
   
  print "<FORM ACTION=\"view_log.cgi\" METHOD=post>";


#   print "<HR><pre>\n"; 
   print "<TABLE border=0>\n";
   print "<TR $tb> \n";
   print "<TD><INPUT TYPE=submit NAME=\"submit\" VALUE=\"P\">";
   print "<INPUT TYPE=submit NAME=\"submit\" VALUE=\"N\">";
   print "<INPUT TYPE=submit NAME=\"submit\" VALUE=\"E\">";
   print "<INPUT TYPE=hidden NAME=\"cline\"  VALUE=\"$fpos\"></TD>";   

   print "<TD>Time</TD>";
   print "<TD>FW</TD>";
   print "<TD>Filter</TD>";
   print "<TD>Action</TD>";
   print "<TD>Proto</TD>";
   print "<TD>Source</TD>";
   print "<TD>Interf.</TD>";
   print "<TD>S.Port</TD>";
   print "<TD>Dest</TD>";
   print "<TD>Interf.</TD>";
   print "<TD>D.port</TD>";
   print "<TD>Flag</TD>";
   print "<TD>Rule</TD>";
   print "</TR>\n";
 
   print "<TR $tb> \n";
    print "<TD ><INPUT TYPE=text NAME=\"line\" SIZE=6 VALUE=\"$fpos\">";
       print "<INPUT TYPE=submit NAME=\"submit\" VALUE=\"G\"></TD>\n";

   print "<TD><INPUT TYPE=text NAME=\"time\" SIZE=12 VALUE=\"$in{'time'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"FW\" SIZE=5 VALUE=\"$in{'FW'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"filter\" SIZE=8 VALUE=\"$in{'filter'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"action\" SIZE=6 VALUE=\"$in{'action'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"proto\" SIZE=3 VALUE=\"$in{'proto'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"source\" SIZE=14 VALUE=\"$in{'source'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"interf\" SIZE=4 VALUE=\"$in{'interf'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"sport\" SIZE=5 VALUE=\"$in{'sport'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"dest\" SIZE=14 VALUE=\"$in{'dest'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"ointerf\" SIZE=4 VALUE=\"$in{'ointerf'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"dport\" SIZE=5 VALUE=\"$in{'dport'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"flag\" SIZE=3 VALUE=\"$in{'flag'}\"></TD>";
   print "<TD><INPUT TYPE=text NAME=\"rule\" SIZE=2 VALUE=\"$in{'rule'}\"></TD>";
 print "</TR>\n";
   
}   
$mtime = $in{'time'} ?  $in{'time'} : ".*";
$mFW = $in{'FW'} ?  $in{'FW'} : ".*";
$mfilter = $in{'filter'} ?  $in{'filter'} : "\\S*";
$maction = $in{'action'} ?  $in{'action'} : "\\S*";
$minterf = $in{'interf'} ?  $in{'interf'} : "\\S*";
$mointerf = $in{'ointerf'} ?  $in{'ointerf'} : "\\S*";
$mproto = $in{'proto'} ?  $in{'proto'} : "\\S*";
$msource = $in{'source'} ?  $in{'source'} : ".*";
$msport = $in{'sport'} ?  $in{'sport'} : ".*";
$mdest = $in{'dest'} ?  $in{'dest'} : "\\S*";
$mdport = $in{'dport'} ?  $in{'dport'} : "\\S*";
$mflag = $in{'flag'} ?  $in{'flag'} : ".*";
$mrule = $in{'rule'} ?  $in{'rule'} : "\\S*";

$log = "";
    while (<FILE>) {
    
       next if $lline ++ < $fpos -1;
 
#       if ( m/^($mtime) ($mFW) kernel: Packet log ($mfilter) ($maction) ($minterf) PROTO=($mproto) ($msource):($msport) ($mdest):($mdport) L=(.*) S=(.*) I=(.*) F=(.*) T=(\d*) ([SYN]*) ?\(\#($mrule)\)/ ) {
#          ($tid,$fw,$filter,$aksjon,$IF,$prot,$fra,$fraport,$til,$tilport,$l, $s, $i, $f, $t, $syn, $rule) = ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17 );
#       if ( m/^($mtime) ($mFW) kernel: cfw:($maction) (IN=.*)/){

#	if ( m/^($mtime) ($mFW) kernel: cfw:($mfilter):($maction) RULE=($mrule) IN=($minterf) OUT=($mointerf) .*?SRC=($msource) DST=($mdest) .*?PROTO=($mproto) (.*)/){ 
	if ( m/^($mtime) ($mFW) kernel:.* cfw:($mfilter):($maction) RULE=($mrule) IN=($minterf) OUT=($mointerf) .*?SRC=($msource) DST=($mdest) .*?PROTO=($mproto) (.*)/){ 
#	   :($mdport) L=(.*) S=(.*) I=(.*) F=(.*) T=(\d*) ([SYN]*) ?\(\#($mrule)\) PROTO=($mproto)/ ) {
          ($tid,$fw,$filter,$aksjon,$rule,$IF,$OIF,$fra,$til,$prot,$rest) = ($1, $2, $3, $4,$5, $6, $7, $8,$9, $10,$11 );
#	 $tilport,$l, $s, $i, $f, $t, $syn, $rule) 
#	    ($IF,$OIF,$fra,$til,$prot,$fraport,$tilport,$syn) = ("", "", "","" );
#	   my @fields = split(/ /, $rest);
#	   foreach(@fields) {
#	       if(/IN=($minterf)/)  { $IF  = $1 || '?' ; }
#	       if(/OUT=($mout)/)    { $OIF = $1 || '?' ; }
#	       if(/SRC=($msource)/) { $fra = $1 || '?' ; }
#	       if(/DST=($mdest)/)   { $til = $1 || '?' ; }
#
#	       if(/PROTO=($mproto)/)  { $prot  = $1 || '?' ; }
#	       if(/SPT=($msport)/)    { $fraport = $1 || '?' ; }
#	       if(/DPT=($mdport)/)    { $tilport   = $1 || '?' ; }
#	       if(/TYPE=(.*)/)   { $fraport   = "type ".$1 || '?' ; }
#	       if(/CODE=(.*)/)   { $tilport   = "code ".$1 || '?' ; }
#	   }
 
	   
	   
	    ($fraport,$tilport,$flag) = ("", "", "","" );
	   

#	  if ( $prot eq "TCP" || $prot eq "UDP" || $prot eq "ICMP" ) { next; }
	  
	  if ( $prot eq "TCP" || $prot eq "UDP") {
	      if ( $rest =~ /.*SPT=($msport) DPT=($mdport) (.*)/) {
		  ($fraport,$tilport,$rest) = ($1, $2, $3 );
		  if($rest =~ /.* SYN.*/)  { $flag  .= "S" ; }
		  if($rest =~ /.* ACK.*/)  { $flag  .= "A" ; }
		  if($rest =~ /.* FIN.*/)  { $flag  .= "F" ; }
		  if($rest =~ /.* RST.*/)  { $flag  .= "R" ; }
		  if( !($flag =~ /$mflag/) ) { next;}
	      }else{
#		  $fraport = $rest;
		  next;
	      }
	  }
	  elsif ( $prot eq "ICMP" ) {
	      if ( $rest =~ /.*TYPE=(.*?) CODE=(.*?) .*/) {
		  ($fraport,$tilport) = ( "type ".$1, "code ". $2 );
	      }else{
		  $fraport="undefinert type ";
#		  next;
	      }
	  }
	   
          $fg = "<font COLOR=$Color{$aksjon}>";
	  $log .= "<TR>  \n"
	       . "<TD>$fg $lline</TD>"
	       . "<TD>$fg $tid</TD>"
	       . "<TD>$fg $fw</TD>"
	       . "<TD>$fg $filter</TD>"
 	       . "<TD>$fg $aksjon</TD>"
	       . "<TD>$fg $prot</TD>"
	       . "<TD>$fg $fra</TD>"
	       . "<TD>$fg $IF</TD>"
	       . "<TD>$fg $fraport</TD>"
	       . "<TD>$fg $til</TD>"
	       . "<TD>$fg $OIF</TD>"
	       . "<TD>$fg $tilport</TD>"
	       . "<TD>$fg $flag</TD>"
	       . "<TD>$fg $rule</TD>"
	       . "</TR>\n";
  
         last if $cur++ > $lines;
						       
        }						       
	
       if ( m/^($mtime) ($mFW) cfw: ($mfilter): ($maction): (.*)$/ ) {
          ($tid,$fw,$filter,$aksjon,$melding) = ($1, $2, $3, $4, $5 );
          $fg = "<font COLOR=$Color{$filter}>";
	  $log .= "<TR>  \n"
	       . "<TD>$fg $lline</TD>"
	       . "<TD>$fg $tid</TD>"
	       . "<TD>$fg $fw</TD>"
	       . "<TD>$fg $filter</TD>"
	       ." <TD>$fg $aksjon</TD>"
	       . "<TD colspan=7>$fg $melding</TD>"
	       . "</TR>\n";
  
         last if $cur++ > $lines;
						       
        }						       


    }
    $log .= "<TR><TD>EOL</TD></TR>\n" if $cur < $lines;
    print $log;
#   print "</pre><HR>\n";
   print "</TABLE>\n";

   print " <INPUT TYPE=hidden NAME=\"lline\"  VALUE=\"$lline\"></TD>";
   print "\n</FORM>\n";

&footer("./log_manager.cgi" , "log manager");
   exit;

