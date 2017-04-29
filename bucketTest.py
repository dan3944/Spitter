import boto.s3
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = 'AKIAIWSDS2KRBFRPN2RA'
AWS_SECRET_ACCESS_KEY = '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'

bucket_name = 'twinty'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)

bucket = conn.get_bucket(bucket_name)

k = Key(bucket)
k.key = 'tweets'
k.set_contents_from_string('This is tweet')

k.set_acl('public-read')