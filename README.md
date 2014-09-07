bash-git-prompt
===============

# What/Why?

My own variation on the bash git prompt. I took most of the functionality
from [magicmonty/bash-git-prompt](https://github.com/magicmonty/bash-git-prompt/blob/master/gitstatus.py). I wanted something simpler in functionality and implementation.

# Install

You can put file [`parrt-prompt.py`](parrt-prompt.py) anywhere but that incantation assumes it’s in the ~/.bash directory.

Add the following incantation to your `.bash_profile` or `.bashrc`, if you are using that file.

```
PROMPT_COMMAND='echo -n -e "\033]0;`pwd`\007"; PS1="`~/.bash/parrt-prompt.py`"'
```

If you want to get fancy, the following variation will also set the title of the window (on OS X at least) to the current working directory.

```
PROMPT_COMMAND='echo -n -e "\033]0;`pwd`\007"; PS1="`~/.bash/parrt-prompt.py`"'
```

# Misc

You might want to update the bash that sits on OS X by default:

```
$ brew upgrade bash
```
