import os

def rename_modified_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.startswith("modified_") and filename.endswith(".txt"):
            original_file_path = os.path.join(directory, filename)
            new_filename = filename.replace("modified_", "")
            new_file_path = os.path.join(directory, new_filename)
            os.rename(original_file_path, new_file_path)
            print("Renamed:", original_file_path, "->", new_file_path)

# Example usage
directory = '/home/sirishant/Desktop/yolov8t3/data'
print("Renaming modified .txt files in directory:", directory)
rename_modified_txt_files(directory)
print("Renaming completed.")
