from adapters.database.mongo_adapter import *


def test_should_get_connection_to_mongo_db():
    mongo = MongoDB(database_name='test', host='localhost', port=27017, username='root', password='root')
    assert isinstance(mongo.get_database_connection(), pymongo.mongo_client.database.Database)


def test_should_get_none_collection_from_mongo_db():
    mongo = MongoDB(database_name='test', host='localhost', port=27017, username='root', password='root')
    assert mongo.get_collection('test') is None
