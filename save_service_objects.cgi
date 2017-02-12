#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: save_service_objects.cgi,v 1.4 2001/02/21 14:32:50 oyvind Exp $
#



require './fw-lib.pl';
require './obj-lib.pl';

if (! $access{'eservice'}) { &error($text{'acl_eservice'} . ": ".$text{'no'} ) }

if (!$in{'name'}) { &error($text{'shost_err_invname'}) }

$objects = &get_objects( "servicefile" );		

$objname =  $in{'object'};
$newname =  $in{'name'};

if ( $newname ne $objname ) {
if (! $access{'cservice'}) { &error($text{'acl_cservice'} . ": ".$text{'no'} ) }
#	print "Name changed, check if object exist. \n";
	if ( ($ob = $objects->{$newname}) ) {
		&error("Object " . $newname . " exists!\n");
	
	}

}	

#$oldname = $ob->name;

local $o = group->new();
$o->name($newname);

@member = split(/ /,$in{'members'});
foreach $m (@member) {
	$o->member($m);
}
#$o->type("host");
#$o->ip($in{'ip'});

#$o->display;

$objects->{$newname} = $o;

&save_service_objects(%$objects);
#print "</pre>\n";

redirect("list_services.cgi");

### END of save_host.cgi ###.
