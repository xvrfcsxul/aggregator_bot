import bson

from pymongo import MongoClient
from pymongo.collection import Collection

collection: Collection = MongoClient('mongo_db', 27017)['task']['salary']
if not collection.find_one():
    with open('sample_collection.bson', 'rb') as bson_file:
        collection.insert_many(bson.decode_all(bson_file.read()))
    print('ДБ успешно заполнена')
else:
    print('Ошибка: ДБ уже заполнена.')
