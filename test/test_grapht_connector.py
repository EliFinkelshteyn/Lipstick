import sys
sys.path.append("../src")
import LilBroFramework.GraphtConnector as GraphtConnector
connector = GraphtConnector.GraphtConnector('grapht.shuttercorp.net')
result = [{'num': 50000, 'total': u'149408', 'date': u'2012/02/13'}, {'num' : 10, 'total': u'144314', 'date': u'2012/02/14'}]
new_result = [{u'(chrome,16.0)': u'18041', u'(chrome,5.0)': u'19', u'(explorer,7.0)': u'5384', u'(firefox,7.0)': u'541', u'(firefox,12.0)': u'22', u'(chrome,7.0)': u'14', u'(blackberry-new,7.0)': u'12', u'(firefox,2.0)': u'69', u'(firefox,5.0)': u'568', u'(opera,9.50)': u'12', u'(ipad,5.1)': u'365', u'(firefox,3.6)': u'3579', u'(chrome,17.0)': u'291', u'(opera,9.30)': u'3', u'(firefox,1.0)': u'25', u'(opera,9.62)': u'2', u'(konqueror,4.7)': u'1', u'(firefox,11.0)': u'187', u'(chrome,12.0)': u'6719', u'(konqueror,4.4)': u'1', 'date': u'2012/02/07', u'(explorer,8.0)': u'17970', u'(safari,7.1)': u'4'}]
newer_result = [{'date': u'2012/02/07', 'explorer8': 17970}, {'total': u'149408', 'date': u'2012/02/13'}]
connector.record_data_points('test_metric3', newer_result)
