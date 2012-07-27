'''
Created on Mar 13, 2012

@author: elifinkelshteyn
'''
import datetime, re, yaml

class PigScriptGenerator(object):
    '''
    This generates a dynamic pig script that should output a bunch of x and y
    coordinates.
    '''

    def __init__(self, params):
        self.main_pig = params['script']
        self.date_range = params['date_range']
        self.rotation = params['rotation']
        #generate a schema string
        schema_file_name = params['schema']
        schema_file = open(schema_file_name)
        schema = yaml.load(schema_file)
        self.schema = '(\n'
        for member,type in schema['schema']['members'].items():
            self.schema += member + ':' + type + ',\n'
        self.schema = self.schema[:-2] + ');\n'

    def generate(self):
        start_date = self.date_range[0]
        end_date = self.date_range[1]
        _pig = ''
        dates_list = self.generate_dates(start_date, end_date)
        for date in dates_list:
            date_string = self.get_readable_date(date)
            dated_pig = re.sub("\$date", date_string, self.main_pig)
            _pig += ("loaded_set = LOAD '" + self.get_files(date) + "' USING " +
                     "PigStorage('\u0001') AS " + self.schema + dated_pig)
            if date.ctime() == start_date.ctime():
                if self.rotation == 'rotated':
                    _pig += ''' final_set = FOREACH pre_final 
                                            GENERATE colname, total, date; '''
                else:
                    _pig += ''' final_set = FOREACH pre_final 
                                            GENERATE total, date; '''
            else:
                _pig +=" final_set = UNION final_set, pre_final; "
        _pig += "\nSTORE final_set INTO '$output' USING PigStorage('\\t');"
        return _pig
        
    #We'll use this to generate the dates we want to run for
    def generate_dates(self, start_date, end_date):
        td = datetime.timedelta(hours=24)
        current_date = start_date
        dates_list = []
        while current_date <= end_date:
            dates_list.append(current_date)
            current_date += td
        return dates_list
    
    #get lil bro hdfs file locations based on a date
    def get_files(self, date_obj):
        return "/data/lil_brother/www/0[0-9]/%s.log.gz" % (
               self.get_readable_date(date_obj))
    
    def get_readable_date(self, date_obj):
        date = "%d/%d/%d" % (date_obj.year, date_obj.month, date_obj.day)
        return re.sub(r'(/|^)(\d)(?=/|$)',r'\g<1>0\g<2>',date)
    
