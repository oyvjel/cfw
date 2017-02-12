#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: save_host.cgi,v 1.6 2003/02/05 02:16:19 oyvind Exp $
#



require './fw-lib.pl';
require './obj-lib.pl';


if (! $access{'eobject'}) { &error($text{'acl_eobject'} . ": ".$text{'no'} ) }

if ((!$in{'ip'}) && (!&check_ipaddress($in{'ip'}))) { &error($text{'shost_err_invip'}) }
#if ((!$in{'netmask'}) && ( (!&check_ipaddress($in{'netmask'})) || ($in{'netmask'} !~ /^\d+$/) )) { &error($text{'shost_err_invnetmask'}) }
if ((!$in{'netmask'}) && ( (!&check_ipaddress($in{'netmask'})) || ($in{'netmask'} !~ /^\d+$/) )) { undef $in{'netmask'} }
if (!$in{'names'}) { &error($text{'shost_err_invname'}) }

if ( $in{'netmask'} == 32 )  { undef $in{'netmask'} }

$objects = &get_objects;

$objname =  $in{'object'};
$newname =  $in{'names'};

if ( $newname ne $objname ) {
#	print "Name changed, check if object exist. \n";
 if (! $access{'cobject'}) { &error($text{'acl_cobject'} . ": ".$text{'no'} ) }
 
 if ( ($ob = $objects->{$newname}) ) {
		&error("Object " . $newname . " exists!\n");
	
	}

}	

local $o;

#$oldname = $ob->name;
if ( $in{'is_if'}) {
   $o = interface->new();
   $o->type("interface");
}elsif ( $in{'netmask'} ) {
   $o = net->new();
   $o->type("net");
}else {
   $o = host->new();
   $o->type("host");
}

$o->name($newname);

$o->ip($in{'ip'});
$o->netmask($in{'netmask'});
$o->location($in{'dev'});

$o->comment($in{'comment'});

$objects->{$newname} = $o;

&save_objects(%$objects);
#print "</pre>\n";

redirect("list_objects.cgi");

### END of save_host.cgi ###.
