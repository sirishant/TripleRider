import os

def modify_labels_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            print("Modifying labels in file:", file_path)
            modified_labels = modify_labels(file_path)
            output_file_path = os.path.join(directory, "modified_" + filename)
            write_labels_to_file(output_file_path, modified_labels)
            print("Modified labels saved to:", output_file_path)

def modify_labels(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    modified_labels = []

    for line in lines:
        class_idx, x_center, y_center, width, height = map(float, line.strip().split())
        
        # Modify the first digit according to the specifications
        if class_idx == 1 or class_idx == 2:
            class_idx = 0
        elif class_idx == 3:
            class_idx = 1
        elif class_idx == 4:
            class_idx = 2
        
        modified_labels.append([class_idx, x_center, y_center, width, height])

    return modified_labels

def write_labels_to_file(output_file_path, modified_labels):
    with open(output_file_path, 'w') as file:
        for label in modified_labels:
            file.write(' '.join(map(str, label)) + '\n')

# Example usage
directory = '/home/sirishant/Desktop/yolov8t3/data'
print("Modifying labels in directory:", directory)
modify_labels_in_directory(directory)
print("Label modification completed.")

# Example usage
# directory = '/home/sirishant/Desktop/yolov8t3/data'
# modify_labels_in_directory(directory)
