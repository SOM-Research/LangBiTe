from importlib.resources import files
import json

def get_resource_path(filename: str):
    return files('langbite.resources').joinpath(filename)

def load_json_from_file(filename: str):
    f = open(filename)
    return json.load(f)