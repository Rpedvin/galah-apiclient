#!/usr/bin/env bash

# This will ensure that the script exits if a failure occurs
set -e

# This will ensure the user is visually prompted upon failure
trap "echo FAILURE: An error has occured! >&2" EXIT

STARTING_DIR=`pwd`

# Create a temporary build directory that we'll construct the contents of our
# tarbell within.
BUILD_DIR=`mktemp -d`/galah-apiclient
mkdir -p $BUILD_DIR
echo "Created build directory at $BUILD_DIR"

# Copy the actual api client to the directory
cp ./api_client.py $BUILD_DIR/
echo "Copied api_client.py into build directory."

# Build all of the man pages for the api commands
MAN_DIR=`mktemp -d`
sphinx-build -q -b man docs/ $MAN_DIR
cd $MAN_DIR
for f in `ls`
do
	gzip $f
done
mkdir -p $BUILD_DIR/man/man1/
mv *.gz $BUILD_DIR/man/man1/
cd $BUILD_DIR
rm -rf $MAN_DIR
echo "Built all of the man pages."

# Download the required requests package and move it into the build directory
REQUESTS_DIR=`mktemp -d`
cd $REQUESTS_DIR

# This will download the requests library but not install it.
pip install -d . requests

# Untar the library then delete the archive, making sure the resulting module
# is named requests.
tar xzf requests-*.tar.gz
rm requests-*.tar.gz
mv requests-* requests

mv requests $BUILD_DIR/
cd $BUILD_DIR
rm -rf $REQUESTS_DIR
echo "Downloaded and untarred requests package"

# Create the final tarbell
cd $BUILD_DIR/..
tar -zcf $STARTING_DIR/api_client.tar.gz galah-apiclient/
echo "Created tarbell api_client.tar.gz in $STARTING_DIR"

# Clean up anything left over
rm -rf $BUILD_DIR


# Unset the trap so we don't freak the user out by telling them an error has
# occured when everything went fine.
trap - EXIT
