#!/usr/bin/perl
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: index.cgi,v 1.8 2003/08/18 06:18:46 oyvind Exp $
#

$cfwversion="v. 3.0.2";

require "./fw-lib.pl";

#@ps=&parse_script();
#$chains=&find_arg_struct('-N', \@ps);

&header($text{'index_title'}, undef, "intro", 1, 1, undef,
        $cfwversion . " <br>\n" . $text{'author'} ." <BR>" . $text{'homepage'});

&toolbar;

print <<EOM;
<p><hr><p>
<center><table border=0><tr><td>

$text{'welcome'}

</td></tr></table>
</center>
<p>
<hr>
EOM

&footer("/", $text{'index_return'});



### END of index.cgi ###.
