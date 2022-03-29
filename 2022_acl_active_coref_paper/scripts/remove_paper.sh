#!/bin/bash
cd $1
REMOTE_URL=$(git config --get remote.origin.url)
echo $REMOTE_URL
cd - > /dev/null 2>&1

read -p "Completely remove paper submodule $1 (y/n)? " -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git submodule deinit -f $1
    git rm -rf $1
    rm -rf .git/modules/$1
fi

#read -p "Migrate paper to new directory (y/n)? " -r
#echo    # (optional) move to a new line
#if [[ $REPLY =~ ^[Yy]$ ]]
#then
    #echo Which year?
    #read YEAR
    #echo Which venue?
    #read VENUE
    #mkdir -p $YEAR/$VENUE
    #cd $YEAR/$VENUE
    #git submodule add $REMOTE_URL
    #cd $(basename $1)
    #chmod +x scripts/*
    #git config core.fileMode false # prevent Overleaf override permissions
#fi

