#! /bin/bash
# make sure we're on the production branch
git checkout production
# pull the latest code from git
git pull
# Rebuild the container
docker build --no-cache -t aharnum/inlibraries .
# force-stop the current container
docker rm -f inlibraries
# run the new version
docker run -d --restart always --name inlibraries -p 5000:5000 aharnum/inlibraries