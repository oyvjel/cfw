# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: obj-lib.pl,v 1.5 2003/02/05 02:16:19 oyvind Exp $


package main;



sub get_objects {

my $file = shift;

if ( !$config{$file}   ) { $file =  "objectfile"; } 

local %objects;

#print " i objread \n";
   open(FIL, $config{$file})  or die "Kan ikke &aring;pne $file $config{$file} \n";    
    
     while (<FIL>) {
    	if ( ($n,$v) = /(SET)=(\S+)/ ) {
#       		print "navn = " .$n ."\n";
#       		print "verdi = " .$v ."\n";
                $set = $v;
       		next;
    	}

    	if ( ($t) = / *(\S+)\s*\( *$/ ) {
#       print "Type = " .$t ."\n";
       		$o = $t->new();
                $o->type($t);
		if ( $t eq "group" ) {$o->listname($set); } 		
       		next;
    	}

    	if ( ($t) = / *(\)) *$/ ) {
#       		print "Type = " .$t ."\n";
		$objects{$o->name} = $o;
       		$t = undef;
       		next;
    	}

    	if ( ($n,$v) = /(\S+?)=(.*?\S)\s*$/ ) {
#       		print "navn = " .$n ."\n";
#       		print "verdi = " .$v ."\n";
                $o->$n($v);
#print $o{$n},"\n";
	        next;
    	}
#    	print FIL $lines;
	
    }	
    return \%objects;
}


sub get_vpn_objects {

my $file = shift;

if ( !$config{$file}   ) { $file =  "vpnfile"; } 

local %objects;

#print "<pre> i objread \n";
   open(FIL, $config{$file})  or die "Kan ikke &aring;pne $file $config{$file} \n";    
    
     while (<FIL>) {
     
    	if ( ($t) = /([ \t]*)#.*/ ) {
#	  print " Kommentar\n";
	  next;
	  }
	  
#    	if ( ($t) = / *(\S+)\( *$/ ) {
    	if ( ($t) = /conn *(\S+)/ ) {
#	      print "Connection = " .$t ."\n";
              if ( $o ) {
                    $objects{$o->name} = $o;
	      }
#	      $o = $t->new();
	      $o = tunnel->new();
	      $o->name($t);
	      #		if ( $t eq "group" ) {$o->listname($set); } 		
	      next;
    	}

    	if ( ($t) = / *(\)) *$/ ) {
#       		print "Type = " .$t ."\n";
		$objects{$o->name} = $o;
       		$t = undef;
       		next;
    	}

    	if ( ($n,$v) = /[ \t]+(\S+?)=(\S+)/ ) {
#       		print "navn = " .$n ."<br>\n";
#       		print "verdi = " .$v ."<br>\n";
                $o->$n($v);
# print $o{$n},"\n";
	        next;
    	}
#    	print FIL $lines;
	
    }
    if ( $o ) {
#      print $o->txtout;
      $objects{$o->name} = $o;
    }
    
#print "</pre> \n";
    return \%objects;
}



sub save_objects {

	my %Objects = @_;

$file =  "objectfile"; 

## print " i objwrite \n";
    open(FIL, ">" . $config{$file} ) or die "Kan ikke &aring;pne $file $config{$file} \n";    
    
    print FIL "# Objektdefinisjoner \n";

    @sok = sort  keys %Objects;
#	        while (($k,$v) = each %$objects) {
    foreach $o (@sok) {
		   $v = $objects->{$o};
#       while (($k,$v) = each %Objects) {
#         print "Key: ", $k, "\n";
#         $v->display;
	 $lines .= $v->txtout;
     }


	print FIL $lines;
#	print  $lines;
	
    }	



sub save_service_objects {

     my %Objects = @_;

    $file =  "servicefile";

## print " i objwrite \n";
    open(FIL, ">" . $config{$file} ) or die "Kan ikke &aring;pne $file $config{$file} \n";    
    
    print FIL "# Objektdefinisjoner \n";

    @sok = sort  keys %Objects;
    foreach $o (@sok) {
         $v = $objects->{$o};
	 $lines .= $v->txtout;
     }


	print FIL $lines;
#	print  $lines;
	
}	


sub save_vpn_objects {

     my %Objects = @_;

    $file =  "vpnfile";

## print " i objwrite \n";
    open(FIL, ">" . $config{$file} ) or die "Kan ikke &aring;pne $file $config{$file} \n";    
    
    print FIL "# Tunnel definisjoner \n";

    @sok = sort  keys %Objects;
    foreach $o (@sok) {
         $v = $objects->{$o};
	 $lines .= $v->txtout;
     }


	print FIL $lines;
#	print  $lines;
	
}	




package Object;

