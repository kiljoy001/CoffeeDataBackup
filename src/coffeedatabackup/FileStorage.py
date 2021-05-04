import boto3
import yaml
from src.coffeedatabackup.RoastDataInformation import RoastDataCollection
from pathlib import Path

SETTINGS = Path(__file__).parent.joinpath('settings.yaml')


def load_settings():
    with open(SETTINGS) as connection_setting:
        conn_string = yaml.load(connection_setting, Loader=yaml.Loader)
        return conn_string


def create_session():
    settings = load_settings()
    session = boto3.session.Session()
    filebase_client = session.client(
        service_name=settings['service_name'],
        aws_access_key_id=settings['access_key'],
        aws_secret_access_key=settings['secret_key'],
        endpoint_url=settings['end_point']
    )
    return filebase_client


def send_to_storage(file_name, bucket_name):
    uploader = create_session()
    path_split = file_name.split('/')
    remote_name = f'{path_split.pop()}_{file_hash}'
    uploader.upload_file(file_name, bucket_name, remote_name)


def get_from_storage(bucket_name, remote_file_name, local_file_name):
    downloader = create_session()
    retrieved_file = downloader.download_file(bucket_name, remote_file_name, local_file_name)
    return retrieved_file


def remove_from_storage(bucket_name, remote_file_name):
    remover = create_session()
    remover.delete_object(Bucket=bucket_name, Key=remote_file_name)

