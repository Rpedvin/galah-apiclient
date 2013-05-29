#!/usr/bin/env bash

# Copyright (c) 2013 Galah Group LLC
# Copyright (c) 2013 Other contributers as noted in the CONTRIBUTERS file
#
# This file is part of galah-apiclient.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# From here on every command will be printed out before it is executed
set -x

# From here on if any command fails the script will abort
set -e

cd $DIR

# Create a temporary build directory to construct the apiclient binary.
TEMP_DIR=`mktemp -d`
cp -r ./apiclient $TEMP_DIR/
cp -r ./galah $TEMP_DIR/__main__.py

# Download dependencies and install into TEMP_DIR
REQUESTS_DIR=`mktemp -d`
cd $REQUESTS_DIR

# This will download the requests library but not install it.
pip install -d . requests

# Untar the library then delete the archive, making sure the resulting module
# is named requests.
tar xzf requests-*.tar.gz
rm requests-*.tar.gz
mv requests-*/requests requests

mv requests $TEMP_DIR/
cd $TEMP_DIR
rm -rf $REQUESTS_DIR
echo "Downloaded and untarred requests package"

YAML_DIR=`mktemp -d`
cd $YAML_DIR

# This will download the requests library but not install it.
pip install -d . pyyaml

# Untar the library then delete the archive, making sure the resulting module
# is named requests.
unzip PyYAML-*.zip
rm PyYAML-*.zip
mv PyYAML-*/lib/yaml yaml

mv yaml $TEMP_DIR/
cd $TEMP_DIR
rm -rf $YAML_DIR
echo "Downloaded and unzipped PyYAML package"

# Create the final zip archive
cd $TEMP_DIR
zip -r $DIR/galah-apiclient.zip *
echo "Created zip galah-apiclient.zip in $DIR"

# Turn zip archive into packaged executable
cd $DIR
echo '#!'`which python` | cat - galah-apiclient.zip > galah-client
chmod +x galah-client
rm galah-apiclient.zip

# Clean up anything left over
rm -rf $TEMP_DIR

# Unset the trap so we don't freak the user out by telling them an error has
# occured when everything went fine.
trap - EXIT

