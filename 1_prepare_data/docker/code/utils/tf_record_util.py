# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import os
import io
import json
import jsonlines
import random
import logging
from utils import dataset_util
from PIL import Image
import tensorflow as tf


class TfRecordGenerator:
    def __init__(self, image_dir, manifest, label_map, output_dir):
        self.image_dir = image_dir
        self.manifest = manifest
        self.label_map = label_map
        self.output_dir = output_dir

    def generate_tf_records(self):
        with jsonlines.open(self.manifest, 'r') as reader:
            ground_truth_annotations = list(reader)
            dataset = split_dataset(ground_truth_annotations)
            for subset in dataset:
                logging.info(f'GENERATING TF RECORD FOR {subset}')
                writer = tf.io.TFRecordWriter(os.path.join(self.output_dir, f'{subset}.records'))
                for image_annotations in dataset[subset]:
                    annotation_dict = json.loads(json.dumps(image_annotations))
                    tf_example = self._create_tf_example(annotation_dict['source-ref'],
                                                         annotation_dict['bees-500']['annotations'])
                    writer.write(tf_example.SerializeToString())
                writer.close()

    def _create_tf_example(self, s3_image_path, annotations):
        image_name = os.path.basename(s3_image_path)
        image_path = f'{self.image_dir}/{image_name}'
        im = Image.open(image_path)

        # READ IMAGE FILE
        with tf.io.gfile.GFile(image_path, 'rb') as fid:
            encoded_jpg = fid.read()

        encoded_jpg_io = io.BytesIO(encoded_jpg)
        encoded_jpg_io.seek(0)
        image = Image.open(encoded_jpg_io)
        image_width, image_height = image.size
        if image.format != 'JPEG':
            image = image.convert('RGB')

        xmins = []
        ymins = []
        xmaxs = []
        ymaxs = []
        classes = []
        classes_text = []
        for a in annotations:
            x = a['left']
            y = a['top']
            width = a['width']
            height = a['height']
            class_id = a['class_id']
            xmins.append(float(x) / image_width)
            xmaxs.append(float(x + width) / image_width)
            ymins.append(float(y) / image_height)
            ymaxs.append(float(y + height) / image_height)
            class_name = self.label_map[str(class_id)]
            classes_text.append(class_name.encode('utf8'))
            classes.append(class_id)

        feature_dict = {
            'image/height': dataset_util.int64_feature(image_height),
            'image/width': dataset_util.int64_feature(image_width),
            'image/filename': dataset_util.bytes_feature(bytes(image_name, 'utf-8')),
            'image/source_id': dataset_util.bytes_feature(bytes(image_name.replace('.jpg', ''), 'utf-8')),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
        }
        example = tf.train.Example(features=tf.train.Features(feature=feature_dict))
        return example


def split_dataset(list_images):
    dataset = {}
    random.seed(42)
    random.shuffle(list_images)
    num_train = int(0.9 * len(list_images))
    dataset['train'] = list_images[:num_train]
    dataset['validation'] = list_images[num_train:]
    logging.info(f'TRAINING EXAMPLES: %d - VALIDATION EXAMPLES: %d', len(dataset['train']), len(dataset['validation']))
    return dataset

