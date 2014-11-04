#File Templates

OmniSharpSublime provides out of the box the ability to create a new C# class and a new C# interface from the side and context menu.  The plugin simply reads in a [template file](https://github.com/OmniSharp/omnisharp-sublime/tree/master/templates) and has the ability to replace placeholders which are currently `${namespace}` (the folder location) and `${classname}` (new file name). 

To add your own template simply add a template file to to the `templates` folder with the extension `.tmpl`.

In the `Context.sublime-menu` and/or `Side Bar.sublime-menu` file add your own menu item that looks something like:

    {
        "caption": "New File Of Some Sort",
        "id": "omnisharp-new-something",
        "command": "omni_sharp_new_file",
        "args":{"tmpltype":"name_of_template_file_without_extensions","paths": []}
    }