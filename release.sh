#!/bin/bash

set -e

git_status="$(git status --porcelain)"
if [ -n "$git_status" ]
then
  echo "WARNING: detected uncommitted changes:"
  echo ""
  echo "$git_status"
  echo ""
  echo "Are you sure you want to continue?"
  read
fi

v="$(cat VERSION)"

echo ""
echo "Current version: $v"

# assume it's a minor version bump
maj=$(cut -f 1 -d '.' <<< "$v")
min=$(cut -f 2 -d '.' <<< "$v")
patch=0

v=$maj.$((min+1)).$patch
echo "New version: $v"

echo $v > VERSION

echo ""
echo "Tagging git"
echo ""

git add VERSION
git commit -m "version $v"
git tag -a "$v" -m "version $v"

git push
git push --tags
