"""
.. Copyright (c) 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

connect.py
"""

import os
import random
import ssl

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

import constants

def test():
    random.seed()
    ssl_path = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../ssl'))
    ssl_certfile = os.path.join(ssl_path, 'client.pem')
    ssl_ca_certs = os.path.join(ssl_path, 'ca.pem')
    print('certfile: {}'.format(ssl_certfile))
    client = MongoClient(
            constants.MONGO_CLIENT['host'], 
            constants.MONGO_CLIENT['port'],
            ssl=True,
            ssl_certfile=ssl_certfile,
            ssl_ca_certs=ssl_ca_certs,
            ssl_match_hostname=False
            )
    print('connection opened')
    try:
        db = client[constants.DB]
        coll = db.get_collection(constants.COLLECTION)
        bulk = coll.initialize_unordered_bulk_op()
        bulk.insert({'val': random.randrange(1000000)})
        print('record queued for insertion')
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
