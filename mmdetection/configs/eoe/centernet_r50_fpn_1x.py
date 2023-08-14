# The new config inherits a base config to highlight the necessary modification
_base_ = '../centernet/centernet-update_r50-caffe_fpn_ms-1x_coco.py'

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    bbox_head=dict(num_classes=2))

# , mask_head=dict( type='FCNMaskHead',num_convs=0,in_channels=2048, conv_out_channels=256,num_classes=4,loss_mask=dict( type='CrossEntropyLoss', use_mask=True, loss_weight=1.0))


# Modify dataset related settings
data_root = 'C:/Users/x7754/OneDrive/Desktop/mmdet/eoe/'
# /hpc/group/tdunn/jx132/mmdet/eoe/

metainfo = {
    'classes': ('eos','papilla','rbc','cluster'),
    'palette': [
        (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)
    ]
}

train_dataloader = dict(
    batch_size=8,
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='New_EoE_train2022.json',
        data_prefix=dict(img='train/')))
val_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='New_EoE_val2022.json',
        data_prefix=dict(img='val/')))
test_dataloader = dict(
    dataset=dict(
        data_root=data_root,
        metainfo=metainfo,
        ann_file='New_EoE_test2022.json',
        data_prefix=dict(img='test/')))
# test_dataloader = train_dataloader

# Modify metric related settings

# 2 class
val_evaluator = dict(ann_file=data_root + 'New_EoE_val2022.json')
test_evaluator = dict(ann_file=data_root + 'New_EoE_test2022.json')


# 4 class
# val_evaluator = dict(ann_file=data_root + 'EoE_val2022.json')
# test_evaluator = dict(ann_file=data_root + 'EoE_test2022.json')


# We can use the pre-trained Mask RCNN model to obtain higher performance
# load_from = 'https://download.openmmlab.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'