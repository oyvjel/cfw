#!/bin/sh
# Cumulus IT Firewalling Script File
# Generated by Cumulus Firewall generator
# Copyright (C) 2002 by �yvind Jelstad, Cumulus IT AS
# http://www.cumulus.no/

# $Id: fwstart.sh,v 1.2 2004/10/21 09:29:07 oyvind Exp $

# ----------------------------------------------------------------------------
#  DEFAULT FILTER SOM SKAL ERSTATTES AV REELT REGELSETT. DETTE FILTERET ER
#  ANTAGELIG IKKE I SAMSVAR MED �NSKET SIKKERHETSPOLITIKK.
#  Blokkerer all trafikk inn til maskin.
#  Minimal logging

#  Stop or Start:

case "$1" in
  stop)
  
  echo "Stopping  firewalling in $2 seconds... "

  logger -p user.info -t cfw ADMIN: Stop: Stopping  firewalling in $2 seconds... 


  sleep $2
  
  echo "...now!"

 # Flush all rules
  echo -n "Flushing all rules ... "
    /sbin/iptables -P INPUT ACCEPT
    /sbin/iptables -P FORWARD ACCEPT
    /sbin/iptables -P OUTPUT ACCEPT
    /sbin/iptables -t nat -P PREROUTING ACCEPT
    /sbin/iptables -t nat -P POSTROUTING ACCEPT
    /sbin/iptables -t nat -P OUTPUT ACCEPT
    /sbin/iptables -F
    /sbin/iptables -t nat -F
    /sbin/iptables -X
    /sbin/iptables -t nat -X

    # Disnable IP spoofing protection
    # turn off Source Address Verification
    for f in /proc/sys/net/ipv4/conf/*/rp_filter; do
        echo 0 > $f
    done

    logger -p user.info -t cfw ADMIN: Stop: Firewall is stopped
    echo "done."

    exit 0
;;

esac

echo " Initial FW script. Probably not what you want. Edit the rules! "
echo " This will block all traffic to the box! "
echo " Minimum logging! "



# ----------------------------------------------------------------------------
# echo "Starting firewalling... "


# ----------------------------------------------------------------------------

logger -p user.info -t cfw ADMIN: Start: Starting Cumulus Firewall



#########
# Load all required IPTables modules
#

#
# Needed to initially load modules
#
# /sbin/depmod -a
  
#
# Adds some iptables targets like LOG, REJECT and MASQUARADE.
#
/sbin/modprobe ipt_LOG
  #/sbin/modprobe ipt_REJECT
  /sbin/modprobe ipt_MASQUERADE
  
#
# Support for owner matching
#
#/sbin/modprobe ipt_owner

#
# Support for connection tracking of FTP and IRC.
#
/sbin/modprobe ip_conntrack_ftp
/sbin/modprobe ip_nat_ftp

#/sbin/modprobe ip_conntrack_irc
#/sbin/modprobe ip_nat_irc

#/sbin/modprobe ip_conntrack_h323
#/sbin/modprobe ip_nat_h323


# Reset all tables and policy.
# Default policy is DENY
    /sbin/iptables -P INPUT DROP
    /sbin/iptables -P FORWARD DROP
    /sbin/iptables -P OUTPUT ACCEPT
    /sbin/iptables -t nat -P PREROUTING ACCEPT
    /sbin/iptables -t nat -P POSTROUTING ACCEPT
    /sbin/iptables -t nat -P OUTPUT ACCEPT
    /sbin/iptables -F
    /sbin/iptables -t nat -F
    /sbin/iptables -X
    /sbin/iptables -t nat -X
  



# ----------------------------------------------------------------------------

    # Enable TCP SYN Cookie Protection
    echo 1 > /proc/sys/net/ipv4/tcp_syncookies

    # Enable always defragging Protection
#    echo 1 > /proc/sys/net/ipv4/ip_always_defrag

    # Enable broadcast echo  Protection
    echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts

    # Enable bad error message  Protection
    echo 1 > /proc/sys/net/ipv4/icmp_ignore_bogus_error_responses

    # Enable IP spoofing protection
    # turn on Source Address Verification
    for f in /proc/sys/net/ipv4/conf/*/rp_filter; do
        echo 1 > $f
    done

    # Disable ICMP Redirect Acceptance
    for f in /proc/sys/net/ipv4/conf/*/accept_redirects; do
        echo 0 > $f
    done

    # Disable Source Routed Packets
    for f in /proc/sys/net/ipv4/conf/*/accept_source_route; do
        echo 0 > $f
    done

    # Log Spoofed Packets, Source Routed Packets, Redirect Packets
    for f in /proc/sys/net/ipv4/conf/*/log_martians; do
        echo 0 > $f
    done

# Enable forwarding.
    echo "1" > /proc/sys/net/ipv4/ip_forward

#
# Dynamic IP users:
#
#echo "1" > /proc/sys/net/ipv4/ip_dynaddr

#
# ----------------------------------------------------------------------------
# New chains:
if ! ( /sbin/iptables -F LOGDROP >/dev/null 2>&1 ) ; 
  then 
   /sbin/iptables -N LOGDROP
fi
/sbin/iptables -F LOGDROP
# /sbin/iptables -A LOGDROP -j LOG --log-prefix "LOGDROP " --log-ip-options --log-tcp-options
[ -n $LOG ] || /sbin/iptables -A LOGDROP -j LOG --log-prefix "cfw:LOGDROP:DROP RULE= "

/sbin/iptables -A LOGDROP -j DROP





# ----------------------------------------------------------------------------
# LOOPBACK

    # Unlimited traffic on the loopback interface.

    /sbin/iptables -A INPUT  -i lo  -j ACCEPT 
    /sbin/iptables -A OUTPUT -o lo  -j ACCEPT 


# MASQ timeouts
#
#   2 hrs timeout for TCP session timeouts
#  10 sec timeout for traffic after the TCP/IP "FIN" packet is received
#  60 sec timeout for UDP traffic (MASQ'ed ICQ users must enable a 30sec firewall timeout in ICQ itself)
#
# ipchains -M -S 7200 10 60

#


# Rule nr 1: FRA Any on |ALL| TIL FW-EXT1 on |EXT| PORT any_tcp
# DESTINATION IS FIREWALL!
# S-IF:  , D-IF: eth0 
[ -n $LOG ] || /sbin/iptables -A INPUT -s 0.0.0.0/0.0.0.0 -d 0.0.0.0/0.0.0.0 -p 0 -j LOG --log-prefix "cfw:INPUT:DROP RULE=1 "
/sbin/iptables -A INPUT -s 0.0.0.0/0.0.0.0 -d 0.0.0.0/0.0.0.0 -p 0 -j DROP


#------------------------------------------------------------------------------

# ICMP  
    /sbin/iptables -I INPUT 1 -p icmp  -j ACCEPT 
    /sbin/iptables -I OUTPUT 1  -p icmp -j ACCEPT
#    /sbin/iptables -I FORWARD 1 -p icmp  -j ACCEPT


##### DNS ############
#    /sbin/iptables -I INPUT 1 -p udp -d 0.0.0.0/0 --destination-port domain  -j ACCEPT 
    /sbin/iptables -I OUTPUT 1 -p  udp -d 0.0.0.0/0 --destination-port domain  -j ACCEPT 
#    /sbin/iptables -I FORWARD 1 -p  udp -d 0.0.0.0/0 --destination-port domain  -j ACCEPT


#### REJECT Ident ( auth ) ############
    /sbin/iptables -I INPUT 1  -p tcp -d 0.0.0.0/0 --destination-port auth  -j REJECT
    /sbin/iptables -I FORWARD 1  -p tcp -d 0.0.0.0/0 --destination-port auth  -j REJECT



#### DROP BOOTP ############
    /sbin/iptables -I INPUT 1 -p udp -d 0.0.0.0/0 --destination-port 67  -j DROP
    /sbin/iptables -I INPUT 1 -p udp -d 0.0.0.0/0 --destination-port 68  -j DROP

## Established 

/sbin/iptables -I INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT 
# /sbin/iptables -I FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT 
/sbin/iptables -I OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT 
# /sbin/iptables -A FORWARD -m limit --limit 3/minute --limit-burst 3 -j LOG 
#          --log-level INFO --log-prefix "IPT FORWARD packet died: "


if [ -x /etc/webmin/cfw/extra.rules ] ; then
   /etc/webmin/cfw/extra.rules;
fi

# ----------------------------------------------------------------------------
# Default actions

#  Drop and log all packets.

    /sbin/iptables -A INPUT   -j LOGDROP
#    /sbin/iptables -A OUTPUT   -j LOGDROP
    /sbin/iptables -A FORWARD   -j LOGDROP


