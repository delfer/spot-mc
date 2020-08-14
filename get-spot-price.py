#!/usr/bin/env python3

import argparse
import boto3
from datetime import datetime, timedelta

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--aws_access_key")
parser.add_argument("--aws_secret_key")
parser.add_argument("--region")
parser.add_argument("--instance_type")
parser.add_argument("--price_gap_percentage")

# Read arguments from the command line
args = parser.parse_args()

client=boto3.client('ec2',
    region_name=args.region,
    aws_access_key_id=args.aws_access_key,
    aws_secret_access_key=args.aws_secret_key
)

response=client.describe_spot_price_history(
    InstanceTypes=[args.instance_type],
    ProductDescriptions=['Linux/UNIX'],
    StartTime=datetime.today() - timedelta(days=1),
    EndTime=datetime.today()
)

prices=[float(o['SpotPrice']) for o in response['SpotPriceHistory']]

if len(prices) > 0:
    print (max(prices) * (1 + float(args.price_gap_percentage)/100.0))
else:
    print (-1)