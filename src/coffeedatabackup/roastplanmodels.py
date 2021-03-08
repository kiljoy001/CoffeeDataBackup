import peewee as pw
import datetime

file = 'roast_planner.db'
db = pw.SqliteDatabase(file)


class BaseModel(pw.Model):
    """
    Base model class
    """

    class Meta:
        """
        Meta Class statement
        """
        database = db


class Users(BaseModel):
    """
    The class for the Users DB table
    """
    user_id = pw.CharField(primary_key=True, max_length=30)
    user_alias = pw.CharField(max_length=30)
    user_name = pw.CharField(max_length=30, default=None)
    user_last_name = pw.CharField(max_length=100, default=None)
    user_email = pw.CharField(max_length=100)
    user_company_name = pw.CharField(max_length=100, default=None)
    user_password = pw.CharField(max_length=128)

    class Meta:
        """
        Meta class statement
        """
        database = db
        table_name = 'users'


class RoastDataInformation(BaseModel):
    """
    The class for the uploaded roast data file
    """
    data_id = pw.CharField(primary_key=True, max_length=30)
    user_id = pw.ForeignKeyField(model=Users, backref='roastdatarmation',
                                 on_update='RESTRICT',
                                 on_delete='CASCADE')
    data_upload_time = pw.DateTimeField(default=datetime.datetime.utcnow)
    data_hash_value = pw.CharField(max_length=100)
    data_file_name = pw.CharField(max_length=100)
    data_bucket_name = pw.CharField(max_length=100)

    class Meta:
        """
        Meta class statement
        """
        database = db
        table_name = 'roastdata'


def create_tables(database, tables):
    """
    Creates tables passed to the function
    """
    database.create_tables(tables)
    return True


def main():
    """
    Connects DB & creates tables
    """
    db.connect(reuse_if_open=True)
    create_tables(db, (Users, RoastDataInformation))
    return True


if __name__ == '__main__':
    main()
