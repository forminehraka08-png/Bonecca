import importlib
import os

class PluginManager:
    def __init__(self, plugins_folder, storage):
        self.plugins_folder = plugins_folder
        self.storage = storage
        self.plugins = []
        self.help_addons = []
        self.enabled_plugins = {}

    def load_plugins(self):
        self.plugins = []
        self.help_addons = []
        files = [
            f for f in os.listdir(self.plugins_folder)
            if f.endswith(".py") and f != "__init__.py"
        ]
        for filename in files:
            modulename = filename[:-3]
            try:
                module_path = f'plugins.{modulename}'
                module = importlib.import_module(module_path)
                plugin = module.Plugin(self.storage)
                self.plugins.append(plugin)
                self.enabled_plugins[modulename] = True
                if hasattr(plugin, 'help_text'):
                    self.help_addons.append(plugin.help_text)
            except Exception as e:
                print(f"Plugin {modulename} failed to load: {e}")
                self.enabled_plugins[modulename] = False

    def get_help_addons(self):
        return self.help_addons

    def get_plugins_list(self):
        return [
            f"{plugin.__class__.__name__} ({'Включен' if self.enabled_plugins.get(plugin.__class__.__name__, True) else 'Отключен'})"
            for plugin in self.plugins
        ]