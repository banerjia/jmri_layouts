import csv
import jarray
import jmri

class CreateSenors(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        base_dir = "/Users/banerjia/jmri_layouts/CMRI_Scripting.jmri/scripts/csv/MM"
        

        TURNOUTS_NODE_ADDR = 1
        SENSORS_NODE_ADDR = 2
        MAX_TURNOUTS = 48
        MAX_SENSORS = 24

        sensor_count  = 1
        turnout_count  = 1

        # Create Blocks & Sensors
        file_path = "/Users/banerjia/Library/Preferences/jmri_layouts/CMRI_Scripting.jmri/scripts/csv/sensors.csv"
        with open(file_path, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 1:
                    sensor_sys_name = "CS{:d}{:03d}".format(SENSORS_NODE_ADDR,sensor_count)
                    obj_sensor = jmri.InstanceManager.getDefault(jmri.SensorManager).newSensor(sensor_sys_name, row[0])   
                    obj_sensor.setComment(row[1])    
                    sensor_count = sensor_count + 1
                    if sensor_count > MAX_SENSORS:
                        break          
                line_count = line_count + 1


        # Create Turnouts
        file_path = "/Users/banerjia/Library/Preferences/jmri_layouts/CMRI_Scripting.jmri/scripts/csv/turnouts.csv"
        with open(file_path, 'rt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 1:
                    turnout_sys_name = "CT{:d}{:03d}".format(TURNOUTS_NODE_ADDR,turnout_count)
                    obj_turnout = jmri.InstanceManager.getDefault(jmri.TurnoutManager).newTurnout(turnout_sys_name, row[0])
                    obj_turnout.setComment(row[3])
                    turnout_count = turnout_count + 1
                    if(row[2] == '1'):
                        if sensor_count <= MAX_SENSORS:
                            obj_turnout.setFeedbackMode("ONESENSOR")
                            sensor_sys_name = "CS{:d}{:03d}".format(SENSORS_NODE_ADDR,sensor_count)
                            sensor_usr_name = "FDBK {}".format(row[0])
                            obj_sensor = jmri.InstanceManager.getDefault(jmri.SensorManager).newSensor(sensor_sys_name, sensor_usr_name)   
                            obj_sensor.setComment("Feedback sensor for turnout {}".format(turnout_sys_name))  
                            obj_turnout.provideFeedbackSensor(sensor_sys_name, 0)
                            sensor_count = sensor_count + 1
                    if turnout_count > MAX_TURNOUTS:
                        break
                line_count = line_count + 1


        return

    def handle(self):
        return 0

CreateSenors().start()
