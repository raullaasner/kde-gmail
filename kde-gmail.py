#!/usr/bin/env python3

# Copyright (C) 2015-2016 Raul Laasner
# This file is distributed under the terms of the GNU General Public
# License, see 'LICENSE' in the root directory of the present
# distribution or http://gnu.org/copyleft/gpl.txt .

from argparse import ArgumentParser
import time
import urllib.request
import feedparser
from subprocess import call
from ctypes import cdll

# Parse command line arguments
parser = ArgumentParser()
parser.add_argument('-u', '--user', nargs=1, help='User name')
parser.add_argument('-p', '--password', nargs=1, help='Password.')
parser.add_argument('-d', '--delay', nargs=1, type=int, default=[120],
                    metavar='N',
                    help='Delay between subsequent checks (default: 120)')
parser.add_argument('-l', '--labels', nargs='+', default=[''], metavar='LABEL',
                    help='Gmail labels to be included (default: Inbox)')
args = parser.parse_args()
if not args.user and not args.password:
    parser.parse_args('-h'.split())
    exit()

WaitBeforeRetry = 600 # In case of failure of opening the feed, the
                      # amount of time to wait before retrying.

# Use res_init from glibc to re-read the DNS configuration file in
# case of connection failures. See
# stackoverflow.com/questions/21356781
libc = cdll.LoadLibrary('libc.so.6')
res_init = libc.__res_init

latest = time.gmtime(0) # Time of the most recent email
latest_prev = latest
# Build the handler
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(
    realm='mail.google.com',
    uri='https://mail.google.com',
    user=args.user[0],
    passwd=args.password[0]
)
opener = urllib.request.build_opener(auth_handler)
while True:
    # Parse the feeds
    feeds = []
    for L in args.labels:
        try:
            data = opener.open('https://mail.google.com/mail/feed/atom/'+L,
                               timeout=args.delay[0])
        except Exception as e:
            time.sleep(WaitBeforeRetry)
            res_init()
            continue
        feeds.append(feedparser.parse(data))
    # Prepare output
    text = ''
    num_msg = 0
    for F in feeds:
        num_msg += len(F.entries)
        for M in F.entries:
            text += '<b>'+M.author+'</b><br>'
            text += '<i>'+M.title+'</i><br>'
            text += '&nbsp;&nbsp;'+M.description+'<br><br>'
            if M.published_parsed > latest: latest = M.published_parsed
    # Call KDialog only if there's new unread mail since the last call
    if text and latest > latest_prev:
        title = str(num_msg)+' new message'
        if num_msg > 1: title += 's'
        call(['kdialog', '--title', title, '--msgbox', text])
        latest_prev = latest

    time.sleep(args.delay[0])
