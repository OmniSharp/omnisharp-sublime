#!/bin/bash

pushd omnisharp-server
xbuild /p:Platform="Any CPU" /property:nowarn=1685
popd

pushd omnisharp-roslyn
./build.sh
popd