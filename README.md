KDE-Gmail
=========

A small KDE-oriented script for checking Gmail.

Brief description
-----------------

A light-weight Python script for checking new email via the Gmail Atom feed. There is just one call to KDialog, making it easy to port to other DEs.

Usage
-----

The script requires the --user and --password arguments and optionally --labels and --delay (in seconds). Any spaces in the labels should be replaced by dashes. Note that Social, Promotions, etc. are part of Inbox.

Example: add `/usr/bin/kde-gmail.py -u <user> -p <password> -l Inbox Foo -d 60` to Autostart.

Troubleshooting
---------------

A good place to bring up any issues is https://github.com/raullaasner/kde-gmail/issues.

License
-------

This project is distributed under the terms of the GNU General Public License, see LICENSE in the root directory of the present distribution or http://gnu.org/copyleft/gpl.txt.
