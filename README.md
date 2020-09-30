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
assert S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True), 'saving failed'
```

    INFO:root:using accelerate endpoint
    INFO:root:data was saved to s3


## check if an object exist

```python
assert S3.exist('', bucket, user=USER, pw=PW, accelerate = False), 'bucket doesnt exist'
```

    INFO:root:using standard endpoint


## load object

```python
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
assert result == sampleDict, f'wrong result {result}, should be {sampleDict}'
```

    INFO:root:using accelerate endpoint
    INFO:root:object exists, loading
    INFO:root:using accelerate endpoint


## presign download object

```python
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
```

    INFO:root:using accelerate endpoint
    INFO:root:using accelerate endpoint





    {'test': 'bool'}



```python
import bz2, json
r = requests.get(url)
result = json.loads(bz2.decompress(r.content).decode())
assert result == sampleDict, 'not returning the correct object'
print(f'result is {result}')
```

    result is {'test': 'bool'}

