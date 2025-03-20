import importlib
import importlib.util
import os
# import inspect

class Autoloader:
    def __init__(self):
        self.loaded_modules = {}
        # self.path=os.path.dirname(__file__)
        # sys.path.append(os.path.abspath(os.path.join(self.path, '..')))

    def __call__(self, class_name):
        m=self.module(class_name)
        cl=class_name.split('.')[-1]
        return getattr(m, cl) if hasattr(m, cl) else m

    def file(self, module_path):
        if module_path not in self.loaded_modules:
            if module_path[0] not in [os.sep[0],'/','\\']:
                module_path=os.path.realpath(os.path.join(os.path.dirname(__file__), module_path))
            self.loaded_modules[module_path]=module_path
            if os.path.isfile(module_path):
                spec = importlib.util.spec_from_file_location(module_path, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module) # type: ignore
                self.loaded_modules[module_path] = module
            else:
                self.loaded_modules[module_path] = None
                
        return self.loaded_modules[module_path]

    def module(self, module_name):
        if module_name not in self.loaded_modules:
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
        return self.loaded_modules[module_name]
    
    def __getattr__(self, name):
        try:
            module = self(name)
            return module
        except ModuleNotFoundError:
            raise AttributeError(f"Module '{name}' not found")

al = Autoloader()
