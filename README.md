(forked from https://code.google.com/p/upodder/)

#Simple podcast downloader
I needed a simple console podcast downloader.

I did not find any one suitable for my needs (podracer lacked ATOM support, hpodder segfaulted from time to time and didn't understand ATOM as well. Both of then were unaware for entries IDs, only for mp3 file names, which are subjects to be changed, as on rpod.ru).

My usage scenario is to download unseen enclosures, place them in the folder with a name ~/podcasts/%d-%m-%Y/{somename}.mp3 (like podracer does) and then rsync them to my MP3 player.

Also, I wrote a bash script, which mounts my player with pmount-hal, calls podracer, rsyncs my player and unmounts it safely.
