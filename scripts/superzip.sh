#!/usr/bin/env bash

# This will ensure that the script exits if a failure occurs
set -e

# This will ensure the user is visually prompted upon failure
trap "echo FAILURE: An error has occured! >&2" EXIT

# Get the directory the script is in.
DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Building superzip of the Galah API client from local repo."

set -x
superzippy -vvv -o galapi "PyYAML --global-option='--without-libyaml'" "$DIR/.." apiclient.main:main

echo "Done."

# Unset the trap so we don't freak the user out by telling them an error has
# occured when everything went fine.
trap - EXIT
