#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: save_rule.cgi,v 1.4 2005/03/22 11:25:27 oyvind Exp $

require "./fw-lib.pl";


if ($in{'rule'}) {
 if (! $access{'erules'}) { &error($text{'srule_err_acl2'}) }
} else {
 if (! $access{'crules'}) { &error($text{'srule_err_acl'}) }
}



# if ($in{'chain'} eq "") { &error($text{'srule_err_nochain'}) }
# if ((&indexof($in{'sport'}, &get_services_list()) >= 0) && $in{'proto'} !~ /^(tcp|udp)$/i) {
# &error($text{'srule_err_servport'});
# }
# if ((&indexof($in{'dport'}, &get_services_list()) >= 0) && $in{'proto'} !~ /^(tcp|udp)$/i) {
# &error($text{'srule_err_servport'});
# }
##########
#if ($in{'target'} eq "port") {
# $target="REDIRECT $in{'redport'}";
#} else {
# $target=$in{'target'};
#}

##################


#if ($in{'rule'} ne "") {
#  $lines=&read_script;
#  if (!$lines[$in{'rule'}]) { &error("No such rule found") }
#  $l=&parse_line($lines[$in{'rule'}]);
#}


$lines=&read_file_lines($config{'rulefile'});
#if (!$$lines[$in{'rule'}]) { &error("No such rule found") }

if ($in{'delete'}) {
      splice (@$lines,$in{'rule'},1);
 }else {
 
$newline=
#    $in{'nr'}
    "$in{'source'}"
    .",$in{'dest'}"
    .",$in{'proto'}"
    .",$in{'frag'}"
    .",$in{'log'}"
    .",$in{'tos'}"
    .",$in{'action'}"
    .",$in{'disable'}"    
    .",$in{'comment'}";
   

if ($in{'newrule'} eq "" || $in{'newrule'} > @{$lines}   ) {    # eller blank eller > antall regler
   push(@{$lines}, $newline);
} else {

   if ($in{'rule'} eq $in{'newrule'}) {
      $lines->[$in{'rule'}]=$newline;
   } else {
   # we are creating a new rule

      $line=$in{'newrule'};
      
      $temp=$newline;
      for (my $i = int($line); $i<@{$lines}; $i++) {
          $temp2 = $lines->[$i];
	  $lines->[$i] = $temp;
	  $temp=$temp2;
      }
      push(@{$lines}, $temp);

   }
}
}

&flush_file_lines();


redirect("list_rules.cgi");

### END of save_rule.cgi ###.
