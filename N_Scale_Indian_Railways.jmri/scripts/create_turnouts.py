"""
    File: create_turnouts.py
    Author: Abhishek Banerji
    Purpose: Create blocks, sensors and lights and associate them with each other as needed
    Algorithm
        - Step 1: Get basic information about the block - name, panel indicator and properties
        - Step 2: Create Sensor
        - Step 3: Create Block and connect to sensor
        - Step 4: If Panel Indicator is needed, create light and associate with sensor

    Block Configuration File Structure
        - User Name
        - Panel
        - Comments
        - Properties

"""


import csv
import json
import re
import jarray
import jmri


class CreateTurnouts(jmri.jmrit.automat.AbstractAutomaton) :
    """
     Script Configuration
    """
    BASEDIR = "/Users/banerjia/jmri_layouts/N_Scale_Indian_Railways.jmri/resources"
            
    # Node Addresses
    NODE_ADDR = {
        "SENSORS": 1,
        "TURNOUTS": 2,
        "PANELS" : 3
    }

    # Station Config
    STATION_CD = 'MML'


    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.

        filePath = "{}/MML_sw_config.csv".format(self.BASEDIR)
        with open(filePath, 'rt') as fileTurnouts:
            
            fileTurnoutsReader = csv.reader(fileTurnouts, delimiter = ',')

            # Counters
            header_skipped = False
            sensors_count = 1
            turnouts_count = 1

            for turnout_entry in fileTurnoutsReader:
                # Skip Header Row
                if not header_skipped:
                    header_skipped = True
                    continue
                
                # Gather basic information
                turnout_userName = "{} {}".format(self.STATION_CD, turnout_entry[0])
                turnout_userName_for_related_objects = turnout_userName.replace(self.STATION_CD, '').lstrip()
                turnout_panel_ind = (turnout_entry[1].upper() == "TRUE")
                turnout_comments = turnout_entry[2]
                _prop_string = re.sub('(\w+):([^;}]+)',r'"\1":"\2"',turnout_entry[3]).replace(';',',')
                turnout_properties = json.loads(_prop_string)
                turnout_systemName = "CT{}{:03d}".format(self.NODE_ADDR["TURNOUTS"],turnouts_count)

                obj_turnout = turnouts.provideTurnout(turnout_systemName)                
                obj_turnout.setUserName(turnout_userName)
                obj_turnout.setComment(turnout_comments)
                for key in turnout_properties:
                    obj_turnout.setProperty(key, turnout_properties[key])
                
                obj_turnout.setProperty("PanelSwitch", turnout_panel_ind)
                
                turnouts.register(obj_turnout)

                turnouts_count = turnouts_count + 1
        return

    def handle(self):
        return 0

CreateTurnouts().start()
