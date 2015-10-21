import sublime
import sublime_plugin
from pprint import pformat


s = sublime.load_settings("PPrint.sublime-settings")


class PprintCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.erase_regions('json_errors')
        for region in self.view.sel():
            # If no selection, use the entire file as the selection
            if region.empty() and s.get("use_entire_file_if_no_selection", True):
                selection = sublime.Region(0, self.view.size())
            else:
                selection = region
            try:
                text = self.view.substr(selection)
                print(text)
                obj = eval(text)
                self.view.replace(edit, selection, pformat(obj))
            except Exception as exception:
                self.show_exception(exception)

    def show_exception(self, exception):
        sublime.status_message(str(exception))


def plugin_loaded():
    global s
    s = sublime.load_settings("PPrint.sublime-settings")
