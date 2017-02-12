#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: rsa_generator.cgi,v 1.9 2003/01/20 12:37:55 oyvind Exp $


require './fw-lib.pl';

	&header();
	print "<script  LANGUAGE=\"Javascript\">\n";
	print "function select(f){\n";
#	print "alert(ifield);\n";
	print "window.opener.document.forms['T'].localkey.value = f;\n";
#      print "ifield.value = f;\n";
	print "top.close();\n";
#	print "return false;\n";
	print "}\n";
	print "</script>\n";
	print "<title>Generate RSA keys</title>\n";

print "<FORM ACTION=\"rsa_generator.cgi\" METHOD=post>";

if ($in{'generate'}) {

#	print "<table width=100%>\n";
    print " Generating keys. This may take some time.........\n<br>";
    open(RSA, "$IPSEC rsasigkey 1024 |") or die " Can not run rsasig";
    #  open(RSA, "ls  |");
    
    @lines=<RSA>;
    close RSA;
    print "..... finished\n<br>";
    
    
    foreach $o (@lines) {
      if ( $o =~ /pubkey=(.*)$/ ){ $key = $1;}
      }
    print "<h1>Generated PUBLIC Key:</h1>\n$key\n<P>\n";
    $file =  $config{'policypath'} ."/my.key.tmp";
    open(KEY, ">" . $file ) or die "Can not open key temporary file";
    
    print KEY ": RSA \t{\n";
    print KEY @lines;
    print KEY "\t}\n";
    close KEY;
    
    print "\n Private key has been saved in $file <p> \n"; 
print "<center>\n";
print "<INPUT TYPE=submit NAME=\"save\" VALUE=\"Save as my.key\">\n";
print "</center><hr>\n";


} elsif ($in{'save'}) {
# Move my.key.tmp to my.key
$filetmp =  $config{'policypath'} ."/my.key.tmp";
$file =  $config{'policypath'} ."/my.key";
system ("mv $filetmp $file") == 0 or die "Can mot move $filetemp to $file \n" ;


}else{

}
#Read my.secret
    print "<h1>PUBLIC Key:</h1>\n";
    $file =  $config{'policypath'} ."/my.key";
    open(KEY, $file ) or print "Can not open key file";
    
    while ( <KEY> ) {
      if ( $_ =~ /pubkey=(.*)$/ ){ $okey = $1;}
    }
    
print "$okey\n<P>\n";
#print "<p><a href=\"\" onClick='return select(\"$okey\", \"$type\")'>Return Key</a>\n";
print "<p><a href=\"javascript:select(\'$okey\')\">Return Key</a>\n";

############  Buttons #######################
if ($in{'generate'}) {
}

print "<center>\n";
print "<INPUT TYPE=submit NAME=\"generate\" VALUE=\"Generate keys\">\n";
print "</center>\n";
print "</FORM><BR><HR>\n";
