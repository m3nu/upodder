#!/usr/bin/env python

import feedparser
import time
import hashlib
import os
from os.path import expanduser
import logging
from ConfigParser import ConfigParser
import urllib
import re
import urlparse

configpath=expanduser("~/.upodder.ini")

yes = [1,"1","on","yes","Yes","YES","y","Y","true","True","TRUE","t","T"]
no = [0,"0","off","no","No","NO","n","N","false","False","FALSE","f","F"]
configcomment = ['#',';','$',':','"',"'"]
badfnchars = re.compile('[^\w]+',re.LOCALE)

defaults = {
		'basedir': '~/.upodder',
		'podcastsdir': '~/PODCASTS',
		'filename': '%(today)s/%(id)s.mp3',
		'subscriptions': '%(basedir)s/subscriptions',
		'seendb': '%(basedir)s/seen.db',
		'tmpdir': '%(basedir)s/temp',
		'logfile': '%(basedir)s/upodder.log',
		'logtofile': "no",
		'logtoconsole': "yes",
		'oldness': 1209600,
		'loglevel': logging.DEBUG,
		'reverseorder': "yes",
}

def purgeSeenDB(oldness):
	"""Rids of records older than oldness argument in seendb"""
	if not os.path.exists(seendb):
		l.info("Creating empty seen database file %s"%seendb)
		open(seendb,'a').close()
		return
	newseendb = seendb + '.tmp'
	ns = open(newseendb,'a')
	now = time.time()
	for s in open(seendb,'r'):
		if len(s) >= 52 and int(now - int(s[41:52])) < oldness: ns.write(s)
		else: l.debug("Expiring (%s)"%s.strip())
	ns.close()
	os.remove(seendb)
	os.rename(newseendb,seendb)

def entryId(entry):
	"""Returns ID of entry"""
	return hashlib.sha1(entry.get('id')).hexdigest()

def entryTime(entry):
	"""Returns tuple in time.localtime() format"""
	return entry.get('updated_parsed',entry.get('published_parsed',entry.get('created_parsed',time.localtime())))

def markEntrySeen(entry):
	"""Marks entry as seen in seen DB"""
	eid = entryId(entry)
	l.info("Marking [%s] (%s) as seen"%(entry.get('title'),eid))
	open(seendb,'a').write("%s %011i\n"%(eid,int(time.time())))

def isEntrySeen(entry):
	"""Returns True if entry already seen. False otherwise"""
	if not os.path.exists(seendb):
		l.info("Creating empty seen database file %s"%seendb)
		open(seendb,'a').close()
		return False
	eid = entryId(entry)
	for s in filter(lambda x: len(x) >= 40,open(seendb,'r')):
		if eid == s[0:40]:
			l.debug("Already seen: [%s] (%s)"%(entry.get('title'),eid))
			return True
	return False

def isEntryOld(entry, oldness):
	"""Returns True if entry is too old (defined by oldness variable), False otherwise"""
	result = False
	entrytime = entryTime(entry)
	if (time.time() - time.mktime(entrytime)) > oldness:
		l.info("Too old for us: [%s] <%s>)"%(entry.get('title'),time.asctime(entrytime)))
		result = True
	return result

def retrieveURL(url,file):
	"""Downloads URL to file, returns file name of download (from URL or Content-Disposition)"""
	if not os.path.exists(os.path.dirname(file)): os.makedirs(os.path.dirname(file),0700)
	(scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)
	filename = path.split("/")[-1]
	try:
		l.debug("Downloading {%s} to {%s}"%(url,os.path.basename(file)))
		urllib.urlretrieve(url,file)
	except Exception, e:
		l.error("Download exception occured: %s"%e)
		return False
	
	if not filename:
		filename = "Untitled.mp3"
	return filename

def downloadEnclosure(enclosure, entry, feed):
	"""Performs downloading of specified file. Returns True on success and False in other case"""

	# Donloading enclosure to specified file
	downloadto = tmpdir + os.sep + entryId(entry)

	try:
		filename = retrieveURL(enclosure.get('href'),downloadto)
	except KeyboardInterrupt:
		l.info("Download aborted by Ctrl+c")
		try:
			user_wish = raw_input("Do you like to mark item as read? (y/N): ")
			if user_wish in yes:
				return True
		except KeyboardInterrupt:
			print "No"
		return False

	if not filename: return False

	# Move downloaded file to its final destination
	moveto = podcastsdir + os.sep + generateFileName(filename, entry, feed)
	l.debug("Moving {%s} to {%s}"%(downloadto,moveto))
	if not os.path.exists(os.path.dirname(moveto)): os.makedirs(os.path.dirname(moveto),0750)
	os.rename(downloadto,moveto)
	return True

