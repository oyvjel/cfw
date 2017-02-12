#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: manual.pl,v 1.3 2003/01/20 12:37:55 oyvind Exp $
#

$ENV{'WEBMIN_CONFIG'} = "/etc/webmin";

$ENV{'WEBMIN_VAR'} = "/var/webmin";
$ENV{'SCRIPT_NAME'} = "/cfw/manual.cgi";
$main::no_acl_check++;


require "./fw-lib.pl";
require './obj-lib.pl';


print "<pre>
  $config_directory - config_directory
  $var_directory - var_directory

  %config
  %gconfig - Global configuration
  $tb - Background for table headers
  $cb - Background for table bodies
  $scriptname - Base name of the current perl script
  $module_name - The name of the current module
  $module_config_directory - The config directory for this module
  $webmin_logfile - The detailed logfile for webmin
  </pre>";


require "./lv-lib.pl";
   if (!-f $config{'scriptfile'}) {
    open( SF,">". $config{'scriptfile'});
    print SF "#Touched by manual.pl";
    close SF;
   }

 &generate_fw_script;

   if (!-x $config{'scriptfile'}) {
    chmod 0755, $config{'scriptfile'};
    $msg="$text{'sman_msg_exec'}<BR>";
   }

   &safe_exec("Restart FW",$config{'scriptfile'});
      
 print $msg;

