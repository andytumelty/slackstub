#!/bin/bash

set -e

docker_username='andytumelty'
docker_image='slackstub'

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
echo "Building and releasing image"
echo ""

docker build . -t $docker_username/$docker_image:latest
echo ""
docker tag $docker_username/$docker_image:latest andytumelty/slackstub:$v

echo ""
docker push $docker_username/$docker_image:latest
echo ""
docker push $docker_username/$docker_image:$v

echo ""
echo "Tagging git"
echo ""

git add VERSION
git commit -m "version $v"
git tag -a "$v" -m "version $v"

git push
git push --tags
