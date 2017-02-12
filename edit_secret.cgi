#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: edit_secret.cgi,v 1.5 2005/03/22 11:25:27 oyvind Exp $

# user_chooser.cgi
# This CGI generated the HTML for choosing a user or list of users.


require './fw-lib.pl';

if (! $access{'ekeys'}) { &error($text{'acl_ekeys'} . ": ".$text{'no'} ) }

&header("Edit secret" , undef, "vpn_auth", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

print "<title>Edit Preshared Secret</title>\n";

if ( $in{'leftip'} =~ /..?faultroute/ ) {
   print "Use 0.0.0.0 or interface real address and not $in{'leftip'}<br>\n";
   $in{'leftip'} = "0.0.0.0";
}

$lines=&read_file_lines( $config{'policypath'} . "/my.secrets" );
#if (!$$lines[$in{'rule'}]) { &error("No such rule found") }

#$psk = $in{'psk'};

$lip = $in{'leftip'};
$rip = $in{'rightip'};
 $nl = -1;
for ( $i = 0; $i<@{$lines}; $i++) {
    $temp = $lines->[$i];
    if ( $temp =~ /$lip[\t ]+$rip[\t ]+"(.*)"$/ || $temp =~ /$rip[\t ]+$lip[\t ]+"(.*)"$/ ){
#       print " linje $i match:$temp <br>\n";
       $nl = $i;
       $psk = $1;
       last;
    }
}
if ( $nl < 0  ) {  print "Key not found<br>\n";}

#print "<p>Lines: $i , @{$lines} <br>\n ";
print "<FORM ACTION=\"edit_secret.cgi\" METHOD=post>";

if ($in{'delete'} && $nl >= 0) {
      splice (@$lines,$nl,1);
      &flush_file_lines();
      
}elsif ($in{'save'}) {
 
$newline=
#    $in{'nr'}
    "$in{'leftip'}"
    ." $in{'rightip'}"
    ." \"$in{'psk'}\"" ;

$psk = $in{'psk'};
   
   
   if ( $nl < 0  ) {  
       push(@{$lines}, $newline);
   } else {
       $lines->[$i] = $newline;
   }   

   &flush_file_lines();


}elsif ($in{'generate'}) {

    print " Generating keys.........\n<br>";
    open(RSA, "$IPSEC ranbits 512 |") or die " Can not runipsec ranbits";
    #  open(RSA, "ls  |");
    
    $psk=<RSA>;
    close RSA;
    print "..... finished\n<br>";


}

print "ID: <INPUT TYPE=text NAME=\"leftip\" VALUE=\"$in{'leftip'}\">\n";
print "<INPUT TYPE=text NAME=\"rightip\" VALUE=\"$in{'rightip'}\">\n";
print "<INPUT TYPE=submit NAME=\"reload\" VALUE=\"Reload key\">\n";
print "<br>Key:<br><INPUT TYPE=text NAME=\"psk\" VALUE=\"$psk\" SIZE=65>\n";


############  Buttons #######################

print "<center>\n";
print "<INPUT TYPE=submit NAME=\"delete\" VALUE=\"Delete secret\">\n";
print "<INPUT TYPE=submit NAME=\"generate\" VALUE=\"Generate secret\">\n";
print "<INPUT TYPE=submit NAME=\"save\" VALUE=\"Save secret\">\n";
print "</center>\n";
print "</FORM><BR><HR>\n";
