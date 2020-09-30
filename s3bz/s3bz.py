# AUTOGENERATED! DO NOT EDIT! File to edit: s3bz.ipynb (unless otherwise specified).

__all__ = ['S3', 'Requests']

# Cell
from botocore.config import Config
import bz2, json, boto3, logging, requests

# Cell
class S3:
  @staticmethod
  def s3(region = 'ap-southeast-1', user = None, pw = None, accelerate = True, **kwargs):
    '''
    create and return s3 client
    '''
    logging.info(f'using {("standard","accelerate")[accelerate]} endpoint')
    config = Config(s3={"use_accelerate_endpoint": accelerate,
                        "addressing_style": "virtual"})
    s3 = boto3.client(
        's3',
        aws_access_key_id= user,
        aws_secret_access_key= pw,
        region_name = region,
        config = config
      )
    return s3
  @classmethod
  def save(cls,  key, objectToSave, bucket = '',**kwargs):
    '''
    save an object to s3
    '''
    s3 = cls.s3(**kwargs)
    compressedData = bz2.compress(json.dumps(objectToSave).encode())
    result = s3.put_object(Body=compressedData, Bucket=bucket, Key=key)
    success = result['ResponseMetadata']['HTTPStatusCode'] ==  200
    logging.info('data was saved to s3')
    if not success: raise Error(success)
    else: return True
  @classmethod
  def exist(cls, key, bucket, **kwargs):
    return 'Contents' in cls.s3(**kwargs).list_objects(
        Bucket=bucket , Prefix=key )
  @classmethod
  def load(cls, key, bucket='', **kwargs):
    if not cls.exist(key, bucket, **kwargs):
      logging.info('object doesnt exist')
      return {}
    logging.info('object exists, loading')
    s3 = cls.s3(**kwargs)
    requestResult =  s3.get_object(
                  Bucket = bucket,
                  Key = key
                )
    allItemsByte = next(requestResult.get('Body',None))
    if not allItemsByte: raise ValueError('all data does not exist in the database')
    allItems = json.loads(bz2.decompress(allItemsByte).decode())
    return allItems

  @classmethod
  def presign(cls, key, expiry = 1000, bucket = '',**kwargs):
    if not cls.exist(key,bucket=bucket,**kwargs): return 'object doesnt exist'
    s3 = cls.s3(**kwargs)
    result = s3.generate_presigned_url(
        'get_object',
          Params={'Bucket': bucket,
                  'Key': key},
        ExpiresIn=expiry)
    return result

# Cell
class Requests:
    '''
      for uploading and downloading contents from url
    '''
    @staticmethod
    def getContentFromUrl( url):
      result = requests.get(url)
      if not result.ok:
        print('error downloading')
        return result.content
      content = result.content
      decompressedContent = bz2.decompress(content)
      contentDict = json.loads(decompressedContent)
      return contentDict