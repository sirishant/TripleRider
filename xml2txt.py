import os
import xml.etree.ElementTree as ET

def convert_coordinates(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_path, classes):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    labels = []
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xml_box = obj.find('bndbox')
        b = (float(xml_box.find('xmin').text), float(xml_box.find('ymin').text),
             float(xml_box.find('xmax').text), float(xml_box.find('ymax').text))
        bb = convert_coordinates((width, height), b)
        labels.append((cls_id,) + bb)
    return labels

def create_yolo_labels(xml_folder, yolo_folder, classes):
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
    for xml_file in xml_files:
        xml_path = os.path.join(xml_folder, xml_file)
        yolo_file = os.path.splitext(xml_file)[0] + '.txt'
        yolo_path = os.path.join(yolo_folder, yolo_file)
        labels = convert_annotation(xml_path, classes)
        with open(yolo_path, 'w') as f:
            for label in labels:
                f.write(' '.join(str(x) for x in label) + '\n')


create_yolo_labels('/home/sirishant/Desktop/yolov8t3/data/xmls', '/home/sirishant/Desktop/yolov8t3/data/labels', ['single', 'double', 'triple', 'head1', 'head2', 'head3', 'numplate'])
