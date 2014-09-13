#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
import os
import sys
import re
import time

Blue=r'\[\e[01;34m\]'
White=r'\[\e[01;37m\]'
Red=r'\[\e[01;31m\]'
Green=r'\[\e[01;32m\]'
Yellow=r"\[\033[0;33m\]"
Reset=r'\[\e[00m\]'
FancyX=r'\342\234\227'
Checkmark=r'\342\234\223'
PathShort="\w"

def u2d(s):
	s = s.encode("utf-8")
	values = [oct(ord(c)) for c in s]
	ss = ""
	for v in values:
		ss += "\\"+str(v[1:])
	return ss

# '\xe2\x86\x91'
#print ''.join(["\\"+oct(ord(c)) for c in Up])
#'\xe2\x86\x93'
#print ''.join(["\\"+oct(ord(c)) for c in Down])
#Up=r'\342\206\221'
Up = u2d(u"\u2191")
Down=u2d(u"\u2186")
Up = u2d(u"\u2912")
Down=u2d(u"\u2913")
UpDown=u2d(u"\u296F")
#UpDown=u2d(u"\u21C5")
Host="\h"

def run(cmd,fail=Host+":"+PathShort+" \$ "):
	res, err = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()
	err_string = err.decode('utf-8')
	if 'fatal' in err_string:
		print fail
		sys.exit(0)
	return res.decode('utf-8')

def branch():
	branch = run(['git', 'symbolic-ref', 'HEAD'])
	return branch.strip()[11:]

def modified_files():
	res = run(['git','diff','--name-status'])
	return [line for line in res.split('\n') if len(line)>0]

def staged_files():
	res = run(['git','diff','--staged', '--name-status'])
	return [line for line in res.split('\n') if len(line)>0]

def ahead():
	# git rev-list origin/master..HEAD
	res = run(['git','rev-list','origin/'+branch()+'..HEAD'])
	if len(res)>0:
		lines = [line for line in res.split('\n') if len(line)>0]
		return lines[0].decode('utf-8')
	return None

# only fetch every 10 requests for behind() for speed reasons
def behind_cache_init():
	f = open('.behind_cache', 'w')
	f.write("1 0")
	cache = "1 0"
	f.close()
	return cache


def behind_cache_read():
	if not os.path.exists('.behind_cache'):
		cache = behind_cache_init()
	else:
		f = open('.behind_cache', 'r')
		cache = f.read()
		f.close()
	count,dirty = cache.split(' ')
	count = int(count)
	dirty = int(dirty)
	return (count,dirty)


def behind_cache_write(count, dirty):
	f = open('.behind_cache', 'w')
	f.write("%d %s" % (count, dirty))
	f.close()


def behind():
	count,dirty = behind_cache_read()
	if not count % 15==0:
		count += 1
		behind_cache_write(count, dirty)
		return dirty
	count = 1

	# git fetch IS REQUIRED. ugh
	# git rev-list HEAD..origin/master
	run(['git','fetch','origin', branch()])
	res = run(['git','rev-list','HEAD..origin/'+branch()])
	dirty = 0
	if len(res)>0:
		lines = [line for line in res.split('\n') if len(line)>0]
		files = lines[0].decode('utf-8')
		if len(files)>0:
			dirty = 1

	behind_cache_write(count, dirty)
	return dirty

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

if dirty:
	print Host+":"+Yellow+branch()+Reset+sync_status+":"+PathShort+" \$ "
else:
	print Host+":"+Green+branch()+Reset+sync_status+":"+PathShort+" \$ "
