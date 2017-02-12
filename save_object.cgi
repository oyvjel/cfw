#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: save_object.cgi,v 1.5 2003/02/05 02:16:19 oyvind Exp $
#



require './fw-lib.pl';
require './obj-lib.pl';


if (! $access{'eobject'}) { &error($text{'acl_eobject'} . ": ".$text{'no'} ) }

if (!$in{'name'}) { &error($text{'shost_err_invname'}) }


$objects = &get_objects;

$objname =  $in{'object'};
$newname =  $in{'name'};

if ( $newname ne $objname ) {
 if (! $access{'cobject'}) { &error($text{'acl_cobject'} . ": ".$text{'no'} ) }
#	print "Name changed, check if object exist. \n";
	if ( ($ob = $objects->{$newname}) ) {
		&error("Object " . $newname . " exists!\n");
	
	}

}	

#$oldname = $ob->name;

local $o = group->new();
$o->name($newname);

$o->comment($in{'comment'});

@member = split(/ /,$in{'members'});
foreach $m (@member) {
	$o->member($m);
}
#$o->type("host");
#$o->ip($in{'ip'});

# $o->display;

$objects->{$newname} = $o;

&save_objects(%$objects);
#print "</pre>\n";

redirect("list_objects.cgi");

### END of save_host.cgi ###.
