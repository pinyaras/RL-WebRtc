#!/usr/bin/env bash

# Set up namespaces, veth links
# bridge, routes, and forwarding
# rules for AlphaRTC Docker Experiment

##############
# NAMESPACES #
##############

NS1="ns1"
NS2="ns2"

# create namespace
ip netns add $NS1
ip netns add $NS2

##############
# VETH PEERS #
##############

VETH1="veth1"
VPEER1="vpeer1"

VETH2="veth2"
VPEER2="vpeer2"

# create veth link
ip link add ${VETH1} type veth peer name ${VPEER1}
ip link add ${VETH2} type veth peer name ${VPEER2}

# setup veth link
ip link set ${VETH1} up
ip link set ${VETH2} up

# add peers to ns
ip link set ${VPEER1} netns ${NS1}
ip link set ${VPEER2} netns ${NS2}

##############
# Interfaces #
##############

VPEER_ADDR1="10.10.0.10"
VPEER_ADDR2="10.10.0.20"

# setup loopback interface
ip netns exec ${NS1} ip link set lo up
ip netns exec ${NS2} ip link set lo up

# setup peer ns interface
ip netns exec ${NS1} ip link set ${VPEER1} up
ip netns exec ${NS2} ip link set ${VPEER2} up

# assign ip address to ns interfaces
ip netns exec ${NS1} ip addr add ${VPEER_ADDR1}/16 dev ${VPEER1}
ip netns exec ${NS2} ip addr add ${VPEER_ADDR2}/16 dev ${VPEER2}

##########
# BRIDGE #
##########

BR_ADDR="10.10.0.1"
BR_DEV="br0"

# setup bridge
ip link add ${BR_DEV} type bridge
ip link set ${BR_DEV} up

# assign veth pairs to bridge
ip link set ${VETH1} master ${BR_DEV}
ip link set ${VETH2} master ${BR_DEV}

# setup bridge ip
ip addr add ${BR_ADDR}/16 dev ${BR_DEV}

# add default routes for ns
ip netns exec ${NS1} ip route add default via ${BR_ADDR}
ip netns exec ${NS2} ip route add default via ${BR_ADDR}

############
# IPTABLES #
############

# enable ip forwarding
bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

# allow traffic accross bridge outside containers
iptables -t nat -A POSTROUTING -s ${BR_ADDR}/16 ! -o ${BR_DEV} -j MASQUERADE
iptables -t nat -A POSTROUTING -s 10.10.0.1/16 ! -o br0 -j MASQUERADE
