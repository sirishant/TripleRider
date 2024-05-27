import os

def remove_whitespace(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Iterate through files
    for file_name in files:
        # Check if the file name contains whitespace
        if ' ' in file_name:
            # Create the new file name by removing whitespace
            new_file_name = file_name.replace(' ', '')
            
            # Rename the file
            old_path = os.path.join(directory, file_name)
            new_path = os.path.join(directory, new_file_name)
            os.rename(old_path, new_path)
            
            print(f"Renamed {file_name} to {new_file_name}")

# Specify the directory containing the files
directory = '/home/sirishant/Desktop/yolov8t3/data/'

remove_whitespace(directory)
