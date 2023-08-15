import json
import os
import numpy as np
import sys

def is_overlapping(bbox1, bbox2):
    return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])


def process_bboxes(bboxes):
    flattened_bboxes = [bbox for sublist in bboxes for bbox in sublist]
    bboxes_to_remove = []
    for i, bbox1 in enumerate(flattened_bboxes):
        has_overlap = False
        for j, bbox2 in enumerate(flattened_bboxes):
            if i != j and is_overlapping(bbox1, bbox2):
                has_overlap = True
                break
        if not has_overlap:
            bboxes_to_remove.append(bbox1)

    # Remove non-overlapping bboxes
    for bbox in bboxes_to_remove:
        flattened_bboxes.remove(bbox)

    return flattened_bboxes


def calculate_iou(box1, box2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou


def nms(bboxes, iou_threshold):
    """
    Perform Non-Maximum Suppression (NMS) on a list of bounding boxes.
    """
    bboxes = sorted(bboxes, key=lambda x: x[4], reverse=True)  # Sort by scores in descending order
    selected_bboxes = []

    while len(bboxes) > 0:
        best_bbox = bboxes[0]
        selected_bboxes.append(best_bbox)

        remaining_bboxes = []
        for bbox in bboxes[1:]:
            if calculate_iou(best_bbox, bbox) < iou_threshold:
                remaining_bboxes.append(bbox)

        bboxes = remaining_bboxes

    return selected_bboxes


def merge_data(filename):
    with open('centernet/{}-centernet.json'.format(filename)) as f1:
        data1 = json.load(f1)
    with open('faster/{}-faster.json'.format(filename)) as f2:
        data2 = json.load(f2)
    with open('mask/{}-mask.json'.format(filename)) as f3:
        data3 = json.load(f3)
    data = data1 + data2 + data3
    return data


if __name__ == "__main__":
    folder_path = sys.argv[0]
    iou_threshold = 0.6
    if not os.path.exists('ensemble'):
        os.makedirs('ensemble')

    for file in os.listdir(folder_path):
        data = merge_data(file)
        processed_bboxes = process_bboxes(data)
        nms_bbox = nms(processed_bboxes, iou_threshold)
        nms_bbox = [nms_bbox]
        with open('ensemble/{}-ensemble.json'.format(file), 'w') as file:
            json.dump(nms_bbox, file)