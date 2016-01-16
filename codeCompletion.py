from sublime import (
    load_settings,
    message_dialog,
    Region,
    windows,
    CLASS_WORD_END,
    INHIBIT_WORD_COMPLETIONS
    )
from sublime_plugin import EventListener, TextCommand

from re import compile

# try system clang python bindings
try:
    from clang.cindex import TranslationUnit
# use customized clang python bindings
except:
    from clangHelper.tools.libclang_version import get_libclang_version
    if get_libclang_version() == '32':
        from clangHelper.clang.cindex32 import TranslationUnit
    if get_libclang_version() == '33':
        from clangHelper.clang.cindex33 import TranslationUnit
    if get_libclang_version() == '34':
        from clangHelper.clang.cindex34 import TranslationUnit
    if get_libclang_version() == '35':
        from clangHelper.clang.cindex35 import TranslationUnit
    if get_libclang_version() == '36':
        from clangHelper.clang.cindex36 import TranslationUnit
    elif get_libclang_version() == '37':
        from clangHelper.clang.cindex37 import TranslationUnit
    if get_libclang_version() == '38':
        from clangHelper.clang.cindex38 import TranslationUnit
    # else:
    #     raise 'couldn\'t load any clang python bindings, plugin is disabled!'

# Sublime Text won't reload changed modules when reloading the plugin
from sys import modules
from imp import reload
for mod in modules:
    if (('clangHelper.clang' in mod or 'clangHelper.tools' in mod) and
            modules[mod] != None):
        reload(modules[mod])

def plugin_loaded():
    # update all open views when plugin is loaded
    for window in windows():
        for view in window.views():
            set_view(view)

def set_view(view, force=False):
    settings = {}
    # ignore if settings already present in the view
    if view.settings().has('clangHelper'):
        if force:
            settings = view.settings().get('clangHelper')
            if view.id() in CodeCompletion.translation_units:
                del CodeCompletion.translation_units[view.id()]
        else:
            return
    settings['is_active'] = False

    # disable if syntax (scope_name) is not c, c++, objc nor objc++
    syntax = compile('(?<=source\.)[\w+#]+').search(
        view.scope_name(view.sel()[0].a))
    if syntax == None:
        view.settings().set('clangHelper', settings)
        return None
    syntax = syntax.group(0)
    if syntax == 'c':
        extension = '.c'
        std = '-std=c89'
    elif syntax == 'c++':
        extension = '.cpp'
        std = '-std=c++98'
    elif syntax == 'objc':
        extension = '.m'
        std = '-std=c89'
    elif syntax == 'objc++':
        extension = '.mm'
        std = '-std=c++98'
    else:
        view.settings().set('clangHelper', settings)
        return None
    settings['is_active'] = True

    # get current file name or buffer name (or make one)
    if view.file_name():
        settings['file_name'] = view.file_name()
    elif view.name():
        settings['file_name'] = view.name()
    else:
        settings['file_name'] = 'TMP_clangHelper' + extension

    # get includes defined in the settings
    def_inc = []
    for i in load_settings('clangHelper.sublime-settings').get('include'):
        def_inc.append('-I' + i)

    # get includes defined for the current project, if there is one
    proj_inc = []
    if view.window().project_file_name():
        data = view.window().project_data()
        if 'clangHelper' in data:
            if 'include' in data['clangHelper']:
                for i in data['clangHelper']['include']:
                    proj_inc.append('-I' + i)

    # get includes defined for the current view
    file_inc = []
    if 'include' in settings:
        for i in settings['include']:
            file_inc.append('-I' + i)

    # get file contents
    files = [(settings['file_name'], view.substr(Region(0, view.size())))]

    # create clang translation unit
    CodeCompletion.translation_units[view.id()] = TranslationUnit.from_source(
        settings['file_name'],
        [std] + def_inc + proj_inc,# + file_inc,
        unsaved_files=files,
        options=TranslationUnit.PARSE_PRECOMPILED_PREAMBLE |
            TranslationUnit.PARSE_CACHE_COMPLETION_RESULTS)

    # save settings for clangHelper in the view
    view.settings().set('clangHelper', settings)

    # set auto_complete_triggers on the view, if not set
    settings = view.settings().get('auto_complete_triggers', [])
    selector = 'source.' + syntax
    not_found = True
    for sel in settings:
        if sel['selector'] == selector:
            not_found = False
    if not_found:
        settings += [{'selector': selector, 'characters': '.>: '}]
    view.settings().set('auto_complete_triggers', settings)

class CodeCompletion(EventListener):
    translation_units = {}

    def on_load_async(self, view):
        set_view(view)

    def on_query_completions(self, view, prefix, locations):
        if view.settings().has('clangHelper'):
            settings = view.settings().get('clangHelper')
        else:
            return None
        if not settings['is_active']:
            return None

        # get file contents
        files = [(settings['file_name'], view.substr(Region(0, view.size())))]

        # where to complete
        if view.classify(view.sel()[0].a) == CLASS_WORD_END:
            (row, col) = view.rowcol(view.word(view.sel()[0]).a)
        else:
            (row, col) = view.rowcol(view.sel()[0].a)

        # execute clang code completion
        cr = self.translation_units[view.id()].codeComplete(
            settings['file_name'],
            row + 1,
            col + 1,
            unsaved_files=files)
        if cr is None or len(cr.results) == 0:
            return None

        # build code completions
        results = []
        for c in cr.results:
            # print (c.string)
            hint = ''
            contents = ''
            place_holders = 1
            for chunk in c.string:
                if chunk.isKindTypedText():
                    trigger = chunk.spelling
                hint += chunk.spelling
                if chunk.isKindResultType():
                    hint += ' '
                    continue
                if chunk.isKindPlaceHolder():
                    contents += ('${' + str(place_holders) + ':' +
                        chunk.spelling + '}')
                    place_holders += 1
                else:
                    contents += chunk.spelling
            results.append([trigger + "\t" + hint, contents])

        return (results, INHIBIT_WORD_COMPLETIONS)


class ClangHelperAddIncludeCommand(TextCommand):
    def run(self, edit):
        self.view.window().show_input_panel('Include directory:',
            '', self.done, None, None)

    def done(self, directory):
        settings = self.view.settings().get('clangHelper', {})
        if 'include' in settings:
            settings['include'] += [directory]
        else:
            settings['include'] = [directory]
        self.view.settings().set('clangHelper', settings)
        set_view(self.view, True)

class ClangHelperRemoveFromViewCommand(TextCommand):
    def run(self, edit):
        if self.view.settings().has('clangHelper'):
            self.view.settings().erase('clangHelper')
        if self.view.id() in CodeCompletion.translation_units:
            del CodeCompletion.translation_units[self.view.id()]
