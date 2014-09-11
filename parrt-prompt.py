#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
import os
import sys
import re

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

branch = run(['git', 'symbolic-ref', 'HEAD'])
branch = branch.strip()[11:]

res = run(['git','diff','--name-status'])
modified_files = [line for line in res.split('\n') if len(line)>0]
res = run(['git','diff','--staged', '--name-status'])
staged_files = [line for line in res.split('\n') if len(line)>0]

"""
See http://stackoverflow.com/questions/2969214/git-programmatically-know-by-how-much-the-branch-is-ahead-behind-a-remote-branc
## master
If you are ahead:

## master...origin/master [ahead 1]
If you are behind:

## master...origin/master [behind 58]
And for both:

## master...origin/master [ahead 1, behind 58]
"""
ahead = None
behind = None
res = run(['git','status','--porcelain', '--branch', '-uno'])
lines = [line for line in res.split('\n') if len(line)>0]
outofsync = lines[0].decode('utf-8')
behind_regex = re.compile(".*behind ([0-9]+).*")
r = behind_regex.search(outofsync)
if r:
	behind = r.group(1)
ahead_regex = re.compile(".*ahead ([0-9]+).*")
r = ahead_regex.search(outofsync)
if r:
	ahead = r.group(1)

sync_status = ""
if behind:
	sync_status += Down
if ahead:
	sync_status += Up
if len(sync_status)>0:
	sync_status = Red+sync_status+Reset

# if behind and ahead:
# 	sync_status = UpDown

#print ahead, behind

#remote_name = Popen(['git','config','branch.%s.remote' % branch], stdout=PIPE).communicate()[0].strip()
#print "remote", remote_name

dirty = False
if len(modified_files)>0 or len(staged_files):
	dirty = True

if dirty:
	print Host+":"+Yellow+branch+Reset+sync_status+":"+PathShort+" \$ "
else:
	print Host+":"+Green+branch+Reset+sync_status+":"+PathShort+" \$ "
