# -*- coding: utf-8 -*-

import copy
import pickle
from datetime import datetime, timedelta

from pymongo import MongoClient, ReadPreference
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
from werkzeug.contrib.sessions import SessionStore, Session
import db_util


SES_EXP = 14 * 24 * 60 * 60  # 14 days in seconds
SES_SHORT = 30 * 60  # 30 minutes in seconds


#class MongoSession(Session):
    #def __init__(self, data=None, sid=None, new=False):
        #Session.__init__(self, data, sid, new)
        
        
def add_mongo_id(obj, objidkeys = ['_id', u'_id',]):
    if isinstance(obj, str) or isinstance(obj, unicode):
        try:
            if len(obj) == 24:
                obj = ObjectId(obj)
        except:
            pass
        
        d = None
        try:
            d = datetime.strptime(obj, "%Y-%m-%d %H:%M:%S.%F")
        except:
            try:
                d = datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    d = datetime.strptime(obj, "%Y-%m-%d")
                except:
                    d = None
        if d:
            obj = d
        return obj
    elif isinstance(obj, Session):
        for k in obj.keys():
            if k in objidkeys and obj[k] is None:
                obj[k] = ObjectId()
            obj[k] = add_mongo_id(obj[k])
                
    elif isinstance(obj, list):
        for i in obj:
            obj[obj.index(i)] = add_mongo_id(i)
    return obj
    
def remove_mongo_id(obj):
    if isinstance(obj, ObjectId):
        obj = str(obj)
    elif isinstance(obj, Timestamp):
        obj = obj.as_datetime().strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, datetime):
        obj = obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = remove_mongo_id(obj[k])
    elif isinstance(obj, list):
        for i in obj:
            obj[obj.index(i)] = remove_mongo_id(i)
    return obj
    

class MongodbSessionStore(SessionStore):
    def __init__(self, session_class=None, host=None, port=None, replicaset=None, db=None, collection=None):
        SessionStore.__init__(self, session_class)
        self.host = host
        self.port = port
        self.replicaset = replicaset
        self.db_name = db
        self.collection_name = collection
        self.db = None
        self.collection = None
        self.client = None
        self.mongo_init()
    
    def mongo_init(self):
        if self.client and not self.client.alive():
            self.client.close()
            self.client = None
        if self.client is None:
            if self.replicaset and len(self.replicaset)>0:
                self.client = MongoClient(self.host, self.port, slave_okay=True, replicaset=str(self.replicaset),  read_preference = ReadPreference.PRIMARY)
            else:
                self.client = MongoClient(self.host, self.port, slave_okay=True)
            
            if self.client is None :
                raise Exception('mongodb session store client failed: host:%s,port:%d' % (self.host, self.port))
            
            if self.client and self.db_name and len(self.db_name)>0 and self.db_name in self.client.database_names():
                self.db = self.client[self.db_name]
            if self.collection_name and self.db and len(self.collection_name)>0 and self.collection_name in self.db.collection_names():
                self.collection = self.db[self.collection_name]
            if self.db is None or self.collection is None:
                raise Exception('mongodb session store init failed: db:%s,collection:%s' % (self.db_name, self.collection_name))
            
            
    def is_valid_key(self, key):
        ret = False
        try:
            oid = ObjectId(key)
            ret = True
        except:
            pass
        return ret

    def generate_key(self, salt=None):
        return str(ObjectId())
            
    def new(self, data):
        if isinstance(data, dict):
            data['session_timestamp'] = datetime.now()
            return self.session_class(data, self.generate_key(), True)
        else:
            raise Exception('data must be dict type')
        
    #def update(self, sid, data):
        #if isinstance(data, dict):
            #data['session_timestamp'] = datetime.now()
            #return self.session_class(data, sid, False)
        #else:
            #raise Exception('data must be dict type')

    def save(self, session):
        self.mongo_init()
        session['_id'] = ObjectId(session.sid)
        session['session_timestamp'] = datetime.now()
        self.collection.save(session)
        

    def delete(self, session):
        _id = ObjectId(session.sid)
        self.delete_data(_id)
    
    def delete_data(self, _id):
        self.mongo_init()
        try:
            self.collection.remove({'_id':_id})
        except:
            pass
        

    def get(self, sid):
        ret = None
        data = self.get_data(sid)
        if data:
            ret = self.session_class(data, sid, False)
        return ret
    
    def get_data(self, sid):
        self.mongo_init()
        if not self.is_valid_key(sid):
            return None
        rec = self.collection.find_one({'_id':ObjectId(sid)})
        return rec
    
    def get_data_by_username(self, sid, username):
        self.mongo_init()
        if not self.is_valid_key(sid):
            return None
        rec = self.collection.find_one({'_id':ObjectId(sid), 'username':username})
        return rec
    

    def list(self):
        ret = []
        self.mongo_init()
        cur = self.collection.find({})
        for i in cur:
            ret.append(i)
        return ret

    #def check_if_expired(self, now, data):
        #ret = False
        #second = int(db_util.gConfig['authorize_platform']['session']['session_age'])
        #if data:
            #if (now - data['session_timestamp']).seconds > second:
                #ret = True
        #return ret
            
    def delete_expired_list(self):
        seconds = int(db_util.gConfig['authorize_platform']['session']['session_age'])
        start_time = datetime.now() - timedelta(seconds=seconds) 
        self.mongo_init()
        try:
            self.collection.remove({'session_timestamp':{"$lt":start_time}})
            #ret = list(self.collection.find({'_id':{"$lt":dummy_id}}))
            #print(len(ret))
        except:
            raise
            
#if __name__=="__main__":
    #db_util.init_global()
    #ss = MongodbSessionStore(host=db_util.gConfig['authorize_platform']['mongodb']['host'], 
                                        #port=int(db_util.gConfig['authorize_platform']['mongodb']['port']), 
                                        #replicaset=db_util.gConfig['authorize_platform']['mongodb']['replicaset'],
                                        #db = db_util.gConfig['authorize_platform']['mongodb']['database'],
                                        #collection = db_util.gConfig['authorize_platform']['mongodb']['collection_session'],
                                        #)
    #ss.delete_expired_list()
    
    
    
    
    