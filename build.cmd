pushd omnisharp-roslyn
dotnet restore
msbuild /p:Configuration=Release
popd
