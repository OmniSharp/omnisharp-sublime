# OmniSharpSublime for ST3
 OmnisharpSublime is a plugin for ST3 to provide a C# development environment. It communicates with OmniSharpServer by nosami for IDE functions.

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
 20. Run Unit Tests
 21. Build/ReBuild/Clean Solution
 22. Reload Solution

#Requirements
 * Mono Development Kit(for [OmniSharpServer](https://github.com/nosami/OmniSharpServer))

#Installation

 * Using [Package Control](https://packagecontrol.io), install the package called `OmniSharp`

# Building From Source
1. Move to ST3 plugin directory in console.

        cd {path to ST3 plugin directory}/Packages

2. Clone repository.

        git clone https://github.com/OmniSharp/omnisharp-sublime.git OmniSharp

3. Move to plugin directory, update submodule and build.

        cd OmniSharp
        git submodule update --init --recursive
        ./build.sh

# Project Setting
The server will automatically find the the solution file from the folder you have opened in Sublime.  For ASP.Net vNext applications it will find the project.json file.  If you have multiple solutions you have to specify the solution file you wish to use in a sublime-project. 

1. Go to `File -> Open` and select the folder with your solution in it.

2. Go to `Project -> Save Project As` and save a `YOURPROJECTNAME.sublime-project` in the same location as your `*.sln`

3. Open your `YOURPROJECTNAME.sublime-project` file that should now appear in the sidebar on the left

4. Enter the location to the `*.sln` file like below

## Example of a sublime-project

```json
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

 ```json
 {
    "auto_complete": true,
    "auto_complete_selector": "source - comment",
    "auto_complete_triggers": [ {"selector": "source.cs", "characters": ".<"} ],
 }
 ```

#OmniSharpServer Settings
The Sublime plugin communicates to OmniSharp Server which has various available settings stored in a `config.json` file. By default the location of this file is in a folder under the Sublime OmniSharp packages folder called `PrebuiltOmniSharpServer` and there is also a user specific plugin setting that specifies the location of this `config.json` file.  To prevent your settings being overridden on new releases of the Sublime package, we recommend you store your `config.json` file somewhere other than the default location.  Once you have taken a copy of `config.json` and put it somewhere safe you will need to update the Sublime plugin's user setting called `"omnisharp_server_config_location"`. 

 
#Format Document Settings

When you press `Ctrl + K + D` to format the document you may see `CR` markers.  

![CR Markers](http://i.imgur.com/SBgyjtk.png)

This is to do with the settings for `OmniSharpServer`.  

1. Click Preferences - Browse Packages
2. Go to `OmniSharp/PrebuiltOmniSharpServer/` sub directory 
3. Open config.json and modify the `eolMarker` setting to `\n` like below

**OR**

Open your safely tucked away config.json file and modify the `eolMarker` setting to `\n` like below

```json
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

#Unit Tests

For the plugin to be able to run unit tests you need to configure the test runner. This is done in the server config file.

1. Click Preferences - Browse Packages
2. Go to `OmniSharp/PrebuiltOmniSharpServer/` sub directory 
3. Open config.json and modify the `TestCommands` like below

**OR**

Open your safely tucked away config.json file and modify the `TestCommands` like below

 ```json
 "TestCommands": {
    "All": "nunit-console.exe -nologo {{AssemblyPath}}",
    "Fixture": "nunit-console.exe -nologo {{AssemblyPath}} -run={{TypeName}}",
    "Single": "nunit-console.exe -nologo {{AssemblyPath}} -run={{TypeName}}.{{MethodName}}"
   },
```

# Sometime
* Find type / symbols
* advanced syntax highlight
