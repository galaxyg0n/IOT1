#!/bin/bash

IFACE="enp6s0"
PC_IP="192.168.50.1"
SUBNET="24"

CONF="/etc/dnsmasq.d/pi-direct.conf"

echo "Enable(e) or Disable(d)?"
read option

if [ $option == "e" ]; then
	echo "[!] - Enabling Pi Direct Ethernet on $IFACE"

	sudo ip link set $IFACE ip
	sudo ip addr flush dev $IFACE
	sudo ip addr add $PC_IP/$SUBNET dev $IFACE

	if [ ! -f "$CONF" ]; then
		echo "interface=$IFACE" | sudo tee $CONF
		echo "dhcp-range=192.168.50.10,192.168.50.20,12h" | sudo tee -a $CONF
	fi

	sudo systemctl start dnsmasq

	echo "Pi Ethernet Mode ENABLED"
fi
if [ $option == "d" ]; then
	echo "[!] - Disabling Pi Direct Ethernet on $IFACE"
	
	sudo systemctl stop dnsmasq
	sudo systemctl restart NetworkManager

	sudo ip addr flush dev $IFACE
	echo "[x] - Check if this looks normal:"
	ip addr show enp6s0

	echo "Pi Ethernet Mode DISABLED"
fi
