import pymongo
from bson.son import SON
import pprint

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.cmc

raw_data = db.raw_data
entities = db.entities

ids = []

for row in raw_data.find({}, { 'id': 1 }):
    try:
        ids.index(int(row['id']))
    except:
        ids.append(int(row['id']))

for entity_id in sorted(ids):
    first = raw_data.find_one({ 'id': str(entity_id) })

    entity = {
        'id': entity_id,
        'nome': first['nome'],
        'cargo': first['cargo'],
        'grupo': first['grupo']
    }

    docs = raw_data.find(
                { 'id': str(entity_id) },
                {'id': 0, 'grupo': 0, 'nome': 0, 'cargo': 0, '_id': 0}
            ).sort('mesano')

    for doc in docs:
        mesano = doc['mesano']
        entity[mesano] = {}

        for field in doc:
            if field is 'mesano':
                continue
            entity[mesano][field] = doc[field]

    entities.insert_one(entity)
