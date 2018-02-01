from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1/')

db = client.cmc
raw_data = db.raw_data

ids = []

counter = {
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 0,
    '7': 0,
    '8': 0,
    '9': 0
}

for data in raw_data.find({}, {'id':1}).sort('grupo'):
    entity_id = int(data['id'])
    try:
        ids.index(entity_id)
    except:
        ids.append(entity_id)

ids = sorted(ids)

for entity_id in ids:
    first = raw_data.find_one({'id':str(entity_id)}, {'id':0})
    
    entity = {
        'nome': first['nome'],
        'cargo': first['cargo'],
        'nome_grupo': first['nome_grupo'],
        'grupo': first['grupo'],
        'salaries': {}
    }

    for salary in raw_data.find({'id':str(entity_id)}, {'salary':1, 'mesano':1}).sort('mesano'):
        data = salary['mesano']
        del salary['mesano']
        del salary['_id']

        entity['salaries'][data] = salary['salary']

    counter[str(entity['grupo'])] += 1

    if entity['grupo'] is 1:
        db.vereadores.insert_one(entity)
    elif entity['grupo'] is 2:
        db.efetivos.insert_one(entity)
    elif entity['grupo'] is 3:
        db.comissionados.insert_one(entity)
    elif entity['grupo'] is 4:
        db.inativos.insert_one(entity)
    elif entity['grupo'] is 5:
        db.ouvidor.insert_one(entity)
    elif entity['grupo'] is 6:
        db.cedido_para_camara.insert_one(entity)
    elif entity['grupo'] is 7:
        db.cedido_pela_camara.insert_one(entity)
    elif entity['grupo'] is 8:
        db.temporario.insert_one(entity)
    elif entity['grupo'] is 9:
        db.estagiario.insert_one(entity)

print(counter)