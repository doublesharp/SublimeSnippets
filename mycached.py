import sublime, sublime_plugin, os, json

class MycachedCommand(sublime_plugin.TextCommand):
    values_file, key = 'User/mycached-values.json', None
    def run(self, edit, action, key=''):
        if action == "add":
            sublime.active_window().show_input_panel("Please enter your key:", key, self.on_add_key, None, None)
        else:
            key_values = self.get_key_values(True)
            menu_items = list(key_values.keys())
            def on_select(index):
                if index > -1:
                    if action == "copy" or action == "cast":
                        sublime.set_clipboard(key_values[menu_items[index]])
                    if action == "paste" or action == "cast": 
                        sublime.active_window().run_command('mycached_paste', {'value':key_values[menu_items[index]]})
                    if action == "edit": 
                        self.on_add_key(menu_items[index]);
            self.view.window().show_quick_panel(menu_items, on_select)
    def on_add_key(self, key):
        self.key, values, value = key.lower(), self.get_key_values(), ''
        if self.key in values: value = values[self.key]
        sublime.active_window().show_input_panel("Please {} the value for '{}':".format('enter' if not value else 'update', self.key), value, self.on_add_value, None, self.cancel_add_value)
    def cancel_add_value(self):
        sublime.active_window().run_command('mycached', {'action':'add', 'key':self.key})
    def on_add_value(self, value):
        values, values[self.key], src = self.get_key_values(), value, open(os.path.join(sublime.packages_path(), self.values_file), "w")
        write, close = src.write(json.dumps(values, sort_keys=True, indent=4)), src.close()
    def get_key_values(self, ui=False):
        try:
            src = open(os.path.join(sublime.packages_path(), self.values_file))
            data, close = json.load(src), src.close()
        except:
            data = { "No Results": "" } if ui else {}
        return data

class MycachedPasteCommand(sublime_plugin.TextCommand):
    def run(self, edit, value):
        view = sublime.active_window().active_view()
        view.insert(edit, view.sel()[0].begin(), value)