#!/bin/sh

GIT="echo git"
if test "x$1" = "xgo"; then
  GIT=git
  echo "Setting up stuff in this repo's .git/config"
else
  echo "------------------------------------------------------------------------------"
  echo "This script can setup a few git aliases and options for you."
  echo "It'll now show what would be done; if you want to actually go ahead, run ./bin/git-setup.sh go"
  echo "------------------------------------------------------------------------------"
fi


$GIT config core.autocrlf input
$GIT config core.safecrlf true
$GIT config alias.co checkout
$GIT config alias.ci commit
$GIT config alias.st status
$GIT config alias.br branch
$GIT config alias.hist "log --pretty=format:\"%h %ad | %s%d [%an]\" --graph --date=short"
$GIT config alias.type "cat-file -t"
$GIT config alias.dump "cat-file -p"
$GIT config alias.xpush "!bin/run-push-tests.sh && git push origin master"
$GIT config alias.xclean "clean -Xdf"
