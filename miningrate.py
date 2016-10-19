#!/usr/bin/env python
###########################################################################
# author: JanKalin
#
# Calculates an estimate of mining rate on this computer
###########################################################################

import argparse
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from prettytable import PrettyTable
from scipy import stats

from zcutils import *

###########################################################################
# Printout functions
###########################################################################

def time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def dtime(delta):
    return str(datetime.timedelta(seconds=int(np.round(delta))))

###########################################################################

parser = argparse.ArgumentParser(description="Estimate mining rate by reading transactions",
                                 fromfile_prefix_chars='@',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--zcash_cli", help="Path to zcash-cli binary.", default="~/zcash/src/zcash-cli")
parser.add_argument("--transactions", help="Process this many transactions", default=10000)
groupdata = parser.add_mutually_exclusive_group()
groupdata.add_argument("--savedata", help="Saves data to 'miningrate.npy' after loading it from blockchain", action='store_true')
groupdata.add_argument("--loaddata", help="Loads data from 'miningrate.npy' instead of loading it from blockchain", action='store_true')
parser.add_argument("--notable", help="Do not print out table", action='store_true')
parser.add_argument("--nostats", help="Do not print out stats", action='store_true')
parser.add_argument("--noprogress", help="Do not display progress", action='store_true')
parser.add_argument("--graph", help="Display graph", action='store_true')
parser.add_argument("--maxdtime", help="Maximum dtime in minutes. Used to skip periods of no activity", type=int, default=0)
args = parser.parse_args()

# dtype for data
dtype=[('height', int), ('time', int), ('dheight', int), ('dtime', int), ('blocktime', float), ('immature', int), ('difficulty', float)]

# Perhaps load data
if args.loaddata:
    data = np.load('miningrate.npy')
    
else: 
    # Create the object, get transactions and find the interesting ones
    zcli = zcli.zcli(args.zcash_cli)
    if not args.noprogress:
        print "Getting transactions ...",
    transactions = zcli.listtransactions(args.transactions)
    if not args.noprogress:
        print "100%"
    generated = [x for x in transactions if 'generated' in x]

    # Create a numpy array and fill it
    data = np.zeros((len(generated),), dtype=dtype)
    if len(generated) > 1 and not args.noprogress:
        progress = utils.Progress("Reading {} blocks ... {{}}% ".format(len(generated)), len(generated))
    for idx, transaction in enumerate(generated):
        if len(generated) > 1 and not args.noprogress:
            progress.step()
        block = zcli.getblock(transaction['blockhash'])
        for field in ['height', 'time', 'difficulty']:
            data[field][idx] = block[field]
        data['immature'][idx] = transaction['category'] == 'immature'
    data['dheight'][1:] = np.diff(data['height'])
    data['dtime'][1:] = np.diff(data['time'])
    data['blocktime'][1:] = data['dtime'][1:]/data['dheight'][1:]
    if args.maxdtime:
        where = np.where(data['dtime'] > 60.*args.maxdtime)
        data = np.delete(data, where)

    # Perhaps save data
    if args.savedata:
        np.save('miningrate.npy', data)

# Table
if not args.notable:
    table = PrettyTable(['height', 'time', 'difficulty', 'immature', 'dheight', 'dtime'])
    for idx in range(len(data)):
        row = [data['height'][idx], time(data['time'][idx]), data['difficulty'][idx], "*" if data['immature'][idx] else ""]
        if idx:
            row += [data['dheight'][idx], dtime(data['dtime'][idx])]
        else:
            row += ["", ""]
        table.add_row(row)
    print table

# Stats
if not args.nostats:
    table = PrettyTable(['qty', 'mean', 'std', 'median'])
    table.float_format = "7.4"
    table.align['qty'] = 'r'
    table.add_row(['difficulty',
                   np.mean(data['difficulty'][1:]),
                   np.std(data['difficulty'][1:]),
                   np.median(data['difficulty'][1:])])
    table.add_row(['dheight',
                   np.mean(data['dheight'][1:]),
                   np.std(data['dheight'][1:]),
                   np.median(data['dheight'][1:])])
    table.add_row(['blockttime',
                   dtime(np.mean(data['blocktime'][1:])),
                   dtime(np.std(data['blocktime'][1:])),
                   dtime(np.median(data['blocktime'][1:]))])
    table.add_row(['dtime',
                   dtime(np.mean(data['dtime'][1:])),
                   dtime(np.std(data['dtime'][1:])),
                   dtime(np.median(data['dtime'][1:]))])
    try:
        delta = 1.*(len(data)-1)/(data['time'][-1] - data['time'][1])*86400
    except:
        delta = 0
    immature = len(np.where(data['immature'])[0]);
    table.add_row(['blocks', "{} + {}".format(len(data)-immature, immature), "", ""])
    table.add_row(['blocks/day', delta, "", ""])
    print table

# Get per-day stats
days = np.unique(data['time']/86400)
daydata = np.zeros((len(days),), dtype=[('time', float), ('dtime', float), ('count', float)])
for idx, day in enumerate(days):
    where = data['time']/86400 == day
    daydata['time'][idx] = day*86400
    daydata['dtime'][idx] = np.mean(data['dtime'][where])
    daydata['count'][idx] = len(np.where(where)[0])
table = PrettyTable(['day', 'dtime', 'count'])
for idx in range(len(daydata)):
    table.add_row([time(daydata['time'][idx]),  daydata['dtime'][idx]/60, daydata['count'][idx]])
print table
    
# Histograms
if args.graph:
    xfmt = mdates.DateFormatter("%d.%m. %H:%M")
    yfmt = mdates.DateFormatter("%H:%M:%S")
    fig = plt.figure()
    fig.autofmt_xdate()

    times = [datetime.datetime.fromtimestamp(x) for x in data['time'][1:]]
    deltas = [datetime.datetime.fromtimestamp(x-3600) for x in data['dtime'][1:]]

    ax = fig.add_subplot(311)
    ax.plot(times, deltas)
    ax.plot(times, [datetime.datetime.fromtimestamp(np.mean(data['dtime'][1:])-3600)]*len(times))
    ax.xaxis.set_major_formatter(xfmt)
    ax.yaxis.set_major_formatter(yfmt)
    plt.xticks(rotation='vertical')

    times = np.array([datetime.datetime.fromtimestamp(x) for x in daydata['time']])
    deltas = np.array([datetime.datetime.fromtimestamp(x-3600) for x in daydata['dtime']])

    try:
        res = stats.mstats.theilslopes(daydata['dtime'], daydata['time'], 0.90)
    except:
        res = None

    ax = fig.add_subplot(312)
    ax.plot(times, deltas)
    if res:
        try:
            ax.plot(times, [datetime.datetime.fromtimestamp(x-3600) for x in res[1] + res[0] * daydata['time']], 'r-')
        except:
            pass
    ax.xaxis.set_major_formatter(xfmt)
    ax.yaxis.set_major_formatter(yfmt)
    ax.set_ylim(int(ax.get_ylim()[0]), (1.0/24)*(int(ax.get_ylim()[1]*24)+1))
    plt.xticks(rotation='vertical')
    
    ax = fig.add_subplot(313)
    ax.plot(times, daydata['count'])
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks(rotation='vertical')
    
    plt.show()


