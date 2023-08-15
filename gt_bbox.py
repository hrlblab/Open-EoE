from mmdet.apis import init_detector, inference_detector
from mmdet.utils import register_all_modules
from mmdet.registry import VISUALIZERS
import mmcv
import os
import numpy as np
from pathlib import Path
import json
import cv2
import gc
import torch
import sys


def convert_to_numpy(item):
    if isinstance(item, torch.Tensor):
        return item.item()  # Extract the tensor value as a Python float
    elif isinstance(item, list):
        return [convert_to_numpy(subitem) for subitem in item]
    else:
        return item


def get_bbox(folder_path, config_file, checkpoint_file,model_name):
    register_all_modules()
    model = init_detector(config_file, checkpoint_file)

    for sub_folders in os.listdir(folder_path):
        sub_folders_path = os.path.join(folder_path,sub_folders)
        bboxes_info = []
        geo_info = []
        for file in os.listdir(sub_folders_path):
            # get coordinates from file name
            img_path = os.path.join(sub_folders_path, file)
            image = cv2.imread(img_path)
            arr = np.array(image)
            pixels = np.sum(arr)
            if pixels <= 178000000:
                print(file)
                coord = file.split('.')[0]
                x = int(coord.split('_')[0])
                y = int(coord.split('_')[1])
                # get predicted bboxes
                img = mmcv.imread(img_path, channel_order='rgb')
                result = inference_detector(model, img)
                initial_bboxes = result.pred_instances['bboxes'] #.numpy().tolist()
                initial_scores = result.pred_instances['scores'] #.numpy().tolist()
                initial_labels = result.pred_instances['labels']  #.numpy().tolist()
                # update bboxes coordinates
                bboxes = [[sublist[0]+x, sublist[1]+y, sublist[2]+x, sublist[3]+y, score] for sublist, label, score in zip(initial_bboxes, initial_labels, initial_scores) if label == 0 and score >= 0.3]
                bboxes_info.append(bboxes)

        bboxes_info = [sublist for sublist in bboxes_info if sublist]
        bboxes_info = convert_to_numpy(bboxes_info)

        for patches_bbox in bboxes_info:
            for coords in patches_bbox:
                polys =  [[[coords[0], coords[1]], [coords[0], coords[3]], [coords[2], coords[3]], [coords[2], coords[1]], [coords[0], coords[1]]]]
                geo_info.append(polys)
        
        geojson_data = {
        "type": "Feature",
        "id": "{}".format(sub_folders),
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": geo_info 
        },
        "properties": {"objectType": "annotation"}
        }

        if not os.path.exists(model_name):
            os.makedirs(model_name)        
        with open('{}/{}-{}.json'.format(model_name,sub_folders,model_name), 'w') as outfile:
            json.dump(bboxes_info,outfile)
        with open('{}/{}-{}.geojson'.format(sub_folders,model_name), "w") as f:
            json.dump(geojson_data, f)

if __name__ == '__main__':
    folder_path = sys.argv[0]

    config_file1 = 'mmdetection/configs/eoe/faster-rcnn_r50_fpn_1x.py'
    checkpoint_file1 = 'mmdetection/work_dirs/faster-rcnn_r50_fpn_1x/epoch_20.pth'
    faster = config_file1.split('/')[-1].split('-')[0]

    config_file2 = 'mmdetection/configs/eoe/mask-rcnn_r50_fpn_1x.py'
    checkpoint_file2 = 'mmdetection/work_dirs/mask-rcnn_r50_fpn_1x/epoch_20.pth'
    mask = config_file2.split('/')[-1].split('-')[0]

    config_file3 = 'mmdetection/configs/eoe/centernet_r50_fpn_1x.py'
    checkpoint_file3 = 'mmdetection/work_dirs/centernet_r50_fpn_1x/epoch_20.pth'
    center = config_file3.split('/')[-1].split('_')[0]

    get_bbox(folder_path, config_file1, checkpoint_file1, faster)
    get_bbox(folder_path, config_file2, checkpoint_file2, mask)
    get_bbox(folder_path, config_file3, checkpoint_file3, center)

