#!/bin/bash

#creates a zip file for the www directory in the _releases folder, named after the folder
# uses rsync to exclude files and folders in rsync-exclusions
# if a .env file is found, it will try to read the value of API_SERVER_VERSION into VERSION
#usage example: create_www_release_zip.sh <version>


#get the version from the command line
VERSION=$1

if [ -z "$VERSION" ]; then
  echo "No version specified"
  echo "Usage: create_www_release_zip.sh <version>"
  exit 1
fi

#validate that the version is in the correct format
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must be in the format x.x.x"
  echo "Example: 1.0.0"
  echo "Version provided: $VERSION"
  exit 1
fi

echo "Creating www release zip $VERSION in $(pwd)/.releases/$VERSION"

ROOT=$(pwd)
#the releases folder will be "releases/" plus the version
RELEASES="$ROOT/releases/$VERSION"
if [ ! -d "$RELEASES" ]; then
  mkdir -p "$RELEASES"
fi

#create a temp folder to rsync the files to
TEMP=$(mktemp -d)


echo "Rsyncing files to $TEMP"
echo "source: $ROOT/../www/src/"

#rsync the current directory to the releases folder
rsync -av --delete --exclude-from=rsync-exclusions "$ROOT/../www/src/" "$TEMP"

#change to the temp folder to avoid including the temp folder in the zip file
cd "$TEMP" || exit 1

#zip the temp folder and move it to the releases folder
zip -r -m "$RELEASES/intellireading-www-$VERSION.zip" ./

#change back to the root folder
cd "$ROOT" || exit 1

#remove the temp folder
rm -rf "$TEMP"

echo "Created release:"
#list the files in the releases folder
ls -l "$RELEASES"
