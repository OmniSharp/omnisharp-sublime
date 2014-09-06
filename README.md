# OmniSharpSublime for ST3
 OmnisharpSublime is a plugin for ST3 to provide C# development environment. It communicate with OmniSharpServer by nosami for IDE functions.

 It works on Mac OSX and Linux.

# Features
 1. Auto OmniSharpServer running
 2. Asynchronous communication with OmniSharpServer (Never freeze!)
 3. Auto Completion
 4. Goto definition
 5. Rename

# Requirements
 * Mono Development Kit(for [OmniSharpServer](https://github.com/nosami/OmniSharpServer))

# Installation
1. Move to ST3 plugin directory in console.

        cd {path to ST3 plugin directory}/Packages

2. Clone repository and update submodule.

        git clone https://github.com/moonrabbit/OmniSharpSublime.git

3. Move to plugin directory

        cd OmniSharpSublime
        git submodule update --init
        ./build.sh

# Project Setting
To run server automatically, you have to specify solution file on sublime-project file.

## Example of sublime-project

        {
            "folders":
            [
                {
                    "name": "csharp_project",
                    "follow_symlinks": true,
                    "path": ".",
                    "file_exclude_patterns":
                    [
                        "*.meta",
                        "*.png",
                        "*.dll",
                        "*.mdb"
                    ],
                    "folder_exclude_patterns":
                    [
                        "Library"
                    ]
                }
            ],
            "settings":
            {
                "tab_size": 4
            },
            "solution_file": "./csharp-project.sln"
        }


# TODO
* find usage
* class rename bug fix
* field rename bug fix
* syntax error notification

# Sometime
* Show Documentations
* Find type / symbols
* code action
* code format
* type lookup
* advanced syntax highlight
