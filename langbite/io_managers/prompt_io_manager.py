import langbite.io_managers.file_manager as FileManager

def load_augmentation_prompt():
    return FileManager.load_file('augmentation_prompt.prm')