#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: script_manager.cgi,v 1.9 2003/06/06 09:38:01 oyvind Exp $
#


require "./fw-lib.pl";
require "./obj-lib.pl";
require "./lv-lib.pl";

if ($in{'action'}) { &doit } else { &printscreen }


sub printscreen {


&header($text{'sman_title'}, undef, "intro", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});
&toolbar;



print "<BR><HR>\n";

if ($msg) {
print <<EOM;
<H3>$msg</H3>
<HR>
EOM
} 

print <<EOM;
<TABLE CELLSPACING=0 CELLPADDING=2 BORDER=2>
 <TR>
  <TD $tb COLSPAN=2><B>$text{'sman_header'}</A></TD>
 </TR>
 <TR>
  <TD $cb COLSPAN=2>$text{'sman_confpath'} $config{'scriptfile'}<BR><BR><B>
EOM

 if (-e $config{'scriptfile'}) {
  print $text{'sman_exist'};
 } else {
  print $text{'sman_notexist'};
 }

print <<EOM;
  </B><BR>&nbsp;
  </TD>
 </TR>
 <TR>
  <TD $cb><A HREF="$ENV{'SCRIPT_NAME'}?action=create">$text{'sman_create'}</A></TD>
  <TD $cb>$text{'sman_createdesc'}</TD>
 </TR>
 <TR>
  <TD $cb><A HREF="$ENV{'SCRIPT_NAME'}?action=view">$text{'sman_view'}</A></TD>
  <TD $cb>$text{'sman_viewdesc'}</TD>
 </TR>
 <TR>
 <TR>
  <TD $cb><A HREF="$ENV{'SCRIPT_NAME'}?action=execute">$text{'sman_execute'}</A></TD>
  <TD $cb>$text{'sman_executedesc'}</TD>
 </TR>
 <TR>
  <TD $cb><A HREF="$ENV{'SCRIPT_NAME'}?action=stopfw">$text{'sman_stopfw'}</A></TD>
  <TD $cb>$text{'sman_stopdesc'}</TD>
 </TR>
  <TD $cb><A HREF="$ENV{'SCRIPT_NAME'}?action=bootup">$text{'sman_bootup'}</A></TD>
EOM
print "  <TD $cb>".&text('sman_bootupdesc', $config{'bootloc'})."</TD>";

print <<EOM;
 </TR>
 <TR>
  <TD $cb><A HREF="$ENV{'SCRIPT_NAME'}?action=rembootup">$text{'sman_rembootup'}</A></TD>
  <TD $cb>$text{'sman_rembootupdesc'}</TD>
 </TR>
 <TR>
  <TD $cb><A HREF="$ENV{'SCRIPT_NAME'}?action=delete">$text{'sman_delete'}</A></TD>
  <TD $cb>$text{'sman_deletedesc'}</TD>
 </TR>
 <TR>
  <TD $cb><A HREF="edit_text.cgi">$text{'sman_extra_rules'}</A></TD>
  <TD $cb>$text{'sman_extra_rules_desc'}</TD>
 </TR>
</TABLE>

EOM

print "<BR><HR>\n";

&footer("./", "module index");

}


