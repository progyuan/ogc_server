# -*- coding: utf-8 -*-
import os
import sys
from pymongo import MongoClient, ReadPreference
from bson.code import Code
from bson.son import SON
from module_locator import dec, enc

def test_average():
    # client = MongoClient('localhost',  27017,  slave_okay=True, replicaset='kmgdrs',  read_preference = ReadPreference.PRIMARY)
    client = MongoClient('localhost',  27017)
    db = client['test']
    if 'user_info' in db.collection_names(False):
        db.drop_collection('user_info')
    user_info = db.create_collection('user_info')
    #else:
        #user_info = db['user_info']
        
    user_info.insert({"uid":"a123","type":"man","class":2,"score":{"math":80,"english":60,"chinese":90}})
    user_info.insert({"uid":"b123","type":"female","class":2,"score":{"math":100,"english":90,"chinese":80}})
    user_info.insert({"uid":"c123","type":"man","class":2,"score":{"math":60,"english":50,"chinese":88}})
    user_info.insert({"uid":"d123","type":"female","class":2,"score":{"math":79,"english":87,"chinese":78}})
    user_info.insert({"uid":"e123","type":"female","class":1,"score":{"math":79,"english":87,"chinese":78}})    
    user_info.insert({"uid":"f123","type":"man","class":1,"score":{"math":99,"english":27,"chinese":60}})    
    
    
    mapfunc = Code("function() {"
              "   emit(this.class,this.score);"
              "}"
              )
               
    reducefunc = Code("function(key,values){"
                  "    var result={math:0,english:0,chinese:0,count:0};"
                  "    for (var i = 0; i < values.length; i++) {" 
                  "       result.math += values[i].math;"
                  "       result.english += values[i].english;"
                  "       result.chinese += values[i].chinese;"
                  "       result.count += 1;"
                  "    }"       
                  "    return result;"
                  "}"       
                 )
    finalizefunc = Code("function(key,values){"
                  "   var result={math:0,english:0,chinese:0};"
                  "   result.math = values.math/values.count;"
                  "   result.english = values.english/values.count;"
                  "   result.chinese = values.chinese/values.count;"
                  "   return result;"
                  "}"       
                 )
    results = user_info.map_reduce(mapfunc,reducefunc,"class_user", finalize=finalizefunc)
    #results = user_info.map_reduce(mapfunc,reducefunc,"class_user")
    for i in results.find():
        print(i)
    
def test_isolutor_count():
    client = MongoClient('localhost',  27017,  slave_okay=True, replicaset='kmgdrs',  read_preference = ReadPreference.PRIMARY)
    db = client['ztgd']
    features = db['features']
    mapfunc = Code("function() {"
              "    var idx = this.properties.name.indexOf('#');"
              "    var line_name = this.properties.name.slice(0, idx);"
              "    if(this.properties.metals){"
              "        var count = 0;"
              "        this.properties.metals.forEach(function(metal) {"
              "            if(metal.type == '绝缘子串'){"
              #"            if(metal.type == '防振锤'){"
              "                 emit(line_name, {count:1});"
              "            }"
              "        });"
              "    }"
              "}"
              )
    
    reducefunc = Code("function(key,values){"
                  "    var result = {count:0};"
                  "    for (var i = 0; i < values.length; i++) {" 
                  "       result.count += values[i].count;"
                  "    }"       
                  "    return result;"
                  "}"       
                 )
    
    results = features.map_reduce(mapfunc,reducefunc,"isolutor_count")
    for i in results.find():
        print('%s=%d' % (enc(i['_id']), i['value']['count']))
    
def test_check_edge_ring():
    client = MongoClient('localhost',  27017)
    db = client['kmgd']
    edges = db['edges']

    startid = '533e88cbca49c8156025a61a'
    mapfunc = Code("function() {"
              "   if(this.properties.start === ObjectId(" + startid + ")){"
              "       emit(this.properties.end);"
              "   }"
              "}"
              )

    reducefunc = Code("function(key,values){"
                  "    var result={start:null, end:null};"
                  "    for (var i = 0; i < values.length; i++) {"
                  "       result.math += values[i].math;"
                  "       result.english += values[i].english;"
                  "       result.chinese += values[i].chinese;"
                  "       result.count += 1;"
                  "    }"
                  "    return result;"
                  "}"
                 )
    # finalizefunc = Code("function(key,values){"
    #               "   var result={math:0,english:0,chinese:0};"
    #               "   result.math = values.math/values.count;"
    #               "   result.english = values.english/values.count;"
    #               "   result.chinese = values.chinese/values.count;"
    #               "   return result;"
    #               "}"
    #              )
    results = {}
    edges.map_reduce(mapfunc,reducefunc,results)
    print(results)



if __name__ == '__main__':
    test_isolutor_count()

    