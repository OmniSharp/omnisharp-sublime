pushd omnisharp-server
msbuild /p:Platform="Any CPU" /property:nowarn=1685
popd

pushd omnisharp-roslyn
build.cmd
popd
