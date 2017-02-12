#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: text_find.pl,v 1.2 2000/12/14 01:17:02 oyvind Exp $


do '../web-lib.pl';
$|=1;


#&init_config();
#%access=&get_module_acl;

$default_lang = "dev";
%text =  &load_language();

$cl=$text{'config_link'};
#print  "Forfatter: ".$text{'author'};

#print $1;
#open(FTFIL, "$fratilfil") or print "Kan ikke åpne $fratilfil\n";    
while (<>) {
#   chop;
   $L=$_;
   while ( $L ne "" ) {
       if ( $L =~ m/text[{(] *\'([^)}]*)\'.*[)}](.*)/ ) {
#          ($tid,$fw,$filter,$aksjon,$IF,$prot,$fra,$fraport,$til,$tilport, $R) = ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11 );
#	  print "$tid\t$fw\t$filter\t$aksjon\t$IF\t$prot\t$fra:$fraport\t$til:$tilport\n";
          if ( $text{$1} ) {
	       $T{$1}= $text{$1};
	     }else {
	       $T{$1}="UNDEFINED ".$1;
	     }
	     
##          print "$1=$text{$1}\n";
          $L = $2;
       }else {
              $L= "";
       }
#       print "LINE = $L \n";

   }    
#print "\n";
   
}

@KL = sort keys %T;

foreach $k ( @KL ) {
   
          print "$k=$T{$k}\n";
#	  undef $text{$k};
}

print "\n\n#
#     Ubrukte definisjoner
#-------------------------------------------------------------\n\n";

@KL = sort keys %text;

foreach $k ( @KL ) {
 if ( ! $T{$k} ) { 
          print "$k=$text{$k}\n";
 }
}
