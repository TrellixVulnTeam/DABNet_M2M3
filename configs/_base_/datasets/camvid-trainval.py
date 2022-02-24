# dataset settings
dataset_type = 'CamVid'
data_root = 'data/CamVid/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
crop_size = (768, 960)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(type='Resize', img_scale=(1536, 768), ratio_range=(0.5, 2.0)),
    dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size=crop_size, pad_val=0, seg_pad_val=255),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(960, 768),
        # img_ratios=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=False),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]

CamVid_train = dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='images/train',
        ann_dir='TrainID/train',
        pipeline=train_pipeline),
CamVid_trainval = dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='images/val',
        ann_dir='TrainID/val',
        pipeline=train_pipeline)


data = dict(
    samples_per_gpu=8,
    workers_per_gpu=8,
    train=[CamVid_train, CamVid_trainval],
    val=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='images/test',
        ann_dir='TrainID/test',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        img_dir='images/test',
        ann_dir='TrainID/test',
        pipeline=test_pipeline))