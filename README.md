# S3Bz
> save and load dictionary to s3 using bz compression


## Install

`pip install s3bz`

## How to use

### Create a bucket and make sure that it has transfer acceleration enabled
#### create a buket
`aws s3 mb s3://<bucketname>`
#### put transfer acceleration
`aws s3api put-bucket-accelerate-configuration --bucket <bucketname> --accelerate-configuration Status=Enabled`

First, import the s3 module

## dummy data

```python
from importlib import reload
from s3bz.s3bz import S3

bucket = 'pybz-test'
key = 'test.dict'
sampleDict = {'test': 'bool'}
```

## save object

```python
result = S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True)
print(('success', 'failed')[result])
```

    failed


## check if an object exist

```python
result = S3.exist('', bucket, user=USER, pw=PW, accelerate = False)
print(('doesnt exist', 'exist')[result])
```

    exist


## load object

```python
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
print(result)
```

    {'test': 'bool'}


## presign download object

```python
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
print(url)
```

    https://pybz-test.s3-accelerate.amazonaws.com/test.dict?AWSAccessKeyId=AKIAVX4Z5TKDVBQJXL2G&Signature=2bQJAd3INtaiZ7S21%2B7tdfv8jCA%3D&Expires=1601444222


### testing signed link

```python
import bz2, json
r = requests.get(url)
result = json.loads(bz2.decompress(r.content).decode())
print(f'result is {result}')
```

    result is {'test': 'bool'}

