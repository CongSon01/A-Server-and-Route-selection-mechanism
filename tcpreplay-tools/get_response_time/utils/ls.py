import os

def ls_subfolders(rootdir):
    sub_folders_n_files = []
    for path, _, files in os.walk(rootdir):
        for name in files:
            sub_folders_n_files.append(os.path.join(path, name))
    return sorted(sub_folders_n_files)

def ls_file_in_current_folder(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def ls_folder_in_current_folder(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]