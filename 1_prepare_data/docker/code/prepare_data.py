# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import json
import argparse
from utils.tf_record_util import TfRecordGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="")
    parser.add_argument("--label_map", type=str, default="")
    parser.add_argument("--ground_truth_manifest", type=str, default="")
    parser.add_argument("--output", type=str, default="")
    args, _ = parser.parse_known_args()

    input_folder = args.input
    ground_truth_manifest = args.ground_truth_manifest
    label_map = json.loads(args.label_map)
    output_folder = args.output

    # Feed in necessary path variables from above operations
    tf_record_generator = TfRecordGenerator(image_dir=input_folder,
                                            manifest=ground_truth_manifest,
                                            label_map=label_map,
                                            output_dir=output_folder)

    print('GENERATING TF RECORD FILES')
    tf_record_generator.generate_tf_records()

    print('GENERATING LABEL MAP FILE')
    with open(f'{output_folder}/label_map.pbtxt', 'w') as label_map_file:
        for item in label_map:
            label_map_file.write('item {\n')
            label_map_file.write(' id: ' + str(int(item) + 1) + '\n')
            label_map_file.write(" name: '" + label_map[item] + "'\n")
            label_map_file.write('}\n\n')

    print('FINISHED')
