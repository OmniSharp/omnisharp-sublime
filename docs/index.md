# OmniSharpSublime for ST3
 OmnisharpSublime is a plugin for ST3 to provide a C# development environment. It communicates with omnisharp-roslyn by nosami for IDE functions.

 It works on: 
   1. Mac OSX
   2. Linux
   3. Windows
 
 
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
 20. Reload Solution

# Linux Requirements
 * mono
 * msbuild-stable 
 
# Windows Requirements
 * Microsoft Build Tools 2015 (*must* be added to PATH)

# Build Requirements
 * dotnet core sdk

# Installation

 * Using [Package Control](https://packagecontrol.io), install the package called `OmniSharp`

# Building From Source
1. Move to ST3 plugin directory in console.

        cd {path to ST3 plugin directory}/Packages

2. Clone repository.

        git clone https://github.com/OmniSharp/omnisharp-sublime.git OmniSharp

3. Move to plugin directory, update submodule and build.


      * Windows
      
       cd OmniSharp
       git submodule update --init --recursive
       build.cmd
 
      * Linux Or Mac OSX
      
       cd OmniSharp
       git submodule update --init --recursive
       ./build.sh

# Project Setting
The server will automatically find the the solution file from the folder you have opened in Sublime.  If you have multiple solutions you have to specify the solution file you wish to use in a `sublime-project`. 

1. Go to `File -> Open` and select the folder with your solution in it.

2. Go to `Project -> Save Project As` and save a `YOURPROJECTNAME.sublime-project` in the same location as your `*.sln`

3. Open your `YOURPROJECTNAME.sublime-project` file that should now appear in the sidebar on the left

4. Enter the location to the `*.sln` file like below

## Example of a sublime-project

```
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
```

Once the `YOURPROJECT.sublime-project` is set up and saved, follow the below:

1. Close Sublime (YMMV but this seems to be the best way to open the `YOURPROJECTNAME.sublime-project`)
2. Open Sublime
3. Click `Project -> Open Project`, and select your `YOURPROJECT.sublime-project` file


# C# language-specific settings
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


