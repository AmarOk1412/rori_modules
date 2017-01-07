from rori import *
import os.path

def load_module(path):
    if "https://" in path:
        print("Not implemented yet.")
    else:
        path = path.replace("/", ".")
        if path[len(path)-1] is ".":
            path = path[:-1]
        exec("import %s.module as module" % path, globals())

def exec_module(path, rori_data_str):
    if "https://" in path:
        print("Not implemented yet.")
        return False
    else:
        module_path = path
        load_module(module_path)
        if path[-1] == "/":
            path = path[:-1]
        path = "rori_modules/" + path + "/sentences"
        sentences = "{}"
        if os.path.isfile(path):
            with open(path, 'r') as f:
                sentences = f.read()
        m = module.Module(sentences)
        m.process(create_data_from_json(rori_data_str))
        return m.continue_processing()
