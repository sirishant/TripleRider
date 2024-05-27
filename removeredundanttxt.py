import os
import shutil

def move_txt_without_png(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Filter out only the txt files
    txt_files = [file for file in files if file.endswith('.txt')]
    
    # Iterate through txt files
    for txt_file in txt_files:
        # Get the corresponding PNG file name
        png_file = os.path.splitext(txt_file)[0] + '.png'
        
        # If the PNG file does not exist, move the txt file
        if png_file not in files:
            src_path = os.path.join(directory, txt_file)
            dest_path = os.path.join(os.path.dirname(directory), txt_file)
            
            # Check if the destination file already exists
            if os.path.exists(dest_path):
                # If the file already exists, rename the txt file
                base_name, extension = os.path.splitext(txt_file)
                counter = 1
                while os.path.exists(os.path.join(os.path.dirname(directory), f"{base_name}_{counter}{extension}")):
                    counter += 1
                dest_path = os.path.join(os.path.dirname(directory), f"{base_name}_{counter}{extension}")

            shutil.move(src_path, dest_path)
            print(f"Moved {txt_file} to parent directory as {os.path.basename(dest_path)}")

# Specify the directory containing the txt files
directory = '/home/sirishant/Desktop/AllData/images/all'

move_txt_without_png(directory)
