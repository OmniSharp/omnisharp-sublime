pushd omnisharp-server
msbuild /p:Platform="Any CPU" /property:nowarn=1685
popd

pushd omnisharp-roslyn
build.cmd
<<<<<<< HEAD
pops
=======
popd
>>>>>>> 4c3023feb3f1e9425820f8ba0f6080c275f39c76
