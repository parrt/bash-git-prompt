#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
import os
import sys
import re
import time

FETCH_REFRESH_INTERVAL_IN_SEC = 30*60 # 30 minutes
FETCH_REFRESH_INTERVAL_IN_SEC = 10

Blue=r'\[\e[01;34m\]'
White=r'\[\e[01;37m\]'
Red=r'\[\e[01;31m\]'
Green=r'\[\e[01;32m\]'
Yellow=r"\[\033[0;33m\]"
Reset=r'\[\e[00m\]'
FancyX=r'\342\234\227'
Checkmark=r'\342\234\223'
PathShort="\w"
Host="\h"

def u2d(s):
	s = s.encode("utf-8")
	values = [oct(ord(c)) for c in s]
	ss = ""
	for v in values:
		ss += "\\"+str(v[1:])
	return ss

Up = u2d(u"\u2912")
Down=u2d(u"\u2913")
UpDown=u2d(u"\u296F")

def run(cmd,failstr=Host+":"+PathShort+" \$ "):
	# print ' '.join(cmd)
	res, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
	err_string = err.decode('utf-8')
	if 'fatal' in err_string:
		if failstr is None:
			return None
		print failstr
		sys.exit(0)
	return res.decode('utf-8')

def repo_root():
	# fatal: Not a git repository (or any of the parent directories): .git
	res = run(['git','rev-parse','--show-toplevel'])
	lines = [line for line in res.split('\n') if len(line)>0]
	if 'fatal' in lines[0]:
		return None
	return lines[0]

def branch():
	branch = run(['git', 'symbolic-ref', 'HEAD'], failstr=None)
	if branch is None:
		return None
	return branch.strip()[11:]

def modified_files():
	res = run(['git','diff','--name-status'])
	return [line for line in res.split('\n') if len(line)>0]

def staged_files():
	res = run(['git','diff','--staged', '--name-status'])
	return [line for line in res.split('\n') if len(line)>0]

def ahead():
	# git rev-list origin/master..HEAD
	br = branch()
	if br is None:
		return 0
	res = run(['git','rev-list','origin/'+ br +'..HEAD'])
	if len(res)>0:
		lines = [line for line in res.split('\n') if len(line)>0]
		return len(lines)
	return None

def fetch_time_cache_file():
	return repo_root()+'/.fetch_time_cache'

def fetch_time_cache_read():
	if not os.path.exists(fetch_time_cache_file()):
		fetch_time_cache_write()
	f = open(fetch_time_cache_file(), 'r')
	cache = f.read()
	f.close()
	prevtime = int(cache)
	return prevtime

def fetch_time_cache_write():
	f = open(fetch_time_cache_file(), 'w')
	cur = int(time.time())
	f.write(str(cur))
	f.close()

def behind():
	# git rev-list HEAD..origin/master
	br = branch()
	if br is None:
		return 0
	res = run(['git','rev-list','HEAD..origin/'+ br], failstr=None)
	n = 0
	if len(res)>0:
		lines = [line for line in res.split('\n') if len(line)>0]
		print lines
		n = len(lines)
	return n

# keep up to date with origin but only fetch every n seconds for speed reasons
def fetch_remote():
	prevtime = fetch_time_cache_read()
	cur = int(time.time())
	# print cur, prevtime
	if (cur - prevtime) >= FETCH_REFRESH_INTERVAL_IN_SEC:
		# reset counter to current time
		fetch_time_cache_write()
		# git fetch IS REQUIRED for comparisons. ugh
		br = branch()
		if br is None:
			return
		run(['git', 'fetch', 'origin', br], failstr=None)

fetch_remote()

sync_status = ""
if behind():
	sync_status += Down
if ahead():
	sync_status += Up
if len(sync_status)>0:
	sync_status = Red+sync_status+Reset

dirty = False
if len(modified_files())>0 or len(staged_files()):
	dirty = True

br = branch()
if br is None:
	print Host+":"+Yellow+"detached"+Reset+":"+PathShort+" \$ "
elif dirty:
	print Host+":"+Yellow+ br +Reset+sync_status+":"+PathShort+" \$ "
else:
	print Host+":"+Green+br+Reset+sync_status+":"+PathShort+" \$ "
