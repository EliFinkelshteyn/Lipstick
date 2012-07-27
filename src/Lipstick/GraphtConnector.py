'''
Created on Mar 15, 2012

@author: elifinkelshteyn
'''
import sys
print sys.path
from com.xhaus.jyson import JysonCodec as json
import urllib2, time
from datetime import datetime

class GraphtConnector(object):
    '''
    accepts some timestamps and values along with 
    '''

    def __init__(self, address):
        if not address: raise "no uri_base specified!"
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.address = address
    
    def record_data_points(self, metric_name, data):
        '''data comes in the form of:
        [{'total': u'149408', 'date': u'2012/02/13'}, 
         {'total': u'144314', 'date': u'2012/02/14'}]...'''
        for point in data:
            timestamp = point['date']
            del point['date']
            segmentations = {'main' : point}
            self.record_data_point(metric_name, timestamp, segmentations)
            
    def record_data_point(self, metric_name, timestamp, segmentations, value=None):
        #if it's not an epoch time, we assume it's a standard lil_bro date
        if not unicode.isnumeric(timestamp):
            timestamp = datetime.strptime(timestamp, "%Y/%m/%d")
            timestamp = time.mktime(timestamp.timetuple())
        uri_time = int(timestamp)
        uri = '/api/metrics/%s/data_points/%s' % (metric_name, uri_time)
        uri = self.address + uri
        if uri[:7] != 'http://': uri = 'http://' + uri
        #if segmentations is None: segmentations = {'sort_method':{'logged_in_relevance2':80085}}
        content_dict = {'metric_name' : metric_name, 
                        'timestamp' : timestamp,
                        'value' : value,
                        'segmentations' : segmentations}
        if value is None: del content_dict['value']
        content = json.dumps(content_dict)
        #content = json.dumps({"timestamp":1331899200,"metric_name":"blah_test_blah","segmentations":{"data_times":{"90th":"1175","min":"1","max":"4814","mean":"41.65","median":"306","95th":"1858"}}})
        #print uri
        #print content
        request = urllib2.Request(uri, data=content)
        request.add_header('content-type', 'application/json')
        request.get_method = lambda: 'PUT'
        url = self.opener.open(request)
        print url.read()