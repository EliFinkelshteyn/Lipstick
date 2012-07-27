'''
Created on Mar 13, 2012

@author: elifinkelshteyn
'''
import PigScriptGenerator, sys
from GraphtConnector import GraphtConnector
#no MatPlotter for now since it's incompatible with Jython. Shit.
#import MatPlotter

# explicitly import Pig class
from org.apache.pig.scripting import Pig

class PigRunner(object):
    '''
    This is just the main file that runs everything
    '''
    def make_dict_from_results(self, result_iter):
        self.result = []
        columns = self.params['columns']
        result = [[] for col in columns]
        for tup in result_iter:
            tup = tup.toDelimitedString('\u0001')
            tup = tuple(tup.split('\u0001'))
            for idx, item in enumerate(tup):
                result[idx].append(item)
        print "rotated is " + self.params['rotation']
        if self.params['rotation'] == 'rotated':
            print "ROTATED"
            '''this means the first column in the set really lists the names we 
            want for all the columns that will be in our final set.
            NOTE: this assumes you just have three columns (colname, 
            some number, date.'''
            self.params['columns'] = list(set(result[0]))
            date = ''
            for idx in xrange(0,len(result[0])):
                if result[2][idx] != date:
                    date = result[2][idx]
                    self.result.append({'date' : unicode(date)})
                else:
                    colname = result[0][idx]
                    number = result[1][idx]
                    self.result[-1][colname] = number
        else:
            for idx in xrange(0,len(result[0])):
                self.result.append( dict((columns[lst_idx] , lst[idx]) 
                                    for lst_idx,lst in enumerate(result)))
        print self.result


    def set_param_defaults(self):
        self.params.setdefault('rotation', 'normal')
    
    def __init__(self, params):
        # BIND and RUN
        self.params = params
        self.set_param_defaults()
        Pig.fs("rmr " + self.params['output_name'])
        generator = PigScriptGenerator.PigScriptGenerator(self.params)
        full_script = generator.generate()
        
        P = Pig.compile( full_script )
        
        results = P.bind({
                              'output':self.params['output_name'],
                              }).runSingle()
        
        if results.isSuccessful() :
            print 'Pig job succeeded'
        else :
            raise 'Pig job failed'
        result_iter = results.result("final_set").iterator()
        
        #This takes care of turning our iter into something we can use.
        self.make_dict_from_results(result_iter)
        
        send_to_grapht = raw_input('do you want to send this data to grapht?')
        if send_to_grapht not in ('y', 'yes', '1'): 
            sys.exit()
        connector = GraphtConnector('grapht.shuttercorp.net')
        metric = self.params['output_name']
        connector.record_data_points(metric, self.result)
        