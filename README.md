KDE-Gmail
=========

A small KDE-oriented script for checking GMail.

Brief description
-----------------

A light-weight Python script for checking new email via the GMail Atom feed. This is a fairly elementary implementation. Any suggestions are welcome. Concerning KDE dependency, there is just one call to KDialog, triggered by new email, and it is thus probably not difficult to port it to other DEs.

Usage
-----

The script requires the --user and --password arguments and optionally --labels and --delay (in seconds). Any spaces in the labels should be replaced by dashes. Note that Social, Promotions, etc. are part of Inbox.

Troubleshooting
---------------

A good place to bring up any issues is https://github.com/raullaasner/kde-gmail/issues.

License
-------

This project is distributed under the terms of the GNU General Public License, see LICENSE in the root directory of the present distribution or http://gnu.org/copyleft/gpl.txt.
