# -*- coding: utf-8 -*-
import codecs
import os, sys
from lxml import etree
import pypyodbc
import uuid

ENCODING = 'utf-8'
def dec(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_encode(aStr, 'replace')
    return text

KML_FILE = dec(r'D:\gis\南网\昆明局资料\输电线路_500kv.kml')
ODBC_DSN = 'KMGD'

def read_kml(filepath):
    tree = etree.parse(filepath)
    lines = []
    if tree:
        root = tree.getroot()
        for child in root:
            for child1 in child:
                for child2 in child1:
                    line = {}
                    tag = child2.tag.replace('{http://www.opengis.net/kml/2.2}','')
                    if tag in ['Folder']:
                        linename = None
                        for item in child2:
                            tagname = item.tag.replace('{http://www.opengis.net/kml/2.2}','')
                            if tagname == 'name':
                                #print('%s' % item.text)
                                linename = item.text
                                line['name'] = linename
                            if tagname == 'Region':
                                line['box'] = {'north':float(item[0][0].text),'south':float(item[0][1].text),'east':float(item[0][2].text),'west':float(item[0][3].text)}
                            if tagname == 'Placemark':
                                if not line.has_key('towers'):
                                    line['towers'] = []
                                tower = {}
                                tower['name'] = item[0].text
                                tower['coordinates'] = {}
                                arr = item[2][2].text.split(',')
                                tower['coordinates']['lgt'] = float(arr[0])
                                tower['coordinates']['lat'] = float(arr[1])
                                line['towers'].append(tower)
                        lines.append(line)
        #print(lines)
        #for line in lines:
            ##for k in line.keys():
            #print('%s=%s' % (line['name'],str(line['towers'])))
    return lines

def insert_line(lines):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect('DSN=%s' % ODBC_DSN)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    #cur.execute('''SELECT * FROM TABLE_LINE  ''')
    #for d in cur.description: 
        #print (d[0])
    
    #print ('')   
    #for row in cur.fetchall():
        #for field in row: 
            #print (field )
        #print ('')        
    
    for line in lines:
        cur.execute('''INSERT INTO TABLE_LINE VALUES(?, ?, ?, ?, ?, ?, ?)''',(str(uuid.uuid4()),'', line['name'], line['box']['north'], line['box']['south'], line['box']['east'], line['box']['west']))
    cur.commit()
    
    cur.close()
    conn.close()
    
def insert_line_tower(lines):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect('DSN=%s' % ODBC_DSN)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    for line in lines:
        lineid = str(uuid.uuid4())
        cur.execute('''INSERT INTO TABLE_LINE VALUES(?, ?, ?, ?, ?, ?, ?)''',(lineid, '', line['name'], line['box']['north'], line['box']['south'], line['box']['east'], line['box']['west']))
        tower_startid, tower_endid = None, None
        for tower in line['towers']:
            tower_endid = towerid = str(uuid.uuid4())
            if line['towers'].index(tower)   == len(line['towers'])-1:
                tower_startid = None
            if tower_startid and tower_endid:
                cur.execute('''INSERT INTO TABLE_TOWER_RELATION VALUES(?, ?, ?, ?)''',(str(uuid.uuid4()), lineid, tower_startid,  tower_endid))
                
            cur.execute('''INSERT INTO TABLE_TOWER_POS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(towerid, lineid, '','','','','','','','',tower['coordinates']['lgt'],tower['coordinates']['lat'],0.0,165.0,0.0,'500kv1',tower['name']  ))
            for i in range(8):
                attachid = str(uuid.uuid4())
                offset_x = -65.0
                offset_y = 0.0
                if i>3:
                    offset_x = 65.0
                if i in [0, 4]:
                    offset_y = 145.0
                elif i in [1, 5]:
                    offset_y = 125.0
                elif i in [2, 6]:
                    offset_y = 105.0
                elif i in [3, 7]:
                    offset_y = 85.0
                cur.execute('''INSERT INTO TABLE_TOWER_ATTACH_POINT VALUES(?, ?, ?, ?, ?)''',(attachid, towerid,  i,  offset_x, offset_y))
            tower_startid = tower_endid    
    cur.commit()
    
    cur.close()
    conn.close()

def get_records(table, condition):
    ret = []
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect('DSN=%s' % ODBC_DSN)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
 
    cur.execute(''' SELECT * FROM %s WHERE %s ''' % (table, condition) )

    for row in cur.fetchall():
        d = row.cursor_description
        line = {}
        for v in row:
            s = v
            #if isinstance(s, float):
                #s = str(v)
            if isinstance(s, str) or isinstance(s, unicode):
                s = v.strip()
            line[d[row.index(v)][0]] = s
        ret.append(line)
    return ret
 
def get_line_seg_count():
    segs = get_records('TABLE_LINE_SEG', '1=1')
    print(len(segs))
    segs = get_records('VIEW_ATTACH_LINE_SEG', '1=1')
    print(len(segs))
    
    
def insert_line_seg():
    lines = get_records('TABLE_LINE', '1=1')
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect('DSN=%s' % ODBC_DSN)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return 
    #print(len(lines))
    for line in lines:
        attas = get_records('VIEW_ATTACH_LINE_SEG', "line_id='%s'" % line['id'])
        print('attachpoint rec=%d' % len(attas))
        for atta in attas:
            segid = str(uuid.uuid4())
            cur.execute('''INSERT INTO TABLE_LINE_SEG VALUES(?, ?, ?, ?, ?, ?)''',(segid, line['id'], atta['start_point_id'],atta['end_point_id'], 0.9, '' ))
                
        
    
    cur.commit()
    cur.close()
    conn.close()
    
def delete_from_table(table, condition):
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect('DSN=%s' % ODBC_DSN)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return
    
    cur.execute(''' DELETE FROM  %s where %s ''' % (table, condition))
    cur.commit()
    cur.close()
    conn.close()

    
def clear_table():
    delete_from_table('TABLE_LINE', '1=1')
    delete_from_table('TABLE_LINE_SEG', 'tensor_T0 != 1')
    delete_from_table('TABLE_TOWER_RELATION', '1=1')
    delete_from_table('TABLE_TOWER_POS', 'cod_station_func IS NOT NULL')
    delete_from_table('TABLE_TOWER_ATTACH_POINT', 'offset_y != 120')
    

if __name__=="__main__":
    #clear_table()
    #data = read_kml(KML_FILE)
    #insert_line_tower(data)
    #insert_line_seg()
    get_line_seg_count()
    
    