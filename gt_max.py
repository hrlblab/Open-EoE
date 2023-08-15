import json
import os
import numpy as np
from scipy.spatial import cKDTree
import sys

# general version
def calculate_bbox_centers(bbox_list):
    centers = []
    for bboxes in bbox_list:
        for bbox in bboxes:
            bbox_x, bbox_y = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
            centers.append((bbox_x, bbox_y))
    return np.array(centers)


def calculate_bbox_in_slide_circle(image_width, image_height, radius, stride, bbox_list):
    max_bbox_count = 0
    centers = calculate_bbox_centers(bbox_list)
    tree = cKDTree(centers)

    for x in range(radius, image_width - radius + 1, stride):
        for y in range(radius, image_height - radius + 1, stride):
            bbox_count = len(tree.query_ball_point([x, y], radius))
            max_bbox_count = max(max_bbox_count, bbox_count)
    return max_bbox_count


def calculate_max(path, model_name):
    json_result = {}
    for file in os.listdir(path):
        print(file)
        imgs_path = os.path.join(path, file)
        imgs = os.listdir(imgs_path)
        sorted_imgs = sorted(imgs, key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1].split('.')[0])))
        img = sorted_imgs[-1]
        prefix, _ = img.split('.')
        image_width = int(prefix.split('_')[0]) + 512
        image_height = int(prefix.split('_')[1]) + 512
        

        json_data_path = os.path.join(model_name, '{}-{}.json'.format(file, model_name))

        try:
            with open(json_data_path, 'r') as data:
                bbox_list = json.load(data)
            max_bbox_in_slide_circle = calculate_bbox_in_slide_circle(image_width, image_height, radius, stride, bbox_list)
            json_result[file] = max_bbox_in_slide_circle
        except Exception as e:
            json_result[file] = 0
            print(f"Error processing {file}: {e}")

    with open('max_bbox_{}.json'.format(model_name), 'w') as outfile:
        json.dump(json_result, outfile)


if __name__ == "__main__": 
    path = sys.argv[0]
    model_name = sys.argv[1]
    radius = 1100
    stride = 10
    calculate_max(path, model_name)
