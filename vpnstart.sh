#!/bin/sh
# 
# Cumulus Firewall 
# Copyright (C) 2000  Øyvind Jelstad, Cumulus IT AS
# 
# $Id: vpnstart.sh,v 1.4 2003/01/20 12:37:55 oyvind Exp $

# Enable IP spoofing protection
    # turn on Source Address Verification
    for f in /proc/sys/net/ipv4/conf/*/rp_filter; do
        echo 0 > $f
    done

/usr/sbin/ipsec setup restart

