#!/usr/bin/env bash
set -e

[ ! "$1" ] && exit 1

cd prebuilt-omnisharp-roslyn

cp in/* .

for file in omnisharp omnisharp.cmd
do
    sed -i "s|@FILENAME@|$1|g" $file
done


