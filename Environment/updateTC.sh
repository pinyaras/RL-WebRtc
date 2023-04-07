#! /usr/bin/env bash

# inspired by
# https://joshrosso.com/docs/2020/2020-09-16-tc/

# tc utility
TC=/sbin/tc

# interface
IF=veth1

# limit
LIMIT=100mbit

# destination
DST_CIDR=10.10.0.10/32

# filter
U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

# create rules
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

# erase existing qdisc
clean() {
    echo "== REMOVING EXISTING QDISC =="
    $TC qdisc del dev $IF root
    echo "== CLEANUP COMPLETE =="
}

# run it
clean
create