sub doit {
 if (!$in{'action'}) {
  &error($text{'sman_err_what'});
 } elsif ($in{'action'} eq "create") {
  if ((-e $config{'scriptfile'}) && !$in{'confirmed'}) {
   if (! $access{'rewrite'}) { &error($text{'sman_err_acl_rewrite'}) }


&header($text{'sman_title'}, undef, "intro", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});


   print "<BR><HR>\n";
   print "<H3>$text{'sman_err_exists'}</H3>\n";
   print "<FORM ACTION=\"$ENV{'SCRIPT_NAME'}\" METHOD=POST>\n";
   print "<INPUT TYPE=hidden NAME=\"confirmed\" VALUE=1>\n";
   print "<INPUT TYPE=hidden NAME=\"action\" VALUE=\"create\">\n";
   print "<INPUT TYPE=submit VALUE=\"$text{'sman_rewrite'}\">\n";
   print "</FORM><HR>\n";
   &footer("script_manager.cgi", $text{'sman_smanret'});
   exit;
  }

  &header($text{'sgen_title'}, undef, "intro", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

  &generate_fw_script;
  

   $msg=$text{'sman_createsucc'};
   &footer("script_manager.cgi", $text{'sman_smanret'});
   exit;

 } elsif ($in{'action'} eq "view") {

   &header($text{'sman_title'}, undef, "intro", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});
      open(FILE, "$config{'scriptfile'}") || &error($text{'sman_err_read'});	
   
   print "<HR><pre>\n"; 
    while (<FILE>) {
      print;
      
    }
    
   print "</pre><HR>\n";
   
   &footer("script_manager.cgi", $text{'sman_smanret'});
   exit;


} elsif ($in{'action'} eq "execute") {

   if (!-x $config{'scriptfile'}) {
    chmod 0755, $config{'scriptfile'};
    $msg="$text{'sman_msg_exec'}<BR>";
   }

   &foreign_check("proc") || &error($text{'sman_err_procneeded'});
   &foreign_require("proc", "proc-lib.pl");

   $got = &foreign_call("proc", "safe_process_exec", $config{'scriptfile'},
                        0, 0, STDOUT, undef, 1);

   if ($got) {
    $msg .= "$text{'sman_exec_err'} $got";
   } else {
     $msg .= $text{'sman_exec_ok'};
   }
 } elsif ($in{'action'} eq "stopfw") {
 
   &header($text{'sman_title'}, undef, "intro", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});
   &safe_exec("STOP FW",$config{'scriptfile'}." stop 1");
   &footer("script_manager.cgi", $text{'sman_smanret'});
   exit;


 } elsif ($in{'action'} eq "bootup") {
   if (! $access{'bootup'}) { &error($text{'sman_err_acl_bootup'}) }
   if (! $config{'bootloc'}) { &error(&text('lib_err_boot', $text{'config_link'})) }
   if (!-e $config{'scriptfile'}) { &error(&text('sman_err_nofile', $config{'scriptfile'})) }
  ($dirpath,$basename) = ($config{'scriptfile'} =~ m#^(.*/)?(.*)#);
  ($config{'scriptfile'} =~ /^$config{'bootloc'}\/$basename$/) || &error(&text('sman_err_bootloc', $config{'bootloc'}));
  &foreign_check('init') || &error($text{'sman_err_init'});
  &foreign_require('init', 'init-lib.pl');

  if (! &foreign_call('init', 'action_levels', 'S', $basename)) {
   if (!-x $config{'scriptfile'}) {
    chmod 0755, $config{'scriptfile'};
    $msg="$text{'sman_msg_exec'}<BR>";
   }

   foreach $i (2,3,4,5) {
    &foreign_call('init', 'add_rl_action', $basename, $i, 'S', 50);
    &foreign_call('init', 'add_rl_action', $basename, $i, 'K', 50);
#VPN
    if (-e "$config{'bootloc'}/cfw_vpn" ) {
       &foreign_call('init', 'add_rl_action', "cfw_vpn", $i, 'S', 51);
       &foreign_call('init', 'add_rl_action', "cfw_vpn", $i, 'K', 51);
    }
   }
  } else {
   &error($text{'sman_err_init1'});
  }

  $msg .= $text{'sman_bootupsucc'};

 } elsif ($in{'action'} eq "rembootup") {
   if (!-e $config{'scriptfile'}) { &error(&text('sman_err_nofile', $config{'scriptfile'})) }
  ($dirpath,$basename) = ($config{'scriptfile'} =~ m#^(.*/)?(.*)#);
  ($config{'scriptfile'} =~ /^$config{'bootloc'}\/$basename$/) || &error(&text('sman_err_bootloc', $config{'bootloc'}));
  &foreign_check('init') || &error($text{'sman_err_init'});
  &foreign_require('init', 'init-lib.pl');

  if (&foreign_call('init', 'action_levels', 'S', $basename)) {
   foreach $i (2,3,4,5) {
    &foreign_call('init', 'delete_rl_action', $basename, $i, 'S');
    &foreign_call('init', 'delete_rl_action', $basename, $i, 'K');
    
    &foreign_call('init', 'delete_rl_action', "cfw_vpn", $i, 'S');
    &foreign_call('init', 'delete_rl_action', "cfw_vpn", $i, 'K');
    
   }
  } else {
   &error($text{'sman_err_init2'});
  }



  $msg = $text{'sman_rembootupsucc'};

 } elsif ($in{'action'} eq "delete") {
  if (! $access{'delete'}) { &error($text{'sman_err_acl_delete'}) }

  $vpnscript = $config{'bootloc'}."/cfw_vpn";
#  if (!-e $config{'scriptfile'}) { &error(&text('sman_err_nofile', $config{'scriptfile'})) }
  ($dirpath,$basename) = ($config{'scriptfile'} =~ m#^(.*/)?(.*)#);
  ($config{'scriptfile'} =~ /^$config{'bootloc'}\/$basename$/) || &error(&text('sman_err_bootloc', $config{'bootloc'}));
  &foreign_check('init') || &error($text{'sman_err_init'});
  &foreign_require('init', 'init-lib.pl');

  if (&foreign_call('init', 'action_levels', 'S', $basename)) {
   foreach $i (2,3,4,5) {
    &foreign_call('init', 'delete_rl_action', $basename, $i, 'S');
    &foreign_call('init', 'delete_rl_action', $basename, $i, 'K');
   }
   $msg .="$text{'sman_msg_rem'}<BR>";
  }


  if ( -e $config{'scriptfile'}) {
    `rm -f $config{'scriptfile'}`;
    $msg .= "File ".$config{'scriptfile'} ." deleted<br>\n";
  }

  if (&foreign_call('init', 'action_levels', 'S', "cfw_vpn")) {
   foreach $i (2,3,4,5) {
    &foreign_call('init', 'delete_rl_action', "cfw_vpn", $i, 'S');
    &foreign_call('init', 'delete_rl_action', "cfw_vpn", $i, 'K');
   }
   $msg .="VPN: $text{'sman_msg_rem'}<BR>";
  }


  if ( -e $vpnscript) {
    `rm -f $vpnscript`;
    $msg .= "File ".$vpnscript ." deleted<br>\n";
  }
  $msg .= $text{'sman_deletesucc'};

 } else {
  &error($text{'sman_err_unkcom'});
 }

 &printscreen;
}

### END of script_manager.cgi ###.
