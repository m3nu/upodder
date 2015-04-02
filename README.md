(Idea and first version from Stas Vitkovsky. Forked from https://code.google.com/p/upodder/)

#Simple podcast downloader

I've been using this script for several years and the project seems abandoned on Google Code. To keep it from disappearing, after Google Code is shut down, I've forked it here and refactored most parts:

- be more object-oriented
- use sqlite instead of text file to keep seen entries
- add progress bar for downloads
- test with more feeds to improve stability
- add basic unit tests
- use the more reliable `requests` library for downloading
- use command line arguments instead of the `.ini` file.

To quote the original author, Stas Vitkovsky and his motivation:

"I needed a simple console podcast downloader.

I did not find any one suitable for my needs (podracer lacked ATOM support, hpodder segfaulted from time to time and didn't understand ATOM as well. Both of then were unaware for entries IDs, only for mp3 file names, which are subjects to be changed, as on rpod.ru).

My usage scenario is to download unseen enclosures, place them in the folder with a name ~/podcasts/%d-%m-%Y/{somename}.mp3 (like podracer does) and then rsync them to my MP3 player.

Also, I wrote a bash script, which mounts my player with pmount-hal, calls podracer, rsyncs my player and unmounts it safely."

## Installation

At some point this app will be available on pypi. Until then, clone this repository, install requirements from `requirements.txt` and add upodder.py in your `PATH`.

```
git clone https://github.com/manuelRiel/upodder
cd upodder
pip install -r requirements.txt
./upodder
```
