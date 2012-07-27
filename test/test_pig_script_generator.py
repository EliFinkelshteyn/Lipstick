import sys, datetime
sys.path.append("../src")
import Lipstick.PigScriptGenerator as PigScriptGenerator

pig = '''new = FOREACH loaded_set GENERATE
         browser_identity, ip_address;
         good = FILTER new BY (browser_identity IS NOT NULL)
         AND (NOT (browser_identity MATCHES '.*[0-9]+\\\..*'))
         AND (ip_address IS NOT NULL);
         distincted = DISTINCT good;
         distincted = FOREACH distincted GENERATE browser_identity;
         grouped = GROUP distincted BY browser_identity;
         pre_final = FOREACH grouped GENERATE
         group AS colname, COUNT(distincted) AS total, '$date' AS date;
'''
   
columns = ['colname', 'total', 'date']
date_range = [datetime.date(2012, 2, 1), datetime.date(2012, 2, 6)]
output_name = 'actions_by_browser2'

params = {'script':pig,
          'date_range':date_range,
          'output_name': output_name,
          'columns': columns,
          'rotation': 'rotated',
          'schema': '/Users/elifinkelshteyn/git/Lipstick/schemas/lil_bro.yaml'}

test_script = PigScriptGenerator.PigScriptGenerator(params)
print test_script.generate()
