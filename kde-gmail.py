#!/usr/bin/env python

# Copyright (C) 2015 Raul Laasner
# This file is distributed under the terms of the GNU General Public
# License, see 'LICENSE' in the root directory of the present
# distribution or http://gnu.org/copyleft/gpl.txt .

from argparse import ArgumentParser
import time
import urllib.request as U
import feedparser
from subprocess import call

# Parse command line arguments
parser = ArgumentParser()
parser.add_argument('-u', '--user', nargs=1, help='User name')
parser.add_argument('-p', '--password', nargs=1, help='Password.')
parser.add_argument('-d', '--delay', nargs=1, type=int, default=[120],
                    metavar='N',
                    help='Delay between subsequent checks (default: 120)')
parser.add_argument('-l', '--labels', nargs='+', default=[''], metavar='LABEL',
                    help='GMail labels to be included (default: Inbox)')
args = parser.parse_args()
if not args.user and not args.password:
    parser.parse_args('-h'.split())
    exit()

# Main
latest = time.gmtime(0) # Time of the latest email
latest_prev = latest
while True:
    # Login and fetch data
    auth_handler = U.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='mail.google.com',
        uri='https://mail.google.com',
        user=args.user[0],
        passwd=args.password[0]
    )
    opener = U.build_opener(auth_handler)
    # Parse the feeds
    feeds = []
    for L in args.labels:
        data = opener.open('https://mail.google.com/mail/feed/atom/'+L)
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
    # Call KDialog only if there's *new* unread mail since the last call
    if text and latest > latest_prev:
        title = str(num_msg)+' new message'
        if num_msg > 1: title += 's'
        call(['kdialog', '--title', title, '--msgbox', text])
        latest_prev = latest
            
    time.sleep(args.delay[0])
