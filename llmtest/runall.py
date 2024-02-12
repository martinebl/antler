#from https://stackoverflow.com/questions/39431287/how-do-i-dynamically-create-instances-of-all-classes-in-a-directory-with-python
import os
import importlib

def instantiate_classes_from_folder(folder_path):
    objects = []

    # Step 1: Identify the files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".py") and f not in ('__init__.py', 'probe.py')]

    for file in files:
        # Step 2: Import modules dynamically
        module_name = file[:-3]  # remove '.py' extension
        relative_module_path = f"llmtest.probes.{module_name}"

        try:
            module = importlib.import_module(relative_module_path)
        except ImportError as e:
            print(f"Error importing module {relative_module_path}: {e}")
            continue

        #only instantiate the first class - since the rest are class dependencies
        class_obj = getattr(module, dir(module)[0])
        objects.append(class_obj())

    return objects