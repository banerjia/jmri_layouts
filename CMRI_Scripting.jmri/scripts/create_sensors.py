import csv
import json
import re
import jarray
import jmri


class CreateSenors(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        base_dir = "/home/banerjia/jmri_layouts/CMRI_Scripting.jmri/scripts/csv/test_layout"
        

        TURNOUTS_NODE_ADDR = 1
        SENSORS_NODE_ADDR = 1
        MAX_TURNOUTS = 48
        MAX_SENSORS = 24

        sensor_count  = 1
        turnout_count  = 1

        # Create Blocks & Sensors
        file_path = "%s/sensors.csv" % (base_dir)
        with open(file_path, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 1:
                    sensor_sys_name = "CS{:d}{:03d}".format(SENSORS_NODE_ADDR,sensor_count)                    
                    obj_sensor = jmri.InstanceManager.getDefault(jmri.SensorManager).newSensor(sensor_sys_name, row[0])   
                    obj_sensor.setComment(row[3])
                    prop_string = re.sub('(\w+):([\w\d_]+)',r'"\1":"\2"',row[4]).replace(';',',')
                    props = json.loads(prop_string)
                    for prop_key in props:
                        obj_sensor.setProperty(prop_key, props[prop_key])
                    sensors.register(obj_sensor)
                    sensor_count = sensor_count + 1    
                line_count = line_count + 1
        return

    def handle(self):
        return 0

CreateSenors().start()
