#!/usr/bin/perl
#
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: delete_service.cgi,v 1.4 2001/02/21 14:32:50 oyvind Exp $


require './fw-lib.pl';
require './obj-lib.pl';

if (! $access{'dservice'}) { &error($text{'acl_dservice'} . ": ".$text{'no'} ) }
#if (! $access{'dservices'}) { &error($text{'delserv_err_acl'}) }
$objects = &get_objects( "servicefile" );
$ob = $objects->{$in{'object'}};

if (!$ob ) {  &error($text{'delhost_err_nohost'}) }


#Sjekk om objektet er brukt i andre objektgrupper eller regler.

delete $objects->{$in{'object'}};

&save_service_objects(%$objects);


redirect("list_services.cgi");

