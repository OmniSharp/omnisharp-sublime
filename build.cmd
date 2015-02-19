@echo off

cd OmniSharpServer
xbuild /p:Platform="Any CPU" /property:nowarn=1685
