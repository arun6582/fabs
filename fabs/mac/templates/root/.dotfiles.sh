#!/bin/bash

##############################CONFIGS STARTS###################################

HOME="{{ home }}"

DIRS="$HOME/.ssh/
$HOME/bin/"

NAME="{{ alias }}"

FILES="$HOME/.vimrc
$HOME/.bash_history
$HOME/.bash_profile
$HOME/.inputrc
$HOME/.gitconfig
$HOME/.screenrc"

##############################CONFIGS ENDS#####################################

bkp="$HOME/dotfiles"
temp="$HOME/tmp/dotfiles"
content="$temp/$NAME"

for file in $FILES
do
    dir=`dirname $file`
    mkdir -p $content$dir
    rsync -az $file $content$dir
done

for dir in $DIRS
do
    mkdir -p $content$dir
    rsync -avh $dir $content$dir --exclude=.git
done

crontab -l > $content/crontab
uptime > $content/uptime

rsync -avh $content/ $bkp/$NAME/ --delete
rm -rf $content

git --work-tree=$bkp --git-dir=$bkp/.git add .
msg=`git --work-tree=$bkp --git-dir=$bkp/.git status -s`
git --work-tree=$bkp --git-dir=$bkp/.git commit -m "$NAME | $msg"
git --work-tree=$bkp --git-dir=$bkp/.git pull origin master --no-edit
git --work-tree=$bkp --git-dir=$bkp/.git push origin master
