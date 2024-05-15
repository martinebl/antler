#from https://stackoverflow.com/questions/39431287/how-do-i-dynamically-create-instances-of-all-classes-in-a-directory-with-python
import os
import importlib
from pathlib import Path

basedir = Path(__file__).parents[0]

def instantiate_all_classes_from_folder(folder: str, excluded: list[str]) -> list[object]:

    # Step 1: Identify the files in the folder
    files = [f for f in os.listdir(basedir / folder) if f.endswith(".py") and f not in (excluded)]
    objects = instantiate_classes_from_folder(folder, files)

    return objects

def get_classes_from_folder(folder: str, included: list[str]):
    objects = []

    # Step 1: Identify the files in the folder
    files = [f for f in os.listdir(basedir / folder) if f.endswith(".py") and f in (included)]

    for file in files:
        # Step 2: Import modules dynamically
        module_name = file[:-3]  # remove '.py' extension
        relative_module_path = f"antler.{folder}.{module_name}"

        try:
            module = importlib.import_module(relative_module_path)
        except ImportError as e:
            print(f"Error importing module {relative_module_path}: {e}")
            continue
        
        #Only instantiate the class where names matches module. Other classes are classes used by the module.
        try:
            class_obj_name = next((cls for cls in dir(module) if cls.lower() == module_name.lower()), None)
            class_obj = getattr(module, class_obj_name)
            objects.append(class_obj)
        except Exception as e:
            print(f"Error finding class of name {class_obj_name if class_obj_name else module_name }: {e}")
            continue

    return objects

def instantiate_classes_from_folder(folder, included: list[str]):
    return [ class_obj() for class_obj in get_classes_from_folder(folder, included)]