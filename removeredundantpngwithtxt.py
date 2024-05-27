import os
import shutil

def move_images_without_txt(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Filter out only the image files
    image_files = [file for file in files if file.endswith('.png')]
    
    # Iterate through image files
    for image_file in image_files:
        # Get the corresponding txt file name
        txt_file = os.path.splitext(image_file)[0] + '.txt'
        
        # If the txt file does not exist, move the image file
        if txt_file not in files:
            src_path = os.path.join(directory, image_file)
            dest_path = os.path.join(os.path.dirname(directory), image_file)
            
            # Check if the destination file already exists
            if os.path.exists(dest_path):
                # If the file already exists, rename the image file
                base_name, extension = os.path.splitext(image_file)
                counter = 1
                while os.path.exists(os.path.join(os.path.dirname(directory), f"{base_name}_{counter}{extension}")):
                    counter += 1
                dest_path = os.path.join(os.path.dirname(directory), f"{base_name}_{counter}{extension}")

            shutil.move(src_path, dest_path)
            print(f"Moved {image_file} to parent directory as {os.path.basename(dest_path)}")

# Specify the directory containing the images
directory = '/home/sirishant/Desktop/AllData/images/all'

move_images_without_txt(directory)

