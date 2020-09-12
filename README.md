# Netdata bitcoind plugin
Plugin to monitor your bitcoin node. This plugin is based on energid plugin ( https://github.com/netdata/netdata/tree/master/collectors/python.d.plugin/energid ), but I made a few modifications to make it work with bitcoin and show different charts. I also include in this repo some alarms so you can monitor your node uptime and sync status. 

## Requirements 
1. netdata: https://github.com/netdata/netdata
1. bitcoin daemon with rpc json api enabled 

## Installation
1. Copy bitcoind.chart.py to your pyhon.d directory, usually /usr/libexec/netdata/python.d/
1. Modify bitcoind.conf file with your bitcoin daemon information and copy file to /etc/netdata/python.d/ directory
1. Optional: copy health.d/bitcoind.conf to /etc/netdata/health.d/ directory
1. Restart netdata

