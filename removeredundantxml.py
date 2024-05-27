import os
import shutil

def move_xml_without_png(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Filter out only the XML files
    xml_files = [file for file in files if file.endswith('.xml')]
    
    # Iterate through XML files
    for xml_file in xml_files:
        # Get the corresponding PNG file name
        png_file = os.path.splitext(xml_file)[0] + '.png'
        
        # If the PNG file does not exist, move the XML file
        if png_file not in files:
            src_path = os.path.join(directory, xml_file)
            dest_path = os.path.join(os.path.dirname(directory), xml_file)
            
            # Check if the destination file already exists
            if os.path.exists(dest_path):
                # If the file already exists, rename the XML file
                base_name, extension = os.path.splitext(xml_file)
                counter = 1
                while os.path.exists(os.path.join(os.path.dirname(directory), f"{base_name}_{counter}{extension}")):
                    counter += 1
                dest_path = os.path.join(os.path.dirname(directory), f"{base_name}_{counter}{extension}")

            shutil.move(src_path, dest_path)
            print(f"Moved {xml_file} to parent directory as {os.path.basename(dest_path)}")

# Specify the directory containing the XML files
directory = '/home/sirishant/Desktop/AllData/images/all'

move_xml_without_png(directory)
