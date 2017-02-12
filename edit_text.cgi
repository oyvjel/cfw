#!/usr/bin/perl
# edit_text.cgi
# Display a form for manually editing a records file

# 
# Cumulus Firewall 
# Copyright (C) 2003  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: edit_text.cgi,v 1.2 2004/09/08 13:16:31 oyvind Exp $
#


require './fw-lib.pl';
require './obj-lib.pl';


&header($text{'extra_rules_title'}, undef, "extra_rules", 1, 1, undef,
        $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;
print "<center>";
# print <<EOM;
# <H3>$text{'lservices_usrdef'}</H3>


# require './bind8-lib.pl';
# &ReadParse();
# $conf = &get_config();
# if ($in{'view'} ne '') {
#	$conf = $conf->[$in{'view'}]->{'members'};
#	}
# $zconf = $conf->[$in{'index'}]->{'members'};
# $file = &absolute_path(&find("file", $zconf)->{'value'});

$file = "/etc/webmin/cfw/extra.rules";
%access = &get_module_acl();

# &can_edit_zone(\%access, $conf->[$in{'index'}]) ||
#	&error($text{'master_ecannot'});
# $access{'file'} || &error($text{'text_ecannot'});
# &header($text{'text_title'}, "");
# print "test";
# print "<center><font size=+1>$file</font></center>\n";

# print "<hr> test\n";

# print " Åpner fil";
# open(FILE, $config{'chroot'}.$file);
open(FILE, $file);
while(<FILE>) {
	push(@lines, &html_escape($_));
	}
close(FILE);
# print " file opened";
if (!$access{'ro'}) {
	print &text('extra_rules_descr', "<tt>$in{'file'}</tt>"),"<p>\n";
	}

$text = join("", @lines);
if (!$text) {
      print"Default" ;
      $text = "#!/bin/sh

# Transparent proxy , se http://en.tldp.org/HOWTO/mini/TransparentProxy-4.html
# iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128 
# iptables -t nat -A PREROUTING  -p tcp --dport 80 -j REDIRECT --to-port 3128 

# Squid config for transparent proxy:
# httpd_accel_host virtual 
# httpd_accel_port 80 
# httpd_accel_with_proxy on 
# httpd_accel_uses_host_header on 

";
     
}


# print "<form action=save_text.cgi method=post enctype=multipart/form-data>\n";
print "<form action=save_text.cgi method=post>\n";
print "<input type=hidden name=index value=\"$in{'index'}\">\n";
print "<input type=hidden name=view value=\"$in{'view'}\">\n";
print "<textarea name=text rows=20 cols=80 wrap=\"off\">\n",
	$text,"</textarea><p>\n";
print "<input type=submit value=\"$text{'save'}\"> ",
      "<input type=reset value=\"$text{'text_undo'}\">\n"
	if (!$access{'ro'});
print "</form>\n";

print "<hr>\n";
&footer("./", $text{'return_to_top'});

