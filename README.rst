(Idea and first version from Stan Vitkovsky. Forked from
https://code.google.com/p/upodder/)

Simple podcast downloader
=========================

A simple command-line podcast downloader. Can be run from cron. Simply
add your RSS feeds in ``~/.upodder/subscriptions`` and watch your latest
podcasts come in. Destination dir, filename, folder structures, etc can
all be customized.

Please report any bugs on
`Github <https://github.com/manuelRiel/upodder>`__. I will promptly fix
them.

Installation
------------

``pip install upodder``

Usage
-----

After installation, run ``upodder``. It will initialize ``~/.upodder/``
to keep your subscriptions and a small DB of seen files. After that
simply enter you feeds in ``~/.upodder/subscriptions``.

The next time you run ``upodder``, it will go over each feed and
download new entries to ``~/Downloads/podcasts``.

To view available options, run ``upodder --help``

History and motivation
----------------------

I've been using this script for several years and the project seems
abandoned on Google Code. To keep it from disappearing, after Google
Code is shut down, I've forked it here and refactored most parts. To
quote the original author, Stan Vitkovsky and his motivation:

"I needed a simple console podcast downloader.

I did not find any one suitable for my needs (podracer lacked ATOM
support, hpodder segfaulted from time to time and didn't understand ATOM
as well. Both of then were unaware for entries IDs, only for mp3 file
names, which are subjects to be changed, as on rpod.ru).

My usage scenario is to download unseen enclosures, place them in the
folder with a name ~/podcasts/%d-%m-%Y/{somename}.mp3 (like podracer
does) and then rsync them to my MP3 player.

Also, I wrote a bash script, which mounts my player with pmount-hal,
calls podracer, rsyncs my player and unmounts it safely."

Further Contributors
--------------------

-  *akira (gaspar0069)*: Add support for multiple file extensions and
   fix file move bug.
