# OmniSharpSublime for ST3
 OmnisharpSublime is a plugin for ST3 to provide C# development environment. It communicate with OmniSharpServer by nosami for IDE functions.

 It works on Mac OSX and Linux.

# Features
 1. Auto OmniSharpServer running
 2. Asynchronous communication with OmniSharpServer (Never freeze!)
 3. Auto Completion
 4. Goto definition
 5. Rename
 6. Goto implementation
 7. Syntax/Semantic error highlighting
 8. Displays possible override methods
 9. Find Usages
 10. Format Document
 11. Displays code issues such as `assigment is redundant`
 12. Fix code issues - put cursor on highlighted issue and select `Fix Code Issue`
 13. Remove Unused, Add Missing and Sort `Using` Statements
 14. Code Actions eg. `Convert LINQ query to Fluent Syntax`

# Requirements
 * Mono Development Kit(for [OmniSharpServer](https://github.com/nosami/OmniSharpServer))

# Installation
1. Move to ST3 plugin directory in console.

        cd {path to ST3 plugin directory}/Packages

2. Clone repository.

        git clone https://github.com/moonrabbit/OmniSharpSublime.git

3. Move to plugin directory, update submodule and build.

        cd OmniSharpSublime
        git submodule update --init --recursive
        ./build.sh

# Project Setting
To run server automatically, you have to specify a solution file in a sublime-project. For ASP.Net vNext applications you do not need to specify the solution file but you need the sublime-project file.

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


## C# language-specific settings
 Create C# settings file as shown in this picture
 
 ![Imgur](http://i.imgur.com/KjcPSFq.png)
 
 
 Paste the below in. This will launch intellisense on . and < symbols
 ```
 {
    "auto_complete": true,
    "auto_complete_selector": "source - comment",
    "auto_complete_triggers": [ {"selector": "source.cs", "characters": ".<"} ],
 }
 ```
#Format Document Settings

When you press `Ctrl + K + D` to format the document you may see `CR` markers.  

![CR Markers](http://i.imgur.com/SBgyjtk.png)

This is to do with the settings for `OmniSharpServer`.  Simply go to the OmniSharpServer/OmniSharp/bin/Debug sub directory then open config.json and modify the `eolMarker` setting to `\n` like below
```
  "TextEditorOptions": {
    "tabsToSpaces": true,
    "tabSize": 4,
    "indentSize": 4,
    "continuationIndent": 4,
    "labelIndent": 0,
    "eolMarker": "\n",
    "indentBlankLines": false,
    "wrapLineLength": 80
  },
```
# TODO
* class rename bug fix
* field rename bug fix

# Sometime
* Show Documentations
* Find type / symbols
* type lookup
* advanced syntax highlight
