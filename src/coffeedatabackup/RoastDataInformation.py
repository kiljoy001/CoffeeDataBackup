import peewee as pw
import coffeedatabackup.roastplanmodels as rpm
from loguru import logger
import hashlib
logger.add('roast_data_log.log', rotation="00:00")


class RoastDataCollection:
    """
    Contains a collection of RoastData objects
    """
    def __init__(self):
        self.database = rpm.RoastDataInformation

    def add_roast_data_information(self, data_id, user_id, data_hash_value, data_file_name, data_bucket_name):
        """
        Adds roast data information to collection
        """
        try:
            self.database.create(
                data_id=data_id,
                user_id=user_id,
                data_hash_value=data_hash_value,
                data_file_name=data_file_name,
                data_bucket_name=data_bucket_name
            )
            logger.info(f'Roast data added successfully: {data_id}')
            return True
        except pw.IntegrityError:
            logger.warning(f'Data {data_id} already exists')
            return False

    def delete_roast_data_information(self, data_id):
        """
        Removes roast data information from collection
        :param data_id: string
        """
        try:
            self.database.get_by_id(data_id).delete_instance()
            logger.info(f'Data {data_id} successfully removed')
            return True
        except pw.DoesNotExist:
            logger.warning(f'Data {data_id} cannot be deleted - data not found')
            return False

    def modify_roast_data_information(self, data_id, user_id, data_hash_value, data_file_name, data_bucket_name):
        """
        Modifies roast data information
        :param data_id: string
        :param user_id: string
        :param data_hash_value: string
        :param data_file_name: string
        :param data_bucket_name: string
        """
        try:
            modify = self.database.get_by_id(data_id)
            (modify.update({
                self.database.user_id: user_id,
                self.database.data_hash_value: data_hash_value,
                self.database.data_file_name: data_file_name,
                self.database.data_bucket_name: data_bucket_name
            }).where(self.database.data_id == data_id).execute())
            logger.info(f'Data {data_id} successfully updated')
            return True
        except pw.DoesNotExist:
            logger.warning(f'Data {data_id} cannot be modified; Data does not exist')

    def search_roast_data_information(self, data_id):
        """
        Searches for roast data by data id
        """
        try:
            return_value = self.database.get_by_id(data_id)
            logger.info(f'Data {data_id} found')
            return return_value
        except pw.DoesNotExist:
            logger.warning(f'Data {data_id} not found')
            return None

    def get_all_data_by_user(self, user_id):
        """
        Returns all data by user
        :param user_id: string
        """
        result = []
        try:
            return_value = self.database.select().where(self.database.user_id == user_id)
            for value in return_value:
                result.append(value.data_id)
                result.append(value.user_id.user_id)
                result.append(value.data_hash_value)
                result.append(value.data_file_name)
                result.append(value.data_bucket_name)
            if result:
                logger.info(f'Data found for user {user_id}')
                return result
            else:
                logger.warning(f'No data found for user {user_id}')
                return None
        except pw.DoesNotExist:
            logger.warning(f'No data found for user {user_id}')

    @staticmethod
    def get_file_hash(path_to_file):
        """
        Returns hash of file
        :param path_to_file: path
        :return: string
        """
        h = hashlib.sha256()
        with open(path_to_file, 'rb') as file:
            while True:
                chunk = file.read(h.block_size)
                if not chunk:
                    break
                h.update(chunk)
            return h.hexdigest()
