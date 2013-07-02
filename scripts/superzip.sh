#!/usr/bin/env bash

# Get the directory the script is in.
DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Building superzip of the Galah API client from local repo."

set -x
superzippy -vvv -o galapi "PyYAML --global-option='--without-libyaml'" "$DIR/.." apiclient.main:main
