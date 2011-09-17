SUMMARY
=======

a diablo III network protocol simulator / replayer

version
-------

1.01 17.09.2011

author
------

sku/thesku

description
-----------

parses diablo3 tcp streams and maps the packets to their respective
protobuf messages, simulates client and server behaviour and keeps track
of bound services / responses etc.

credits
-------

shadow^dancer, TOM_RUS, #d3.dev, diablo3dev.com

legal
-----

code posted to public domain by sku, no copyright
use at your own risk

DATA FILE FORMAT
================

1) open wireshark
2) filter for tcp.srcport==1119||tcp.dstport==1119
3) rightclick any packet -> Follow TCP stream
4) save all bytes to all.dat
5) save client->server bytes to c2s.dat
6) save server->client bytes to s2c.dat
7) place these 3 files in the ./data folder

OMG
===

yes, this is a poc, it's ugly and has alot of repetitive code
get over it