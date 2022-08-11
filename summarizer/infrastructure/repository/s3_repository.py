from boto3 import client

from summarizer.exception import DatabaseException

class S3Repository():
    def __init__(self, s3 : client, bucket: str):
        self.s3 = s3
        self.bucket = bucket
    
    def get_s3_url(self, prefix, key):
        try:
            url = self.s3.generate_presigned_url(   'get_object',
                                                    Params={'Bucket': self.bucket,
                                                            'Key': prefix+'/'+key},
                                                    ExpiresIn=6000)
            return url
        except:
            raise DatabaseException(f"{self.__class__} get_s3_url method doesn't work")
    
    def upload(self, file, prefix, key):
        try:
            self.s3.put_object(Bucket= self.bucket, Key=prefix+'/'+key, Body=file)
        except:
            raise DatabaseException(f"{self.__class__} upload method doesn't work")

    def upload_video(self, file_path, prefix, key):
        try:
            self.s3.upload_file(Bucket= self.bucket, Key=prefix+'/'+key, Filename=file_path)
        except:
            raise DatabaseException(f"{self.__class__} upload_video method doesn't work")
