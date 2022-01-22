#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Updates DynamoDB with new items

import ast
import json
import boto3
import os
from dotenv import load_dotenv

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_NAME = os.path.basename(BASE_PATH)
ENV_FILE_PATH = os.path.join(os.path.dirname(BASE_PATH), '.env')
FILENAMES = os.path.join(BASE_PATH, 'filenames.json')
load_dotenv(dotenv_path=ENV_FILE_PATH)


def main():
    filenames = []
    resource = boto3.resource('dynamodb', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), region_name=os.getenv('AWS_REGION'))
    if os.path.exists(FILENAMES):
        with open(FILENAMES, 'r') as json_file:
            filenames = json.load(json_file)
            if type(filenames) is not list:
                filenames = ast.literal_eval(filenames)
    table = resource.Table(os.getenv('DYNAMODB_IMAGES_TABLE'))
    item = table.get_item(Key={'cam': BASE_NAME})['Item']
    item['images'] = filenames
    table.put_item(Item=item)


if __name__ == '__main__':
    main()
