'''
Created on Apr 12, 2011

@author: michel
'''
import unittest
from FeatureServer.WebFeatureService.FilterEncoding import FilterEncoding as fe
from wfs_server import WFSServer
from FeatureServer.DataSource.PostGIS import PostGIS
#from FeatureServer.Service import WFS


class SpatialOperatorTestCase(unittest.TestCase):
    datasource = None
    server = None
    params = {'type': 'PostGIS',
              'title': 'Point Type',
              'abstract': 'Point Type',
              'dsn' : 'host=localhost dbname=mysdb user=postgres password=postgres',
              'layer' : 'testpoint',
              'fid': 'gid',
              'geometry': 'geom',
              'srid' : '4326',
              'attribute_cols' : 'point_name, point_id, point_color',
              'bbox' : '102.714388095 24.6362239650001 102.853348618 24.8560861620001'
              }
    
    def setUp(self):
        pass
        #self.datasource = PostGIS('all', **self.params)
        #self.server = Server({'all': self.datasource})
    def tearDown(self):
        self.datasource = None
        self.server = None
    
    def testEquals(self):
        filters = {
            "<Filter>" +
                "<Equals>" + 
                    "<ValueReference>way</ValueReference>" +
                    "<Literal>" +
                        "<gml:Point srsName=\"EPSG:4326\">" +
                            "<gml:coordinates>5.9656087,46.144381600000003</gml:coordinates>" +
                        "</gml:Point>" +
                    "</Literal>" +
                "</Equals>" +
            "</Filter>" :
            "ST_Equals(way, ST_GeomFromGML('<gml:Point xmlns:gml=\"http://www.opengis.net/gml\" xmlns:regexp=\"http://exslt.org/regular-expressions\" srsName=\"EPSG:4326\"><gml:coordinates>5.9656087,46.144381600000003</gml:coordinates></gml:Point>'))"
        }
    
        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))
            
    def testBBOX(self):
        filters = {
            "<Filter>" +
                "<BBOX>" + 
                    "<ValueReference>way</ValueReference>" +
                    "<gml:Envelope xmlns:gml=\"http://www.opengis.net/gml\" srsName=\"asdf:EPSG:4326\">" +
                        "<gml:lowerCorner>5.95459 45.75986</gml:lowerCorner>" +
                        "<gml:upperCorner>10.52490 47.83528</gml:upperCorner>" + 
                    "</gml:Envelope>" +
                "</BBOX>" +
            "</Filter>" :
            "NOT ST_Disjoint(way, ST_MakeEnvelope(5.95459,45.75986,10.52490,47.83528, 4326))"
        }
        for fil, stmt in filters.iteritems():
            filterEncoding = fe.FilterEncoding(fil)
            filterEncoding.parse()
            self.assertEqual(stmt, filterEncoding.render(self.datasource))
    
    def testDatasource(self):
        print(self.datasource.getColumns())
        
    def testServer(self):
        service = WFSServer('../ogc-config.ini')
        service.load()
        #http://XIEJUN-DESKTOP:88/wfs?VERSION=1.1.0&SERVICE=WFS&REQUEST=GetCapabilities&TYPENAME=yn_point
        #http://XIEJUN-DESKTOP:88/wfs?VERSION=1.1.0&SERVICE=WFS&REQUEST=GetFeature&TYPENAME=yn_point
        url = '%s?VERSION=1.1.0&SERVICE=WFS&REQUEST=GetCapabilities' % service.config['wfs']['url']
        print(service.dispatchRequest())

        

class SpatialOperatorTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self,map(SpatialOperatorTestCase,
                                                     ("testEquals",
                                                      "testBBOX")))

def suite(): 
    suite = unittest.TestSuite()
    #suite.addTest(SpatialOperatorTestCase('testEquals'))
    #suite.addTest(SpatialOperatorTestCase('testBBOX'))
    #suite.addTest(SpatialOperatorTestCase('testDatasource'))
    suite.addTest(SpatialOperatorTestCase('testServer'))
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main(defaultTest='suite')
    
    
    