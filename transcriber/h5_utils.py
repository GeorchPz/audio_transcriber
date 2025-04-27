from transcriber import os, h5py, get_dir_files

def get_h5_files(directory):
    '''Return a list of H5 files in a directory'''
    return get_dir_files(directory, extension='h5')

def print_h5_info(h5_file_path):
    with h5py.File(h5_file_path, 'r') as f:
        print(f"\nTop-level groups in {os.path.basename(h5_file_path)}:")
        transcriptions_names = list(f.keys())
        print(transcriptions_names)

if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    h5_files = get_h5_files(this_dir)
    
    print('H5 files in the directory:')
    print(h5_files)
    
    if h5_files:
        h5_file = h5_files[0]
        h5_path = os.path.join(this_dir, h5_file)
        print_h5_info(h5_path)
    else:
        print("No H5 files found in the directory.")