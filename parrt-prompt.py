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

def behind():
	# git rev-list HEAD..origin/master
	res = run(['git','rev-list','HEAD..origin/'+branch()])
	if len(res)>0:
		lines = [line for line in res.split('\n') if len(line)>0]
		return lines[0].decode('utf-8')
	return None

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
