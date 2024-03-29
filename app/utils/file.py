import os

def get_filename(filename: str):
    filename_ = filename.split('/')[-1]
    
    return filename_

def extend_filename(filename: str, token: str, delimiter: str = '.'):
    extension = filename.split(delimiter)[-1]
    body = filename.split(delimiter)[:-1]
    
    new_filename = delimiter.join(body)+'_'+token+delimiter+extension

    return new_filename

def create_folder(directory_name: str):
    from os import path
    if not path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created!")
    else:
        print(f"Directory '{directory_name}' already exists.")