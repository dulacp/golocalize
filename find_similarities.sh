#!/usr/bin/env bash

# base for comparing
BASE="en"

# retrieve the langage to compare
COMPARE=$1

# Syntax sugar.
indent() {
  RE="s/^/       /"
  [ $(uname) == "Darwin" ] && sed -l "$RE" || sed -u "$RE"
}

# Heroku style Steps
function puts-step (){
  echo "-----> $@"
}

# Heroku style Warnings
function puts-warn (){
  echo " !     $@"
}

# change current dir
DIR=$(cd $(dirname $0); pwd)
puts-step "Change the directory for $DIR"

# files
BASE_FILE="$BASE.lproj/Localizable.strings"
COMPARE_FILE="$COMPARE.lproj/Localizable.strings"
puts-step "Compare file '$COMPARE_FILE' with '$BASE_FILE'"

# run the diff command
diff --unchanged-group-format='@@ %dn,%df %<
' --old-group-format='' --new-group-format='' \
  --changed-group-format='' $BASE_FILE $COMPARE_FILE | grep -e "*" -v | grep -v '@' | grep -e '^$' -v | indent
