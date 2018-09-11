#!/usr/bin/env bash
set -e

cd omnisharp-roslyn
dotnet restore
msbuild /p:Configuration=Release

