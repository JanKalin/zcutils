#!/usr/bin/env python
###########################################################################
# author: JanKalin
#
# Calculates an estimate of mining rate on this computer
###########################################################################

import argparse
import os
import sys
import tempfile

import numpy as np
from prettytable import PrettyTable

from zcutils import *

###########################################################################
# Printout functions
###########################################################################

def time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def dtime(delta):
    return str(datetime.timedelta(seconds=int(np.round(delta))))

###########################################################################

cachefile = os.path.join(tempfile.gettempdir(), "minerdata.npy")
parser = argparse.ArgumentParser(description="Generate a list of miners",
                                 fromfile_prefix_chars='@',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--zcash_cli", help="Path to zcash-cli binary.", default="~/zcash/src/zcash-cli")
groupdata = parser.add_mutually_exclusive_group()
groupdata.add_argument("--nocache", help="Do not use cache file '{}'".format(cachefile), action='store_true')
parser.add_argument("--top", help="Print only top N miners", type=int, metavar='N')
parser.add_argument("--noprogress", help="Do not display progress", action='store_true')
parser.add_argument("--lastdays", help="Inlude only data from last few days", type=int)
parser.add_argument("--map", help="Map address->name for printing out pool names. Perhaps best set using '@<filename>",
                    nargs='+', metavar='ADDR:NAME')
parser.add_argument("--valuesort", help="Sort output by mined value, not number of blocks", action='store_true')
parser.add_argument("--plaintable", help="Output plain tab-separated table", action='store_true')
args = parser.parse_args()

# Get name map
if args.map:
    namemap = {x[0]:x[1] for x in [x.split(":") for x in args.map]}

# Create the object, get transactions and find the interesting ones
zcli = zcli.zcli(args.zcash_cli)

# dtype for data
dtype=[('n', int), ('time', float), ('value', float), ('address', object)]
tmpdata = []

# Perhaps load cache
cache = np.zeros((0,), dtype=dtype)
cacheblockcount = -1
if not args.nocache:
    try:
        cache = np.load(cachefile)
        cacheblockcount = np.max(cache['n'])
        if not args.noprogress:
            print "{} blocks in cache".format(cacheblockcount)
    except:
        pass

# Get block count and perhap
blockcount = int(zcli.blockcount())

# Perhaps we have all data in cache, otherwise we read it
if blockcount <= cacheblockcount:
    data = cache
else:
    if not args.noprogress:
        progress = utils.Progress(fmt="Reading blocks {} to at least {}: {{}}".format(cacheblockcount+1, blockcount), value=cacheblockcount)
    blockhash = zcli.getblockhash(cacheblockcount+1)
    block = zcli.getblock(blockhash)
    while True:
        if not args.noprogress:
            progress.step()
        if not block['height']:
            tmpdata.append([0, block['time'], 0, 'GENESIS'])
        for txid in block['tx']:
            try:
                rawtx = zcli.getrawtransaction(txid)
                tx = zcli.decoderawtransaction(rawtx)
                try:
                    tx['vin'][0]['coinbase']
                    tmpdata.append((block['height'], block['time'], tx['vout'][0]['value'],
                                    tx['vout'][0]['scriptPubKey']['addresses'][0]))
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass
            except KeyboardInterrupt:
                sys.exit()
            except:
                pass
        try:
            block = zcli.getblock(block['nextblockhash'])
        except KeyboardInterrupt:
            sys.exit()
        except:
            if not args.noprogress:
                progress.done()
            break
    if not len(tmpdata):
        print "No blocks found"
        exit(0)

    # Create a numpy array and fill it
    data = np.zeros((len(tmpdata),), dtype=dtype)
    for idx, line in enumerate(tmpdata):
        data['n'][idx], data['time'][idx], data['value'][idx], data['address'][idx] = line

    # Perhaps save data
    if not args.nocache:
        data = np.concatenate((cache, data))
        np.save(cachefile, data)

# Perhaps prune dates
if args.lastdays:
    where = np.where(data['time'] < data['time'][-1]-86400*args.lastdays)
    if len(where[0]) and not args.noprogress:
        print "Keeping last {} blocks".format(len(data)-len(where[0]))
    data = np.delete(data, where)

# Get unique addresses and print stats for each one
addresses = np.unique(data['address'])
summary = np.zeros((len(addresses),), dtype=dtype)
for idx, address in enumerate(addresses):
    where = np.where(data['address'] == address)
    count = len(where[0])
    value = np.sum(data['value'][where])
    try:
        name = namemap[address]
    except:
        name = address
    summary['n'][idx], summary['value'][idx], summary['address'][idx] = count, value, name
summary[:] = np.sort(summary, order=('value' if args.valuesort else 'n'))[::-1]

# Print
totalcount = np.sum(summary['n'])
totalvalue = np.sum(summary['value'])
header = ['blocks', '% bl.', 'value', '% val.', 'name/address']
if args.plaintable:
    print "\t".join(header)
else:
    table = PrettyTable(['blocks', '% bl.', 'value', '% val.', 'name/address'])
    table.float_format = "9.4"
    table.align['blocks'] = 'r'
for idx in range(len(summary) if not args.top else args.top):
    row = [summary['n'][idx], 100.*summary['n'][idx]/totalcount,
           summary['value'][idx], 100.*summary['value'][idx]/totalcount,
           summary['address'][idx]]
    if args.plaintable:
        print "\t".join([str(x) for x in row])
    else:
        table.add_row(row)
if not args.plaintable:
    print table
