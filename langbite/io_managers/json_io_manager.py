import langbite.io_managers.file_manager as FileManager

def load_factories():
    filename = FileManager.get_resource_path('factories.json')
    return FileManager.load_json_from_file(filename)
    # TODO: pending validation against JSON schema

def load_contexts():
    filename = FileManager.get_resource_path('contexts.json')
    return FileManager.load_json_from_file(filename)
    # TODO: pending validation against JSON schema

def load_augmentations(filename: str):
    return FileManager.load_json_from_file(filename)