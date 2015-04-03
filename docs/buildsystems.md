#Build Systems
Sublime allows you to create your own build system.  OmniSharpSublime comes with the ability to run `xbuild/msbuild` out of the box but if you wish to create your own build system please follow the instructions below.

Click Tools -> Build System -> New Build System

Below is a similar build system to what comes out of the box with OmniSharpSublime. Use this as a model and save your file with the extension `sublime-build`

```
{
    "cmd": [
        "xbuild",
        "/property:GenerateFullPaths=true",
        "/nologo",
        "/v:q"
    ],
    "path": "/usr/bin/",
    "working_dir": "${project_path:${folder}}",
    "file_regex": "(?:^| |\"|'|\\(|\\[)((?:[A-Za-z]:)?[\\/][^\n \"':\\(\\)\\[\\]]+\\.\\w{0,4})(?=[\n \"':\\(\\)\\[\\]])\\((\\d+),\\d+\\)",
    "syntax": "Packages/OmniSharp/BuildConsole.hidden-tmLanguage",
    "variants": [
        {
            "name": "Clean",
            "cmd": [
                "xbuild",
                "/property:GenerateFullPaths=true",
                "/nologo",
                "/v:q",
                "/target:Clean"
            ],
            "path": "/usr/bin/",
            "working_dir": "${project_path:${folder}}"
        },
        {
            "name": "ReBuild",
            "cmd": [
                "xbuild",
                "/property:GenerateFullPaths=true",
                "/nologo",
                "/v:q",
                "/target:rebuild"
            ],
            "path": "/usr/bin/",
            "working_dir": "${project_path:${folder}}"
        }
    ]
}
```


Press CMD+B to build the solution and see the output in the console. Press F4 to open the file where there is an error. Shift+F4 to go backwards through the error list.

Using the Command Palette, type Build and you will see the options to build, clean and rebuild also!!

![Build](http://i.imgur.com/j4y5qCv.png)
