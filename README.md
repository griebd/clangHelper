# clangHelper #

> Maybe you should go for [EasyClangComplete](https://github.com/niosus/EasyClangComplete)!!!
I will try it later and report MY opnion, but it looks like what I was looking for when I
decided to make it by myself...

This [Sublime Text][] plugin adds syntactically- and semantically-valid
suggestions for **c**/**c++**/**objc**/**objc++** code completion. It uses
[libclang][] (part of [LLVM][]) and its [Python Bindings][] internally.

I started writing it because I couldn't find a working one, and when I went
looking why I discovered they would use clang command line binary and not the
library. That is not a problem in itself but it made me look away from them.

This plugin only support [Sublime Text][] 3! The reason is that [Sublime Text][]
2 won't import ctypes without user intervention in Linux and I do wan't a plugin
that works out of the box for everyone! (If there are too many requests for it,
I can change my mind :wink:)

**This plugin needs tests, please read the How To Help section below!**

## Install ##

For now, only using `git clone`. Later, when I fill it's good for general use,
I'll add it to [Package Control][]

##### Prerequisites #####

  - [LLVM][] 3.2 or greater
  - [Sublime Text][] 3

##### How-to #####

Just go to your Sublime Text package directory and
```sh
git clone https://github.com/griebd/clangHelper.git
```

To find your package directory open the console (View -> Show Console) in
[Sublime Text][] and type
```sh
sublime.packages_path()
```

## Usage ##

The plugin works "out of the box"! Just instal it, open any
**c**/**c++**/**objc**/**objc++** and check it out. Any time you type one of
these four characteres, **.**, **>**, **:** or '&nbsp;' (space) the plugin will
run the code completion and you should see valid options for your code.

If you miss some sugestions from libs you are using this happens because clang,
as a compiler, needs to know where the include files for those libs are.
Basically it needs all the "-I" directories you pass to your compiler when
compiling this file.

This plugin offers 3 options to set those directories:

1. Plugin level include:

  Will be included to all files you edit.

  Edit the plugin user settings file:  
    Preferences -> Package Settings -> clangHelper -> Settings - User  
  There are explanations on the plugin settings file:  
    Preferences -> Package Settings -> clangHelper -> Settings - Default

2. Project level include:

  Will be included to all files in the project.

  Edit your project file, you must include something like:
  ```json
  {
    "clangHelper":
    {
      "include":
      [
        "/usr/lib64/qt/mkspecs/linux-g++",
        "/usr/lib64/qt/include/QtCore",
        "/usr/lib64/qt/include/QtGui",
        "/usr/lib64/qt/include/QtSql",
        "/usr/lib64/qt/include"
      ]
    },
    "folders":
    [
      {
        "path": "."
      }
    ]
  }
  ```
  This is the .sublime-project file of a small Qt project of mine.

3. View level include:

  Will be included only on the file you are editing. This config will be lost
  when the view is closed!

  Right click the view and select 'clangHelper' -> 'Add a include directory to
  this view' and type the include directory you want. To include more than one,
  repeat the procedure.

Please not that the more library directories you add the more [libclang][] will
take to proccess your code completions! The good thing is that your editor won't
be blocked at any time, no matter how long [libclang][] takes.

To disable the plugin in any view right click the view and select 'clangHelper'
-> 'Clear all settings on this view'. To re-enable the plugin you will need to
reopen the view or Sublime Text itself.

## How To Help ##

I wrote this plugin on my developing environment, [Slackware][] 14.1, [LLVM][]
3.3 and [Sublime Text][] 3. [LLVM][] cames without the [Python Bindings][] in
[Slackware][] so I added it in the plugin.

It's working quite well for me already.

BUT, I need someone to do any of the following tests to make it more stable:

- [ ] check if the script will work on a system where [LLVM] has the
  [Python Bindings] alread instaled (any version)
- [ ] check if the script works with the other [LLVM] versions, 3.2 to 3.8
- [ ] check if the script works on Windows
- [ ] check if the script works on OS X
- [ ] check if the script works on Linux 32 bit

If you start using it, please report your success or failure through the
[issues][] in [GitHub][]. Please include your system and versions used.

Do ask for wanted features through the [issues][] in [GitHub][]!

And no need to say but: DO report any [issues/bugs][issues] you find!

## Contributors ##

So far, only myself. But I hope that changes quickly.

## Credits ##

- [Sublime Text][] for the great text editor! Simple, fast, small, not hungre on
  resources and with plenty of features!
- [LLVM][] Without them, this plugin wouldn't be possible!

## License ##

The MIT License (MIT)

Copyright &copy; 2016 Adriano Grieb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[libclang]: http://clang.llvm.org/ "a C language family frontend for LLVM"
[LLVM]: http://llvm.org/ "The LLVM Compiler Infrastructure"
[Python Bindings]: https://github.com/llvm-mirror/clang/tree/master/bindings/python "Clang Python Bindings"
[Sublime Text]: http://www.sublimetext.com/ "Sublime Text"
[Package Control]: https://packagecontrol.io/ "The Sublime Text package manager"
[Slackware]: http://www.slackware.com/ "The Slackware Linux Project"
[GitHub]: https://github.com/ "GitHub"
[issues]: https://github.com/griebd/clangHelper/issues "Issues"
