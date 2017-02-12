#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: save_service.cgi,v 1.4 2001/02/21 14:32:50 oyvind Exp $
#



require './fw-lib.pl';
require './obj-lib.pl';

if (! $access{'eservice'}) { &error($text{'acl_eservice'} . ": ".$text{'no'} ) }

if (!$in{'names'}) { &error($text{'sservice_err_invname'}) }



#print "<pre>\n";

$objects = &get_objects( "servicefile" );

$objname =  $in{'object'};
$newname =  $in{'names'};

#print "Objectname: ". $objname ."\n";
#print "Newname: ". $newname ."\n";
if ( $newname ne $objname ) {
if (! $access{'cservice'}) { &error($text{'acl_cservice'} . ": ".$text{'no'} ) }
#	print "Name changed, check if object exist. \n";
	if ( ($ob = $objects->{$newname}) ) {
		&error("Object " . $newname . " exists!\n");
	
	}

}	

#$oldname = $ob->name;

local $o = service->new();
$o->name($newname);
$o->type("service");
$o->port($in{'ports'});
$o->sport($in{'sports'});
$o->proto($in{'proto'});
$o->icmptype($in{'icmptype'});
$o->tos($in{'tos'});



#print "sports = $in{'sports'} = " . $o->sport ." \n";

#$o->display;

$objects->{$newname} = $o;

&save_service_objects(%$objects);
#print "</pre>\n";

redirect("list_services.cgi");

### END of save_host.cgi ###.
