#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: save_tunnel.cgi,v 1.5 2001/02/21 14:32:50 oyvind Exp $
#



require './fw-lib.pl';
require './obj-lib.pl';

if (! $access{'evpn'}) { &error($text{'acl_evpn'} . ": ".$text{'no'} ) }

if (!$in{'newtunnel'}) { &error($text{'sservice_err_invname'}) }



#print "<pre>\n";

$objects = &get_vpn_objects( "vpnfile" );

if ($in{'delete'}) {
    if (! $access{'dvpn'}) { &error($text{'acl_dvpn'} . ": ".$text{'no'} ) }
    $ob = $objects->{$in{'object'}};
    if (!$ob ) {  &error($text{'delhost_err_nohost'}) }
    delete $objects->{$in{'object'}};
    
}else{
    #$oldname = $ob->name;
    
    $objname =  $in{'object'};
    $newname =  $in{'newtunnel'};
    
    #print "Objectname: ". $objname ."\n";
    #print "Newname: ". $newname ."\n";
    local $o;
    if ( $newname ne $objname ) {
       if (! $access{'cvpn'}) { &error($text{'acl_cvpn'} . ": ".$text{'no'} ) }
    #	print "Name changed, check if object exist. \n";
       if ( ($o = $objects->{$newname}) ) {
           &error("Object " . $newname . " exists!\n");
	   
       }
       $o = tunnel->new();	
     }else{
       
            if ( !($o = $objects->{$newname}) ) {
		&error("Object " . $newname . " == " .$objname ."\n");
		$o = tunnel->new();	
	    }
	    
     }    
     $o->name($newname);
     
     $o->auto($in{'auto'});
     $o->authby($in{'authby'});
	  
     $o->left($in{'localIP'});
     $o->leftid($in{'localID'});
     $o->leftsubnet($in{'source'});
     $o->leftrsasigkey($in{'localkey'});
     $o->leftnexthop($in{'localNHop'});
     $o->leftupdown($in{'vpn_fw'});
     
     $o->right($in{'remoteIP'});
     $o->rightid($in{'remoteID'});
     $o->rightsubnet($in{'dest'});
     $o->rightnexthop($in{'remoteNHop'});
     $o->rightrsasigkey($in{'remotekey'});
     
     
     #$o->display;
     
     $objects->{$newname} = $o;
}     

&save_vpn_objects(%$objects);
#print "<pre>\n",$o->txtout,"\n</pre>\n";
#	&error("Object <pre>\n" . $o->txtout . "</pre>\n");


redirect("list_tunnels.cgi");

### END of save_host.cgi ###.
