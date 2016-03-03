"""
.. Copyright (c) 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

connect.py
"""

import os
import random

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

import constants

def test():
    print(os.environ['HOME'])
    random.seed()
    client = MongoClient(
            constants.MONGO_CLIENT['host'], 
            constants.MONGO_CLIENT['port']
            )
    print('connection opened')
    try:
        db = client[constants.DB]
        coll = db.get_collection(constants.COLLECTION)
        bulk = coll.initialize_unordered_bulk_op()
        bulk.insert({'val': random.randrange(1000000)})
        result = bulk.execute()
    except BulkWriteError:
        print('ERROR writing to mongo!')
    else:
        print('{} record(s) inserted'.format(result['nInserted']))
    finally:
        client.close()
        print('connection closed')

if __name__ == '__main__':
    test()
