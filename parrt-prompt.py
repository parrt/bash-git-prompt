#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
import os
import sys

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

dirty = len(modified_files)>0 or len(staged_files)

if dirty:
	print Host+":"+PathShort+" "+Yellow+branch+Reset+" \$ "
else:
	print Host+":"+PathShort+" "+Green+branch+" "+Checkmark+Reset+" \$ "
