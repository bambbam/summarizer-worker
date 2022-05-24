from boto3 import client

class S3Repository():
    def __init__(self, s3 : client, bucket: str):
        self.s3 = s3
        self.bucket = bucket
    
    def get_s3_url(self, prefix, key):
        url = self.s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': self.bucket,
                                                            'Key': prefix+'/'+key},
                                                    ExpiresIn=6000)
        return url
    
    def upload(self, file, prefix, key):
        try:
            self.s3.put_object(Bucket= self.bucket, Key=prefix+'/'+key, Body=file)
            return True
        except:
            return False
