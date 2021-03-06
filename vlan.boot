#!/bin/sh
# 
# Cumulus Firewall 
# Copyright (C) 2000  �yvind Jelstad, Cumulus IT AS
# 
# $Id: vlan.boot,v 1.3 2002/12/15 20:20:20 oyvind Exp $

DHCPLIST="" # initialize list of interfaces to be passed to dhcpd startup
	 
# comma-sep list of DNS servers to be used in generated vlan-dhcpd.conf
DNSLIST="192.168.50.100, 193.212.1.11"
DOMAIN="cumulus.no"
	   
# VLANs that will NOT use DHCP 
# make sure not to overlap with VLAN_DHCP list above            
VLAN_NO_DHCP="101 102"  #leave blank or add interface number
	          
# VLAN interfaces that will use DHCP
# NOTES: 
#   avoid vlan 1 - Reasons: 
#      -CISCO uses 1 as a DEFAULT_VLAN
#      -we're using 192.168.1.0 for eth1
#   max VLANs is 253 (1 - 254) here since we're using a 192.168.xxx.0 subnet in 
#     dhcpd.conf setup for -each- VLAN interface added
# make sure not to overlap with VLAN_NO_DHCP list below  
     VLAN_DHCP="2 3 4"  
     
     
#Real interface:
REALIF="eth0"
########################## START
case $1 in 
 start)
 echo "# DHCP for VLAN automaticly generated by vlan.boot"  > /tmp/vlan-dhcpd.conf
  echo "ddns-update-style none;"  >> /tmp/vlan-dhcpd.conf

# use interfaces names of (example) vlan8 vs. eth1.8 
# so that iptables doesn't gripe about the "dot" in interface names
# like eth1.3
/usr/bin/vconfig set_name_type VLAN_PLUS_VID_NO_PAD

######################### VLANs WITH DHCP
for i in $VLAN_DHCP
do
  echo "Creating VLAN $i..."
  /usr/bin/vconfig add $REALIF $i

  echo "bringing VLAN $i interface up..."
  /sbin/ifconfig vlan$i 192.168.${i}.1 up
  
  # add this interface to the list that will get passed to DHCPD startup
  DHCPLIST="$DHCPLIST vlan$i"

echo "subnet 192.168.$i.0 netmask 255.255.255.0 {
# --- default gateway
        option routers                  192.168.$i.1;
        option subnet-mask              255.255.255.0;
        option domain-name-servers      $DNSLIST;
	option domain-name      \"$DOMAIN\";
        range dynamic-bootp 192.168.$i.20 192.168.$i.240;
        default-lease-time 21600;
        max-lease-time 43200;
}" >> /tmp/vlan-dhcpd.conf
#        option time-offset              +2;

done

######################### VLANs WITHOUT DHCP
for x in $VLAN_NO_DHCP
do
    echo "Creating non-DHCP VLAN $x..."
    /usr/bin/vconfig add $REALIF $x

   echo "bringing non-DHCP VLAN $x interface up..."
  /sbin/ifconfig vlan$x 192.168.${x}.1 up
done
  
# insert one final rule for all VLANs at the TOP of the FORWARD table
#/sbin/iptables -I FORWARD -i vlan+ -o eth0 -j ACCEPT

#Stop dhcpd
#if [ -f /var/lock/subsys/dhcpd ]; then
#  /etc/rc.d/init.d/dhcpd stop
#fi

# start DHCPD back up with specific interfaces
#echo "Starting DHCP for $DHCPLIST"
#/etc/rc.d/init.d/dhcpd start "$DHCPLIST"

# move vlan-dhcpd.conf file after starting
#mv /tmp/vlan-dhcpd.conf /tmp/vlan-dhcpd.conf-OLD
;;

########################## STOP
stop)
#Stop dhcpd
#/etc/rc.d/init.d/dhcpd stop

# restart iptables since we inserted rules above
#/etc/rc.d/init.d/iptables restart

# now remove VLAN interfaces
for i in `ls /proc/net/vlan|grep -v config`
do
/usr/bin/vconfig rem $i

done
;;

########################## RESTART
restart)
$0 stop
$0 start
;;

########################## USAGE
*)
echo "usage: $0 {start|stop|restart}"
;;
esac
