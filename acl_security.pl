#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: acl_security.pl,v 1.1 2001/02/21 14:32:50 oyvind Exp $
#

require './fw-lib.pl';

# acl_security_form(&options)
# Output HTML for editing security options


sub read_defacl
{
#print " I read_acl \n";
 if ( ! @aclf ) {
# print "Reading acl file \n";
   if ( ! open (ACL, "defaultacl") ) {
      print "<h2>Kan ikke &aring;pne defaultacl </h2>\n";    
      return ;
   }
   while (<ACL>) {

      if ( ($n,$v) = /[ \t]*(\S+)=(.*)/ ) {
#	  print "$n  = $v \n";
	  push(@aclf, $n);
      }
   }  
   close(ACL);
 }
 return \@aclf;
}

sub acl_security_form
{
# print " I acl_security_form ". $_[0]->{'cchains'}."\n";
 &read_defacl;
   foreach $a (@aclf) {
   $t = "acl_".$a;
      print "<TR><TD>". ( $text{$t} ? $text{$t} : $t ) . "</TD>\n";
      print "<TD><INPUT TYPE=radio NAME=\"$a\" VALUE=\"1\"", ($_[0]->{$a}) ? " CHECKED" : "", "> $text{'yes'} ";
      print "<INPUT TYPE=radio NAME=\"$a\" VALUE=\"0\"", ($_[0]->{$a}) ? "" : " CHECKED", "> $text{'no'}</TD></TR>\n";
      
   }
}


# acl_security_save(&options)
# Parse the form for security options
sub acl_security_save
{
   &read_defacl;
   foreach $a (@aclf) {
      $_[0]->{$a} = $in{$a};
   }

}

1;
#&acl_security_form();
### END.