def generateFileName(filename, entry, feed):
	"""Generates file name for this enclosure based on config settins"""
	(year,month,day,hour,minute,second,weekday,yearday,leap) = time.localtime()
	subst = { 
		'today': '%i-%02i-%02i'%(year,month,day),
		'entry_date': '%i-%02i-%02i'%entryTime(entry)[0:3],
		'id': entryId(entry),
		'entry_title': re.sub(badfnchars,'_',entry.get('title')),
		'feed_href': re.sub(badfnchars,'_',feed.href.split('://')[-1]),
		'feed_title': re.sub(badfnchars,'_',feed.feed.get('title',feed.href)),
		'original_filename': re.sub(badfnchars,'_',filename),
	}
	return c.get('DEFAULT','filename',vars=subst)

def manageEntry(entry, feed):
	"""We'll deal with this entry"""
	
	# Let's check if we worked on this entry earlier...
	if isEntrySeen(entry): return
	
	# Let's check the entry's date
	if isEntryOld(entry, int(c.get('DEFAULT','oldness'))):
		markEntrySeen(entry)
		return

	# This post is neither seen, nor too old for us.
	l.info("Recent podcast: [%s]"%(entry.get('title')))
	# Search for mpeg enclosures
	for enclosure in filter(lambda x: x.get('type') == 'audio/mpeg',entry.get('enclosures',[])):
		# Work only with first found audio/mpeg enclosure (Bad Thing? maybe :( )
		if downloadEnclosure(enclosure,entry,feed): markEntrySeen(entry)
		break

def manageFeed(url):
	"""Let's deal with this podcast feed"""
	feed = feedparser.parse(url)
	if feed.bozo and type(feed.bozo_exception) != type(feedparser.CharacterEncodingOverride()):
		l.error("Erroneous feed URL: %s (%s)"%(url,feed.bozo_exception))
		return
	l.info("Checking feed: {%s}"%feed.feed.title)
	if c.get('DEFAULT','reverseorder') in yes:
		feed.entries.reverse()
	for entry in feed.entries: manageEntry(entry, feed)

# Initializing config file
c = ConfigParser(defaults)
if not os.path.exists(configpath):
	c.write(open(configpath,'a'))
c.read(configpath)


# Initializing logging
l = logging.Logger('upodder',int(c.get('DEFAULT','loglevel')))

if c.get('DEFAULT','logtoconsole') in yes:
	stderrHandler = logging.StreamHandler()
	stderrHandler.setFormatter(logging.Formatter('%(message)s'))
	l.addHandler(stderrHandler)

if c.get('DEFAULT','logtofile') in yes:
	fileHandler = logging.FileHandler(expanduser(c.get('DEFAULT','logfile')),'a')
	fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)s (%(levelname)s): %(message)s'))
	l.addHandler(fileHandler)

# Initializing necessary files and directories
basedir =	expanduser(c.get('DEFAULT','basedir'))
podcastsdir =	expanduser(c.get('DEFAULT','podcastsdir'))
tmpdir =	expanduser(c.get('DEFAULT','tmpdir'))
subscriptions =	expanduser(c.get('DEFAULT','subscriptions'))
seendb =	expanduser(c.get('DEFAULT','seendb'))

if not os.path.exists(basedir):
	l.info("Creating base dir %s"%basedir)
	os.makedirs(basedir,0700)

if not os.path.exists(subscriptions):
	l.info("Creating empty subscriptions file %s"%subscriptions)
	open(subscriptions,'a').write("# Add your RSS/ATOM subscriptions here.\n\n")

#Processing feed URLs
for url in map(lambda x: x.strip(), open(subscriptions)):
	if not url: continue
	if url[0] in configcomment: continue
	manageFeed(url)

l.info("Purging seendb")
purgeSeenDB(int(c.get('DEFAULT','oldness') * 2))

