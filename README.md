# OmniSharpSublime for ST3
 OmnisharpSublime is a plugin for ST3 to provide C# development environment. It communicate with OmniSharpServer by nosami for IDE functions.

 It works on Mac OSX, Linux & Windows.

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
 15. Add File To Project
 16. Remove File from Project (via sidebar and context menu)
 17. Add New C# Class & Interface (via sidebar and context menu) via File Templates which also adds to `csproj`
 18. Type Lookup with Documentation 
 19. Hide/Show Info Panel

#Requirements
 * Mono Development Kit(for [OmniSharpServer](https://github.com/nosami/OmniSharpServer))

#Installation

 * Using the Sublime Package Manager install the package called `OmniSharp`

# Building From Source
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

Let's assume you already have a solution.

    Go to `File -> Open` and select the folder with your solution in it.
    
    Go to `Project -> Save Project As` and save your .sublime-project in the same location as your *.sln
    
    Open your .sublime-project file that should now appear in the sidebar on the left
    
    Enter the location to the *.sln file like below

## Example of sublime-project

    {
        "folders":
        [
            {
                "follow_symlinks": true,
                "path": "."
            }
        ],
        "solution_file": "./testconsoleprj.sln"
    }
    
 Once the `sublime-project` is set up and saved follow the below:
    
    Close Sublime (YMMV but this seems to be the best way to open the .sublime-project)
    
    Open Sublime
    
    Click `Project -> Open Project`, and select your .sublime-project file


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

This is to do with the settings for `OmniSharpServer`.  
   ```
   Click Preferences - Browse Packages
   Go to `OmniSharp/PrebuiltOmniSharpServer/` sub directory 
   Open config.json and modify the `eolMarker` setting to `\n` like below
   ```
   
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

#Build Solution

Create a new Build System

`Tools -> Build System -> New Build System`

Paste in the below and save the file as `xbuild.sublime-build`

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
    "file_regex": "^([\\d\\w:/\\.-]*)\\((\\d+),(\\d+)\\)\\s*(.*)$",
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
            "working_dir": "${project_path:${folder}}",
            "file_regex": "^([\\d\\w:/\\.-]*)\\((\\d+),(\\d+)\\)\\s*(.*)$"
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
            "working_dir": "${project_path:${folder}}",
            "file_regex": "^([\\d\\w:/\\.-]*)\\((\\d+),(\\d+)\\)\\s*(.*)$"
        }
    ]
}
```

Press `CMD+B` to build the solution and see the output in the console. Press `F4` to open the file where there is an error. `Shift+F4` to go backwards through the error list.

Using the Command Pallete, type Build and you will see the options to build, clean and rebuild also!!

**NOTE:** If you used Homebrew to install Mono the path in the build system needs to be `/usr/local/bin/`

![Build](http://i.imgur.com/j4y5qCv.png)


# TODO
* class rename bug fix
* field rename bug fix

# Sometime
* Show Documentations
* Find type / symbols
* advanced syntax highlight
