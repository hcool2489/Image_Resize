import json
import datetime
import os
from io import BytesIO

# Requirements: boto3 and Pillow(PIL)
import boto3
import PIL
from PIL import Image

def get_url(key, bucket, region):
	return "https://{bucket}.s3.{region}.amazonaws.com/{key}".format(key=key,bucket=bucket,region=region)

def resizeImage(bucket, key, size):
	dimensions = seze.split('x')
	s3 = boto3.resource('s3')
	obj = s3.Object(bucket_name = bucket,key = key)
	objBody = obj.get()['Body'].read()
	img = Image.open(BytesIO(objBody))
	img = img.resize((int(dimensions[0]),int(dimensions[1])), PIL.Image.ANTIALIAS)
	temp = BytesIO()
	img.save(temp, 'JPEG')
	temp.seek(0)
	
	newKey = "{size}_{key}".format(size=size, key=key)
	obj = s3.Object(bucket_name=bucket,key=newKey)
	obj.put(Body=temp, ContentType='image/jpeg')
	
	return get_url(newKey, bucket, os.environ["AWS_REGION"])

def main(event, context):
	key = event["pathParameters"]["image"]
	size = event["pathParameters"]["size"]
	result_url = resizeImage(os.environ["BUCKET"],key,size)
	
	response = {
		"statusCode": 301,
		"body": "",
		"headers": {
			"location": result_url
		}
	}
	return response