#           use strict;

           ##################################################
           ## the object constructor (simplistic version)  ##
           ##################################################
           sub new {
               my $proto = shift;
	       my $class = ref($proto) || $proto;			      
	       my $self  = {};
	       
#               $self->{NAMES}   = [];
#               $self->{AGE}    = undef;
#               $self->{PEERS}  = [];
               bless($self,$class);
               return $self;
           }

           ##############################################
           ## methods to access per-object data        ##
           ##                                          ##
           ## With args, they set the value.  Without  ##
           ## any, they only retrieve it/them.         ##
           ##############################################

        
	 
sub AUTOLOAD {
	my $self = shift;
	my $typ = ref($self)
		or die "$self is not an object";
	my $name = $AUTOLOAD;
	$name =~ s/.*://;   # strip fully-qualified portion

#	unless (exists $self->{_permitted}->{$name} ) {
#		croak "Can't access $name' field in class $type";
#	}

	if (@_) {
#		 push @{ $self->{_VARS} }, $name;
		 $self->{_VARS}->{$name}++;		 
		return $self->{$name} = shift;
		
	} else {
		return $self->{$name};
	}

}

sub txtout {
               my $self = shift;

              $rv = $self->type . "(\n";
#              for $n ( @{$self->{_VARS}}) {
              for $n ( keys %{$self->{_VARS}}) {
	          $rv .= "\t" . $n ."=" . $self->{$n} ."\n";
	      }
	      $rv .= ")\n";
	      return $rv;
           }


package group;
@ISA = ("Object");

           sub new {
               my $proto = shift;
	       my $class = ref($proto) || $proto;			      
	       my $self  = {};
	       
               $self->{LIST}  = "Rec";
               bless($self,$class);
               return $self;
           }


#my %Rec = undef;

#my $listname="Rec";
           sub listname {
               my $self = shift;
               if (@_) { $self->{LIST} = shift }
               return $self->{LIST};
           }
           sub name {
               my $self = shift;
               if (@_) { $self->{NAME} = shift }
               return $self->{NAME};
           }


           sub members {
               my $self = shift;
               if (@_) { @{ $self->{MEMBERS} } = @_ }
               return @{ $self->{MEMBERS} };
           }
           sub member {
               my $self = shift;
               if (@_) { push @{ $self->{MEMBERS} }, @_ }
               return @{ $self->{MEMBERS} };
           }
	   
           sub hash {
               my $self = shift;
               if (@_) { @{ $self->{HASH} } = @_ }
               return @{ $self->{HASH} };
           }



sub txtout {
               my $self = shift;

               $rv = "group(\n";

	       $rv .= "\tname=". $self->name ."\n";
	       $rv .= "\tcomment=". $self->comment ."\n";
	       
	       foreach my $elem ($self->members) {
	          $rv .=  "\tmember=". $elem ."\n";
	       }
               $rv .= ")\n";

               return $rv;
           }


sub display {
               my $self = shift;
	       my $list = $self->listname;	       
	       printf "\nGruppen %s har følgende medlemmer i %s: \n", $self->name, $list;
               printf "________________________________________\n";

	print "LISTENAVN = ", $list, "\n";
	foreach my $elem ($self->members) {
		my $object;
#
#	       $h = $hash;
#	       print $h;
	       if ($object = $main::{$list}{$elem}) { 
	       		$object->display;
	       } else {
	       		print "Object " . $elem . " not found in " .$list. "\n";
		}
#	       $Rec{$elem}->display;	       
	       
#$elem->display;

	   }
               printf "________________________________________\n";


	       }

#########################  host ############################# 
package host;
@ISA = ("Object");

sub display {
               my $self = shift;
	       
	       printf "\nHost %s har IP %s .\n", $self->name, $self->ip;
           printf "Den er tilkoblet %s interfacet.\n", $self->location;

	       }

#########################  net ############################# 
package net;
@ISA = ("Object");

sub display {
               my $self = shift;
	       
	       printf "\nNettverk %s har IP %s .\n", $self->name, $self->ip;
	       printf "\nSubnettmaske er %s .\n", $self->netmask;
	       
	       printf "Nettet nåes via  %s interfacet.\n", $self->location;

	       }

package interface;
@ISA = ("Object");

sub display {
               my $self = shift;
	       
	       printf "\nInterface %s har IP %s .\n", $self->name, $self->ip;
	       printf "Nettverk: %s .\n", $self->location;

	       }



#########################  service ############################# 
package service;
@ISA = ("Object");

sub display {
               my $self = shift;
	       
	       printf "\nService %s har sport %s .\n", $self->name, $self->sport;

	       }



#########################  tunnel  ############################# 
package tunnel;
@ISA = ("Object");

sub display {
               my $self = shift;
	       
	       printf "\nTunnel name %s.\n", $self->name;

	       }

sub txtout {
               my $self = shift;

              $rv = "conn " . $self->name . "\n";
#              for $n ( @{$self->{_VARS}}) {
              for $n ( keys %{$self->{_VARS}}) {
	          next if $n eq "name";
		  next if $self->{$n} eq "";
	          $rv .= "\t" . $n ."=" . $self->{$n} ."\n";
	      }
	      $rv .= "#\n";
	      return $rv;
           }


##########################################

1;
