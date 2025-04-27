from transcriber import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(PROJECT_DIR, 'audio_files')

def get_file_path(filename, extension=None, directory=None):
    '''Construct a full file path from a filename'''

    if extension not in [None, '']:
        filename += f'.{extension}'

    if directory in [None, '']:
        directory = PROJECT_DIR
    elif directory == 'project':
        directory = PROJECT_DIR
    elif directory == 'audio':
        directory = AUDIO_DIR
    
    return os.path.join(directory, filename)

def get_dir_files(directory=None, extension=None, non_processed=False):
    '''Return a list of files in a directory'''

    if directory in [None, '']:
        directory = PROJECT_DIR
    elif directory == 'project':
        directory = PROJECT_DIR
    elif directory == 'audio':
        directory = AUDIO_DIR
    
    in_dir = os.listdir(directory)
    if extension not in [None, '']:
        files = [f for f in in_dir if f.endswith(f'.{extension}')]
    else:
        is_file = lambda f: os.path.isfile(os.path.join(directory, f))
        files = [f for f in in_dir if is_file(f)]
    
    if non_processed:
        is_not_processed = lambda f: not os.path.isfile(get_file_path(f, 'txt'))
        files = [f for f in files if is_not_processed(f)]

    return files