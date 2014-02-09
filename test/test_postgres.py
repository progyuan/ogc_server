import codecs
import os, sys
import pypyodbc
import decimal
import psycopg2 as psycopg

PG_DSN = r'host=localhost dbname=kmgdgeo user=postgres password=postgres port=5432'
ODBC_DSN = 'KMGD'

ENCODING = 'utf-8'
ENCODING1 = 'latin1'

def dec(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING)
    text, length = gb18030_encode(aStr, 'replace')
    return text
def dec1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_decode(aStr, 'replace')
    return text
def enc1(aStr):
    gb18030_encode, gb18030_decode, gb18030_reader, gb18030_writer =  codecs.lookup(ENCODING1)
    text, length = gb18030_encode(aStr, 'replace')
    return text

def update_line_name():
    lines = odbc_get_records('TABLE_LINE', '1=1')
    #towers = odbc_get_records('VIEW_TOWER_LINE', '1=1')
    #print(towers)
    db = psycopg.connect(PG_DSN)
    cursor = db.cursor()
    for line in lines:
        sql = """UPDATE line_all set line_name = '%s' where line_id='%s'""" % (line['line_name'], line['id']) 
        cursor.execute(sql)
    db.commit()
    #result = cursor.fetchall()
    #for i in result:
        #print(dec1(i[0]))
    cursor.close()
    db.close()
    
def update_tower_name():
    towers = odbc_get_records('VIEW_TOWER_LINE', '1=1')
    db = psycopg.connect(PG_DSN)
    cursor = db.cursor()
    for tower in towers:
        sql = """UPDATE towers_all set tower_name = '%s', line_name='%s' where tower_id='%s'""" % (tower['tower_name'], tower['line_name'], tower['id']) 
        cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

   
def odbc_get_records(table, condition):
    ret = []
    conn = None
    cur = None
    try:
        conn = pypyodbc.connect('DSN=%s' % ODBC_DSN)
        cur = conn.cursor()
    except:
        print(sys.exc_info()[1])
        return ret
 

    try:
        cur.execute(''' SELECT * FROM %s WHERE %s ''' % (table, condition) )
        for row in cur.fetchall():
            d = row.cursor_description
            line = {}
            for v in row:
                s = v
                if isinstance(s, decimal.Decimal):
                    s = float(v)
                if isinstance(s, str) or isinstance(s, unicode):
                    s = v.strip()
                #if d[row.index(v)][0] == 'end_geo_z':
                    #print('end_geo_z=%f' % s)
                line[d[row.index(v)][0]] = s
                if table=='VIEW_ATTACH_LINE_SEG':
                    if not 'end_geo_z' in str(d):
                        print(d)
            ret.append(line)
        
    except:
        print(sys.exc_info()[1])
        ret = []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return ret
    
    
if __name__=="__main__":
    update_tower_name()
    
    