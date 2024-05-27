import os
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont

def load_detections(file_path: str, confidence_threshold: float = 0.5) -> List[Tuple[int, float, float, float, float]]:
    detections = []
    with open(file_path, 'r') as f:
        for line in f:
            values = line.strip().split()
            if len(values) == 5:  # Check if the line contains five values
                label_index = int(values[0])
                conf = float(values[1])
                if conf >= confidence_threshold:
                    x_center = float(values[2])
                    y_center = float(values[3])
                    width = float(values[4])
                    # height = float(values[5])  # Removed this line
                    x1 = x_center - width / 2
                    y1 = y_center - width / 2  # Corrected from height to width
                    x2 = x_center + width / 2
                    y2 = y_center + width / 2  # Corrected from height to width
                    detections.append((label_index, conf, x1, y1, x2, y2))  # Corrected the values
    return detections

def associate_heads(detections: List[Tuple[int, float, float, float, float, float]]) -> List[Tuple[int, int]]:
    rider_heads = []
    for detection in detections:
        label, conf, x1, y1, x2, y2 = detection
        if label == 0 or label == 1 or label == 2:  # single, double, or triple rider
            rider_box = (x1, y1, x2, y2)
            num_heads = 0
            for head in detections:
                head_label, head_conf, hx1, hy1, hx2, hy2 = head
                if head_label == 3:  # head
                    head_box = (hx1, hy1, hx2, hy2)
                    if is_associated(rider_box, head_box):
                        num_heads += 1
            rider_heads.append((label, num_heads))
            print("Rider:", label, "Num Heads:", num_heads)
    return rider_heads

def is_associated(rider_box: Tuple[float, float, float, float], head_box: Tuple[float, float, float, float]) -> bool:
    rx1, ry1, rx2, ry2 = rider_box
    hx1, hy1, hx2, hy2 = head_box
    rider_width = rx2 - rx1
    rider_height = ry2 - ry1
    head_width = hx2 - hx1
    head_height = hy2 - hy1
    max_head_dist = max(rider_width, rider_height) * 0.5  # Adjust this factor as needed
    center_x, center_y = (rx1 + rx2) / 2, (ry1 + ry2) / 2
    head_center_x, head_center_y = (hx1 + hx2) / 2, (hy1 + hy2) / 2
    distance = ((center_x - head_center_x) ** 2 + (center_y - head_center_y) ** 2) ** 0.5
    return distance < max_head_dist

def update_classifications(rider_heads: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    updated_classifications = []
    for rider_label, num_heads in rider_heads:
        if num_heads == 0:
            updated_label = 0  # single rider
        elif num_heads == 1:
            updated_label = 1  # double rider
        else:
            updated_label = 2  # triple rider
        updated_classifications.append((updated_label, num_heads))
    return updated_classifications

def draw_detections(image_path, detections, label_names):
    # Open image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Font for label text
    font = ImageFont.load_default()
    
    # Assuming detections is a list of tuples, where each tuple contains detection information
    for detection in detections:
        label_index = detection[0]
        label_name = label_names[label_index]
        print("Detected label:", label_name)
    
        # Other code for drawing bounding boxes or processing detections
        x_center, y_center, width, height = detection[1], detection[2], detection[3], detection[4]
        x1 = int((x_center - width / 2) * image.width)
        y1 = int((y_center - height / 2) * image.height)
        x2 = int((x_center + width / 2) * image.width)
        y2 = int((y_center + height / 2) * image.height)
    
        # Ensure x1 is less than or equal to x2
        x1, x2 = min(x1, x2), max(x1, x2)
        # Ensure y1 is less than or equal to y2
        y1, y2 = min(y1, y2), max(y1, y2)
    
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1), label_name, fill="red", font=font)


    # Save the annotated image in the specified output directory
    output_dir = "/home/sirishant/Desktop/yolov8t3/runs"  # Replace with your desired output directory
    output_filename = os.path.splitext(os.path.basename(image_path))[0] + "_output.png"
    output_path = os.path.join(output_dir, output_filename)
    image.save(output_path)

def process_detections(detections_dir: str, images_dir: str):
    label_names = ['single', 'double', 'triple', 'head', 'numplate']
    confidence_threshold = 0.5  # Adjust the confidence threshold as needed
    for file_name in os.listdir(detections_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(detections_dir, file_name)
            image_path = os.path.join(images_dir, os.path.splitext(file_name)[0] + '.png')
            detections = load_detections(file_path, confidence_threshold)
            print("Detections before processing:", detections)  # Debug output
            rider_heads = associate_heads(detections)
            print("Rider heads:", rider_heads)  # Debug output
            updated_classifications = update_classifications(rider_heads)
            updated_detections = []
            for classification, num_heads in updated_classifications:
                for detection in detections:
                    label, conf, x1, y1, x2, y2 = detection
                    if label == classification:
                        updated_detections.append((classification, conf, x1, y1, x2, y2))
            draw_detections(image_path, updated_detections, label_names)

if __name__ == "__main__":
    detections_dir = "/home/sirishant/Desktop/yolov8t3/runs/detect/predict5/labels/"
    images_dir = "/home/sirishant/Desktop/yolov8t3/test_images/"
    process_detections(detections_dir, images_dir)
