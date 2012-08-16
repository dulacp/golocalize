#!/usr/bin/env bash

# Usage:
#
# $ convert_utf16_to_utf8.sh subdirectory/*.strings

# Pattern to find files to convert
DEFAULT_PATTERN="MainStoryboard*.strings"
PATTERN=${1:-$DEFAULT_PATTERN}

# Fail fast and fail hard.
set -eo pipefail

# Syntax sugar (inspired from Heroku syntax)
indent() {
  RE="s/^/       /"
  [ $(uname) == "Darwin" ] && sed -l "$RE" || sed -u "$RE"
}

function puts-step (){
  echo "-----> $@"
}

function puts-warn (){
  echo " !"
  echo " !     $@"
  echo " !"
}

# Loop
find . -name $PATTERN -type f -print | while read f; do

  # converting the file
  puts-step "Convert file $f"
  set +e
  OUT=$(iconv -f UTF-16 -t UTF-8 "$f" > "$f.recode")
  if [ $? -ne 0 ]; then
    puts-warn "Error converting file $f"
    echo "$OUT" | indent
  else
    # override the original file
    mv "$f.recode" "$f"
  fi 
  set -e
done
