#!/usr/bin/env perl
use strict;
use warnings;

use Net::Netmask;

# our owners and their ranges
my @blocks = (
	    [ 'A', '000.0.0.0/1' ],
	    [ 'B', '128.0.0.0/2' ],
	    [ 'C', '192.0.0.0/4' ],
	    [ 'D', '224.0.0.0/4' ],
	    [ 'E', '240.0.0.0/4' ],
	    [ 'L', '127.0.0.0/255.0.0.0' ],
    	    [ 'PA', '10.0.0.0/255.0.0.0' ],
    	    [ 'PB', '172.16.0.0/255.240.0.0' ],
    	    [ 'PC', '192.168.0.0/255.255.0.0' ],

    );

# populate the table with tagged blocks
for my $block (@blocks) {
        my ($owner, $range) = @$block;
        my $nb = Net::Netmask->new2($range);
        $nb->tag('owner', $owner);
        $nb->storeNetblock();
    };

# do the lookup.
while (my $ip = <DATA>) {
        chomp $ip;
        my $block = findNetblock($ip);
    if (  $block ) {
        print "$ip belongs to ", $block->tag('owner'), "\n";
    }else{ 
        print "$ip belongs to UNDEF, \n";
       }
    }

__DATA__
  1.0.0.1
  126.255.255.255
  127.0.0.1
  128.0.0.1
  191.255.255.255
  192.0.0.1
  224.0.0.1
  239.255.255.255
  240.0.0.1
  254.255.255.255
  192.168.3.33
  192.168.4.12
  $ADR_eth0
  10.1.0.0
  10.255.255.255
  172.18.0.0
  192.168.220.1