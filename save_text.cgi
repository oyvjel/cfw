#!/usr/bin/perl

# 
# Cumulus Firewall 
# Copyright (C) 2003  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: save_text.cgi,v 1.2 2004/09/08 13:16:31 oyvind Exp $
#


require './fw-lib.pl';
require './obj-lib.pl';

# &ReadParseMime();
# $conf = &get_config();
# if ($in{'view'} ne '') {
#	$conf = $conf->[$in{'view'}]->{'members'};
#	}
# $zconf = $conf->[$in{'index'}]->{'members'};
# $file = &absolute_path(&find("file", $zconf)->{'value'});
# %access = &get_module_acl();
# &can_edit_zone(\%access, $conf->[$in{'index'}]) ||
#	&error($text{'master_ecannot'});
# $access{'file'} || &error($text{'text_ecannot'});
# $access{'ro'} && &error($text{'master_ero'});

$file = "/etc/webmin/cfw/extra.rules";
# if (!$in{'text'}) { &error("text mangler") }

# &lock_file($file);
$in{'text'} =~ s/\r//g;
$in{'text'} .= "\n" if ($in{'text'} !~ /\n$/);
open(FILE, ">$file");
print FILE $in{'text'};

# print  FILE "saved";

close(FILE);

# &unlock_file($config{'chroot'}.$file);
# &webmin_log("text", undef, $conf->[$in{'index'}]->{'value'},
#	    { 'file' => $file });
# &redirect("edit_master.cgi?index=$in{'index'}&view=$in{'view'}");
# &redirect("list_rules.cgi");
&redirect("edit_text.cgi");

