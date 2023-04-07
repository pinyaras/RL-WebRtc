#! /usr/bin/env bash

##################################################
# Traffic shaping method inspired by             #
# https://joshrosso.com/docs/2020/2020-09-16-tc/ #
##################################################

##############
# PARAMETERS #
##############

TC=/sbin/tc             # tc utility
IF=veth1                # interface
LIMIT=100mbit           # rate limit (NOTE: this could be changed to user input)
DST_CIDR=10.10.0.10/32  # destination IP
U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"  # filter template

#############
# FUNCTIONS #
#############

# Create the tc rules
create() {
    echo "== SHAPING INIT =="

    # set up root qdisc
    $TC qdisc add dev $IF root handle 1:0 htb \
        default 30

    # set up htb class
    $TC class add dev $IF parent 1:0 classid \
        1:1 htb rate $LIMIT

    # establish filter
    $U32 match ip dst $DST_CIDR flowid 1:1

    echo "== SHAPING DONE =="
}

# Erase existing qdisc
clean() {
    echo "== REMOVING EXISTING QDISC =="
    $TC qdisc del dev $IF root
    echo "== CLEANUP COMPLETE =="
}

##############
# MAIN SCOPE #
##############

clean   # run the clean function to remove existing qdisc definitions
create  # run the create function to create a new qdisc hierarchy
